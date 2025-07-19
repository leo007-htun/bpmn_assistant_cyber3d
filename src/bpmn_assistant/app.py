from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Union
import xml.etree.ElementTree as ET
from copy import deepcopy
import os, re, datetime, uuid, json

from bpmn_assistant.api.requests import (
    BpmnToJsonRequest,
    ConversationalRequest,
    DetermineIntentRequest,
    ModifyBpmnRequest,
)
from bpmn_assistant.core import handle_exceptions
from bpmn_assistant.core.enums import OutputMode
from bpmn_assistant.services import (
    BpmnJsonGenerator,
    BpmnModelingService,
    BpmnXmlGenerator,
    ConversationalService,
    determine_intent,
)
from bpmn_assistant.utils import (
    replace_reasoning_model,
    get_available_providers,
    get_llm_facade,
    send_prompt_to_llm,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bpmn_modeling_service = BpmnModelingService()
bpmn_xml_generator = BpmnXmlGenerator()

# --------------------------
# ✅ REQUEST MODELS
# --------------------------

class MessageHistoryItem(BaseModel):
    role: str
    content: str

class SuggestSecurityRequest(BaseModel):
    modified_bpmn_xml: str
    model: str
    message_history: List[MessageHistoryItem] = []

class ModifySecurityRequest(BaseModel):
    modification_log: List[Dict[str, Union[str, List[str]]]]
    count: int
    modified_bpmn_xml: str

# --------------------------
# ✅ BASIC ENDPOINTS
# --------------------------

@app.post("/bpmn_to_json")
@handle_exceptions
async def _bpmn_to_json(request: BpmnToJsonRequest) -> JSONResponse:
    bpmn_json_generator = BpmnJsonGenerator()
    result = bpmn_json_generator.create_bpmn_json(request.bpmn_xml)
    return JSONResponse(content=result)

@app.get("/available_providers")
@handle_exceptions
async def _available_providers() -> JSONResponse:
    providers = get_available_providers()
    return JSONResponse(content=providers)

@app.post("/determine_intent")
@handle_exceptions
async def _determine_intent(request: DetermineIntentRequest) -> JSONResponse:
    """
    ✅ Improved to detect confirmations like 'yes, apply' or 'no, skip'
    """
    model = replace_reasoning_model(request.model)
    llm_facade = get_llm_facade(model)

    # --- Custom intent prompt ---
    confirm_prompt = f"""
    You are an intent classifier. The conversation so far is:

    {request.message_history}

    Rules:
    - If the user explicitly confirms applying security mappings (e.g., "yes", "apply", "confirm", "do it"), return:
      {{ "intent": "modify_security", "confidence": 0.95 }}
    - If the user explicitly declines (e.g., "no", "skip", "not now"), return:
      {{ "intent": "chat", "confidence": 0.9 }}
    - Otherwise, classify normally:
      - if they want to edit/create BPMN → modify
      - if they ask about security → suggest_security
      - otherwise → talk

    Only return JSON with `intent` + `confidence`.
    """

    llm_intent_response = send_prompt_to_llm(llm_facade, confirm_prompt)
    print("🟡 INTENT RAW RESPONSE:", llm_intent_response)

    # Fallback to old determine_intent if needed
    try:
        parsed_intent = json.loads(llm_intent_response.replace("'", '"')) if isinstance(llm_intent_response, str) else llm_intent_response
        if "intent" in parsed_intent:
            return JSONResponse(content=parsed_intent)
    except:
        pass

    # Fallback legacy detection
    intent = determine_intent(llm_facade, request.message_history)
    return JSONResponse(content=intent)

@app.post("/modify")
@handle_exceptions
async def _modify(request: ModifyBpmnRequest) -> JSONResponse:
    llm_facade = get_llm_facade(request.model)
    text_llm_facade = get_llm_facade(request.model, OutputMode.TEXT)

    process = (
        bpmn_modeling_service.edit_bpmn(llm_facade, text_llm_facade, request.process, request.message_history)
        if request.process
        else bpmn_modeling_service.create_bpmn(llm_facade, request.message_history)
    )

    bpmn_xml_string = bpmn_xml_generator.create_bpmn_xml(process)
    return JSONResponse(content={"bpmn_xml": bpmn_xml_string, "bpmn_json": process})

@app.post("/talk")
@handle_exceptions
async def _talk(request: ConversationalRequest) -> JSONResponse:
    model = replace_reasoning_model(request.model)
    conversational_service = ConversationalService(model)

    if request.needs_to_be_final_comment:
        message = await conversational_service.make_final_comment_as_text(request.message_history, request.process)
    else:
        message = await conversational_service.respond_to_query_as_text(request.message_history, request.process)

    return JSONResponse(content={"message": message})

# --------------------------
# ✅ SUGGEST SECURITY
# --------------------------

@app.post("/suggest_security")
@handle_exceptions
async def suggest_security(request: SuggestSecurityRequest) -> JSONResponse:
    """
    Suggest security ontologies based on BPMN + conversation history.
    """
    # --- Extract available ontology paths ---
    modified_tree = ET.ElementTree(ET.fromstring(request.modified_bpmn_xml))
    modified_root = modified_tree.getroot()

    def extract_paths_from_xml(element, current_path="", paths=None):
        if paths is None:
            paths = []
        path = f"{current_path}/{element.tag}" if current_path else element.tag
        children = list(element)
        if children:
            for child in children:
                extract_paths_from_xml(child, path, paths)
        else:
            paths.append(path)
        return paths

    ontology_path = os.path.join(os.path.dirname(__file__), "ontology_template.xml")
    ontology_tree = ET.parse(ontology_path)
    ontology_root = ontology_tree.getroot()
    available_ontologies = extract_paths_from_xml(ontology_root)

    # ✅ Convert message history into readable text
    history_text = ""
    if request.message_history:
        history_text = "\n".join(
            [f"{msg.role.upper()}: {msg.content}" for msg in request.message_history]
        )

    # --- Build LLM prompt ---
    prompt = f"""
    You are a BPMN security assistant.
    
    Here is the previous conversation context:
    {history_text}

    The user provided this BPMN XML:
    {request.modified_bpmn_xml}

    These are the available ontology paths:
    {available_ontologies}

    First, provide a **short, brief and succinct explanation** of which parts of the BPMN need what kinds of security ontologies as in {available_ontologies} and why. 
    And what you have added to the BPMN.

    Then, return a JSON object with this exact structure:
    {{
        "explanation": "short explanation here",
        "security_ontologies": [
            {{
                "elementID": "task1",
                "elementText": "Send Email",
                "ontology_path": ["root/bpmnElement/accesscontrol/authentication"]
            }}
        ]
    }}
    """

    # --- Call the LLM ---
    llm_facade = get_llm_facade(request.model)
    raw_response = send_prompt_to_llm(llm_facade, prompt)

    print("🟡 LLM RAW RESPONSE TYPE:", type(raw_response))
    print("🟡 LLM RAW RESPONSE:", raw_response)

    explanation = "Invalid LLM response format."
    suggestions = []

    # --- CASE 1: Already a Python dict ---
    if isinstance(raw_response, dict):
        print("✅ Detected dict from LLM directly")
        explanation = raw_response.get("explanation", "")
        suggestions = raw_response.get("security_ontologies", [])

    # --- CASE 2: It's a JSON string ---
    elif isinstance(raw_response, str):
        normalized = raw_response.replace("'", '"')
        try:
            parsed = json.loads(normalized)
            print("✅ Parsed JSON successfully from LLM string")

            explanation = parsed.get("explanation", "")
            suggestions = parsed.get("security_ontologies") or parsed.get("suggestions", [])

        except Exception as e:
            print("❌ JSON parse failed, trying regex fallback:", e)
            
            # ✅ Correct: raw string + non-greedy prevents warnings
            match = re.search(r"\[.*?\]", raw_response, re.DOTALL)

            if match:
                json_part = match.group(0)
                explanation = raw_response[:match.start()].strip()
                try:
                    suggestions = json.loads(json_part)
                except Exception as inner_e:
                    print("❌ Failed regex JSON:", inner_e)
                    suggestions = []
            else:
                explanation = raw_response.strip()

    else:
        print("❌ Unknown LLM output format")

    # --- Save debug log ---
    log_data = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "user_prompt": prompt.strip(),
        "history_text": history_text,
        "raw_response": str(raw_response),
        "explanation": explanation,
        "suggestions": suggestions
    }
    os.makedirs("logs", exist_ok=True)
    save_path = os.path.join("logs", f"suggestions_{uuid.uuid4()}.json")
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2)
    print(f"✅ Security suggestion log saved at: {os.path.abspath(save_path)}")

    # --- Return structured output ---
    return JSONResponse(content={
        "explanation": explanation,
        "security_ontologies": suggestions,
        "suggestions": suggestions,
        "modification_log": suggestions  # same for Unity
    })



