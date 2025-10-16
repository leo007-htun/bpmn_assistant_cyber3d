# CyberD3sign: Comprehensive Technical Architecture Report

**Document Version:** 1.0
**Date:** 2025-10-16
**Prepared For:** Technical Documentation & System Understanding

---

## Executive Summary

CyberD3sign is a sophisticated hybrid application that combines 3D visualization (Unity) with AI-powered business process modeling and security analysis. The system consists of three main architectural layers:

1. **Frontend Layer:** Unity 2020.2.1f1 3D BPMN editor with interactive visualization
2. **AI Backend Layer:** Python FastAPI server with multi-LLM integration for intelligent BPMN assistance
3. **Database Layer:** IONOS-hosted PHP backend for user authentication and persistent data storage

This report provides a detailed technical analysis of the system architecture, component interactions, data flows, and integration patterns.

---

## Table of Contents

1. [System Architecture Overview](#1-system-architecture-overview)
2. [Frontend Architecture (Unity)](#2-frontend-architecture-unity)
3. [Backend Architecture (FastAPI + IONOS)](#3-backend-architecture-fastapi--ionos)
4. [Function Call Chains](#4-function-call-chains)
5. [Data Flow Analysis](#5-data-flow-analysis)
6. [LLM Integration Pipeline](#6-llm-integration-pipeline)
7. [Security Framework](#7-security-framework)
8. [Network Communication](#8-network-communication)
9. [Critical Code Paths](#9-critical-code-paths)
10. [Deployment Architecture](#10-deployment-architecture)

---

## 1. System Architecture Overview

### 1.1 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     UNITY CLIENT (Frontend)                      │
│                    Unity 2020.2.1f1 / C#                         │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ Login Scene  │  │  Menu Scene  │  │  BPMN Scene  │          │
│  │ (Auth UI)    │→ │ (Dashboard)  │→ │ (3D Editor)  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                           ↓                    ↓                 │
│  ┌──────────────────────────────────────────────────────┐       │
│  │         Core Components                               │       │
│  │  • DiagramHandler - Data loading/management          │       │
│  │  • SaveHandler - Persistence operations              │       │
│  │  • LoadElements - BPMN rendering                     │       │
│  │  • BPMNSecurityAnalyzer - Claude integration         │       │
│  └──────────────────────────────────────────────────────┘       │
└─────────────────┬────────────────────────────┬──────────────────┘
                  │                             │
        HTTP/HTTPS (WWW)          HTTP/HTTPS (UnityWebRequest)
                  ↓                             ↓
    ┌─────────────────────────┐   ┌────────────────────────────┐
    │  IONOS PHP Backend      │   │  FastAPI AI Backend        │
    │  (cyberd3sign.com)      │   │  (Port 8000 - Docker)      │
    ├─────────────────────────┤   ├────────────────────────────┤
    │ • User Authentication   │   │ • BPMN AI Assistant        │
    │ • BPMN Storage (MySQL)  │   │ • LLM Provider Abstraction │
    │ • Security Req Storage  │   │ • Security Suggestions     │
    │ • Session Management    │   │ • Intent Classification    │
    └─────────────────────────┘   └────────────────┬───────────┘
                                                     │
                                          External LLM APIs
                                                     ↓
                        ┌────────────────────────────────────────┐
                        │ • OpenAI (GPT-4.1, o4-mini)            │
                        │ • Anthropic (Claude Sonnet/Opus 4)     │
                        │ • Google (Gemini 2.5 Flash/Pro)        │
                        │ • Fireworks AI (Llama, Qwen, Deepseek) │
                        └────────────────────────────────────────┘
```

### 1.2 Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Frontend** | Unity | 2020.2.1f1 | 3D visualization & UI |
| | C# | .NET 4.x | Application logic |
| | TextMesh Pro | Bundled | Advanced text rendering |
| **AI Backend** | Python | 3.12 | Runtime environment |
| | FastAPI | 0.115.6+ | REST API framework |
| | Anthropic SDK | 0.40.0+ | Claude integration |
| | LiteLLM | 1.66.2+ | Multi-LLM abstraction |
| | Pydantic | 2.10.3+ | Data validation |
| | Uvicorn | 0.33.0+ | ASGI server |
| **Database Backend** | PHP | 7.x+ | Legacy API layer |
| | MySQL | 5.7+ | Persistent storage |
| **Deployment** | Docker | Latest | Containerization |
| | Docker Compose | Latest | Orchestration |
| **Infrastructure** | IONOS | N/A | Web hosting |

---

## 2. Frontend Architecture (Unity)

### 2.1 Scene Hierarchy

```
CyberD3sign Unity Project
│
├── Login.unity          - User authentication
├── Menu.unity           - Main dashboard
├── BPMN.unity           - BPMN diagram editor
├── Build.unity          - Security requirements editor
├── Policy.unity         - Security policy management
├── Loading.unity        - Loading screen
├── Credits.unity        - Credits
└── About.unity          - About page
```

### 2.2 Core Script Components

#### 2.2.1 DiagramHandler.cs (889 lines)

**Location:** `Assets/Scripts/DiagramHandler.cs`

**Responsibilities:**
- Loading BPMN and Security diagrams from IONOS server
- Parsing server responses (PHP format: `field1^field2^field3~...`)
- Managing in-memory XML documents (BPMNDoc, secDoc, reqDoc)
- Pagination of diagram lists (10 items per page)
- User interface population

**Key Static Variables:**
```csharp
public static string BPMNDiagramData        // Currently loaded BPMN XML
public static string securityDiagramData    // Security diagram XML
public static string securityRequirements   // Security requirements XML
public static string BPMNFileName           // Current BPMN filename
public static string securityFileName       // Current security filename
public static XmlDocument BPMNDoc           // BPMN XML document
public static XmlDocument secDoc            // Security diagram document
public static XmlDocument reqDoc            // Requirements document
public static List<BPMNDiagram> bpmndiagramList
public static List<SecurityDiagram> secdiagramList
```

**Critical Methods:**

| Method | Purpose | Called By |
|--------|---------|-----------|
| `getDiagrams()` | Fetch BPMN diagrams from server | Menu scene |
| `SecurityDiagrams()` | Fetch security diagrams from server | Triggered after BPMN load |
| `ParseBPMN(string)` | Parse PHP response into BPMNDiagram list | getDiagrams() |
| `ParseSecDiagrams(string)` | Parse PHP response into SecurityDiagram list | SecurityDiagrams() |
| `BPMNClickHandler()` | Load selected BPMN into editor | UI button click |
| `SecurityClickHandler()` | Load security diagram + requirements | UI button click |
| `DeleteBPMNRow()` | Delete BPMN from server | Delete button |

**Server Endpoints Called:**
```
POST /database/UserMechanics/diagrams.php
POST /database/UserMechanics/securitydiagrams.php
POST /database/UserMechanics/deletebpmn.php
POST /database/UserMechanics/deletesecurityrequirements.php
```

#### 2.2.2 SaveHandler.cs (322 lines)

**Location:** `Assets/Scripts/SaveHandler.cs`

**Responsibilities:**
- Serializing BPMN/Security XML documents to strings
- Uploading diagrams to IONOS server
- Screenshot capture for diagram thumbnails
- Differentiating between new saves and updates

**Key Static Variables:**
```csharp
public static bool saveDiagram               // Trigger for BPMN save
public static bool saveSecurityDiagram       // Trigger for security save
public static string bpmnDiagram             // BPMN XML string
public static string securityDiagram         // Security XML string
public static string securityRequirements    // Requirements XML string
public static string diagramUI               // User-facing diagram name
public static List<elementSaveDetails> elementSaveDetails
public static List<sequenceFlow> sequenceFlows
```

**Critical Methods:**

| Method | Purpose | Data Sent |
|--------|---------|-----------|
| `tSaveBPMN()` | Convert BPMNDoc to XML string | Static bpmnDiagram |
| `tSaveSecurity()` | Convert secDoc to XML string | Static securityDiagram |
| `tSaveRequirements()` | Convert reqDoc to XML string | Static securityRequirements |
| `saveBPMN()` | Upload BPMN to server | diagram, uID, diagramUI, company, username |
| `saveSecurity()` | Upload security + screenshot | diagram, uID, diagramUI, BPMNID, company, username, screenshot (PNG binary) |
| `saveRequirements()` | Upload security requirements | diagram, uID, diagramUI, username |

**Screenshot Workflow:**
```csharp
// saveSecurity() - Lines 121-211
1. Store original camera position
2. Calculate center of BPMN diagram (middle element)
3. Position camera at elevation + distance from center
4. Wait for frame render (yield WaitForEndOfFrame)
5. Capture screen to Texture2D (ReadPixels)
6. Encode to PNG byte array
7. Attach to WWWForm as binary data
8. Restore original camera position
```

**Server Endpoints Called:**
```
POST /database/UserMechanics/savediagrams.php     (new BPMN)
POST /database/UserMechanics/updatediagrams.php   (existing BPMN)
POST /database/UserMechanics/savesecurity.php     (new security)
POST /database/UserMechanics/updatesecurity.php   (existing security)
POST /database/UserMechanics/saverequirements.php (security requirements)
```

#### 2.2.3 Login.cs (212 lines)

**Location:** `Assets/Scripts/Login.cs`

**Responsibilities:**
- User credential collection
- Server connection toggle (localhost vs. production)
- Session initialization via UserSession singleton
- Navigation to Menu scene on success

**Authentication Flow:**
```csharp
// login() - Lines 120-165
1. Collect username/password from InputFields
2. Create WWWForm with credentials
3. POST to /database/UserMechanics/login.php
4. If response is non-empty string → username validated
5. Store currentUser = response text
6. Load "Menu" scene
```

**Server Connection Management:**
```csharp
// ServerConnection.cs - Lines 7-9
s_localHost = "http://localhost"
s_cyberD3sign = "http://www.cyberd3sign.com"
s_cyberD3signHTTPS = "https://www.cyberd3sign.com"

// Toggle controlled by localhost_TOGGLE checkbox
UserSession.Instance.ServerConnection = localhost_TOGGLE.isOn
    ? ServerConnection.s_localHost
    : ServerConnection.s_cyberD3sign;
```

**Server Endpoint Called:**
```
POST /database/UserMechanics/login.php
  - Fields: myform_user, myform_pass
  - Success: Returns username as plain text
  - Failure: Returns empty string or error
```

#### 2.2.4 BPMNSecurityAnalyzer.cs (810 lines)

**Location:** `Assets/Scripts/BPMNSecurityAnalyzer.cs`

**Responsibilities:**
- Direct integration with Claude API (Anthropic)
- Security analysis of BPMN elements
- AI-powered security control suggestions
- Ontology path mapping

**Key Configuration:**
```csharp
[SerializeField] private string apiKey;                              // Claude API key
[SerializeField] private string apiEndpoint = "https://api.anthropic.com/v1/messages";
[SerializeField] private string claudeModel = "claude-3-opus-20240229";
```

**Critical Methods:**

| Method | Purpose | API Called |
|--------|---------|------------|
| `AnalyzeFullDiagram()` | Analyze entire BPMN for security | Anthropic Claude |
| `AnalyzeElement(string elementId)` | Analyze specific BPMN element | Anthropic Claude |
| `AnalyzeBPMNWithClaude()` | Core LLM API call | POST /v1/messages |
| `ParseClaudeResponse()` | Extract security suggestions from JSON | N/A |
| `ApplySuggestions()` | Apply AI recommendations to diagram | N/A |
| `ApplySecurityToElement()` | Update secDoc with security category | N/A |

**LLM Prompt Structure (Lines 215-263):**
```
You are an expert in BPMN security analysis.
Focus on analyzing the BPMN element with ID: {elementId}

Security Categories to consider:
1. accesscontrol - Authentication, identification, authorization
2. privacy - User consent, confidentiality
3. integrity - Data, hardware, personnel, and software integrity
4. accountability - Non-repudiation, audit trails
5. attackharm - Vulnerability assessment, firewalls, intrusion detection
6. availability - Backups, redundancy, uptime requirements

Here's the BPMN XML to analyze:
```xml
{bpmnXml}
```

Format your response as JSON:
{
  "elementId1": {
    "explanation": "This element handles sensitive data.",
    "suggestedControls": ["accesscontrol", "privacy.confidentiality"]
  }
}
```

**Response Parsing (Lines 266-351):**
- Extracts JSON from Claude response
- Parses nested structure (element → explanation + suggested controls)
- Handles fallback to text-based extraction if JSON parsing fails
- Returns `Dictionary<string, List<string>>`

**Security Application (Lines 672-742):**
```csharp
// Creates/updates security XML structure
<root>
  <bpmnElement elementID="task1" elementText="Send Email">
    <accesscontrol required="true"/>
    <privacy required="false"/>
    <integrity required="false"/>
    <accountability required="false"/>
    <attackharm required="false"/>
    <availability required="false"/>
  </bpmnElement>
</root>
```

### 2.3 Data Models

#### BPMNDiagram Class
```csharp
public class BPMNDiagram
{
    public string _name;          // Diagram filename
    public string _data;          // BPMN XML content
    public string _lastEdited;    // Timestamp (YYYY-MM-DD HH:MM)
    public string _lastUser;      // Username
}
```

#### SecurityDiagram Class
```csharp
public class SecurityDiagram
{
    public string _name;          // Security diagram filename
    public string _data;          // Security diagram XML
    public string _requirements;  // Requirements XML
    public string _bpmn;          // Associated BPMN filename
    public string _lastEdited;    // Timestamp
    public string _lastUser;      // Username
}
```

#### elementSaveDetails Class
```csharp
public class elementSaveDetails
{
    public string id;             // Element ID
    public string type;           // task, gateway, event, etc.
    public Vector3 position;      // 3D position
    public string text;           // Label text
    // Additional BPMN properties
}
```

---

## 3. Backend Architecture (FastAPI + IONOS)

### 3.1 FastAPI Server Architecture

**Location:** `backend_server_IONOS/bpmn_assistant_cyber3d-main/src/bpmn_assistant/app.py`

#### 3.1.1 API Endpoints

| Endpoint | Method | Purpose | Request Model | Response |
|----------|--------|---------|---------------|----------|
| `/bpmn_to_json` | POST | Convert BPMN XML to JSON | `BpmnToJsonRequest` | JSON diagram structure |
| `/available_providers` | GET | List available LLM providers | None | `{"openai": bool, "anthropic": bool, ...}` |
| `/determine_intent` | POST | Classify user intent | `DetermineIntentRequest` | `{"intent": str, "confidence": float}` |
| `/modify` | POST | Create/edit BPMN diagram | `ModifyBpmnRequest` | `{"bpmn_xml": str, "bpmn_json": dict}` |
| `/talk` | POST | Conversational response | `ConversationalRequest` | `{"message": str}` |
| `/suggest_security` | POST | AI security suggestions | `SuggestSecurityRequest` | `{"explanation": str, "security_ontologies": list}` |

#### 3.1.2 Request Models (Pydantic)

**BpmnToJsonRequest:**
```python
class BpmnToJsonRequest(BaseModel):
    bpmn_xml: str
```

**DetermineIntentRequest:**
```python
class DetermineIntentRequest(BaseModel):
    message_history: List[MessageItem]
    model: str
```

**ModifyBpmnRequest:**
```python
class ModifyBpmnRequest(BaseModel):
    message_history: List[MessageItem]
    process: Optional[List[dict]]  # Existing BPMN JSON (for edits)
    model: str
```

**SuggestSecurityRequest:**
```python
class SuggestSecurityRequest(BaseModel):
    modified_bpmn_xml: str
    model: str
    message_history: List[MessageHistoryItem] = []
```

**MessageHistoryItem:**
```python
class MessageHistoryItem(BaseModel):
    role: str    # "user" or "assistant"
    content: str # Message text
```

#### 3.1.3 Service Layer Architecture

```
app.py (API Layer)
    ↓
Services Layer
    ├── BpmnModelingService    (create_bpmn, edit_bpmn)
    ├── BpmnJsonGenerator      (XML → JSON conversion)
    ├── BpmnXmlGenerator       (JSON → XML conversion)
    ├── ConversationalService  (LLM-powered chat)
    └── determine_intent       (Intent classification)
         ↓
Core Layer
    ├── LLMFacade              (Unified LLM interface)
    ├── ProviderFactory        (Create provider instances)
    └── Provider Implementations
        ├── AnthropicProvider  (Claude SDK)
        └── LiteLLMProvider    (OpenAI, Google, Fireworks)
             ↓
External LLM APIs
```

### 3.2 IONOS PHP Backend

**Base URL:** `http://www.cyberd3sign.com` or `https://www.cyberd3sign.com`

#### 3.2.1 PHP Endpoints

| Endpoint | Method | Purpose | Request Fields | Response Format |
|----------|--------|---------|----------------|-----------------|
| `/database/UserMechanics/login.php` | POST | Authenticate user | `myform_user`, `myform_pass` | Plain text username or empty |
| `/database/UserMechanics/username.php` | POST | Get user ID | `username` | User ID string |
| `/database/UserMechanics/companyname.php` | POST | Get company name | `username` | Company name string |
| `/database/UserMechanics/diagrams.php` | POST | Fetch BPMN diagrams | `username`, `company` | `name^data^lastEdit^lastUser~...` |
| `/database/UserMechanics/securitydiagrams.php` | POST | Fetch security diagrams | `username`, `company` | `name^data^requirements^bpmn^lastEdit^lastUser~...` |
| `/database/UserMechanics/savediagrams.php` | POST | Save new BPMN | `diagram`, `uID`, `diagramUI`, `company`, `username` | Empty on success, error text on failure |
| `/database/UserMechanics/updatediagrams.php` | POST | Update existing BPMN | `diagram`, `uID`, `diagramUI`, `company`, `username` | Empty on success |
| `/database/UserMechanics/savesecurity.php` | POST | Save new security | `diagram`, `uID`, `diagramUI`, `BPMNID`, `company`, `username`, `screenshot` (binary PNG) | Empty on success |
| `/database/UserMechanics/updatesecurity.php` | POST | Update security | `diagram`, `uID`, `diagramUI`, `company`, `username`, `screenshot` | Empty on success |
| `/database/UserMechanics/saverequirements.php` | POST | Save requirements | `diagram`, `uID`, `diagramUI`, `username` | Empty on success |
| `/database/UserMechanics/deletebpmn.php` | POST | Delete BPMN | `name`, `userID` | Confirmation text |
| `/database/UserMechanics/deletesecurityrequirements.php` | POST | Delete security | `name`, `userID` | Confirmation text |

#### 3.2.2 Response Format

**Pattern:** `field1^field2^field3~field1^field2^field3~...`

- **Delimiter:** `^` separates fields within a record
- **Record Separator:** `~` separates multiple records

**BPMN Diagram Response:**
```
diagramName1^<xml>BPMN data</xml>^2024-10-15 14:30^john.doe~
diagramName2^<xml>BPMN data</xml>^2024-10-14 09:15^jane.smith~
```

**Security Diagram Response:**
```
securityName1^<xml>securityData</xml>^<xml>requirements</xml>^bpmnName1^2024-10-15 16:45^john.doe~
```

#### 3.2.3 Database Schema (Inferred)

**Users Table:**
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    company VARCHAR(255),
    created_at TIMESTAMP
);
```

**BPMN Diagrams Table:**
```sql
CREATE TABLE bpmn_diagrams (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    company VARCHAR(255),
    diagram_name VARCHAR(255),
    diagram_xml LONGTEXT,
    last_edited TIMESTAMP,
    last_user VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Security Diagrams Table:**
```sql
CREATE TABLE security_diagrams (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    company VARCHAR(255),
    security_name VARCHAR(255),
    security_xml LONGTEXT,
    requirements_xml LONGTEXT,
    bpmn_name VARCHAR(255),
    screenshot BLOB,
    last_edited TIMESTAMP,
    last_user VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## 4. Function Call Chains

### 4.1 User Login Flow

```
User enters credentials in Login.unity
    ↓
Login.cs :: LoginWrapper()
    ↓
Login.cs :: login() [Coroutine]
    ↓
WWWForm created with myform_user + myform_pass
    ↓
HTTP POST → UserSession.Instance.ServerConnection.BaseURL + "/database/UserMechanics/login.php"
    ↓
IONOS PHP: Validate credentials against MySQL database
    ↓
Response: Username string (success) or empty (failure)
    ↓
Login.cs :: if (!string.IsNullOrEmpty(formText))
    ↓
Login.currentUser = formText
    ↓
SceneManager.LoadScene("Menu")
    ↓
Menu scene loaded → DiagramHandler.getDiagrams() triggered
```

### 4.2 Loading BPMN Diagrams Flow

```
Menu.unity :: User clicks "Load BPMN"
    ↓
DiagramHandler.cs :: getDiagrams() [Coroutine]
    ↓
WWWForm with username + company
    ↓
HTTP POST → BaseURL + "/database/UserMechanics/diagrams.php"
    ↓
IONOS PHP: SELECT * FROM bpmn_diagrams WHERE company = ? AND user_id = ?
    ↓
Response: "name1^xmlData1^2024-10-15 14:30^john.doe~name2^xmlData2^..."
    ↓
DiagramHandler.cs :: ParseBPMN(string PHPReturn)
    ↓
Split by '~' → foreach entry
    ↓
Split by '^' → temp[0]=name, temp[1]=data, temp[2]=date, temp[3]=user
    ↓
bpmndiagramList.Add(new BPMNDiagram(temp[0], temp[1], temp[2], temp[3]))
    ↓
DiagramHandler.cs :: StartCoroutine(SecurityDiagrams())
    ↓
WWWForm with username + company
    ↓
HTTP POST → BaseURL + "/database/UserMechanics/securitydiagrams.php"
    ↓
IONOS PHP: SELECT * FROM security_diagrams WHERE company = ? AND user_id = ?
    ↓
Response: "name1^secXml^reqXml^bpmnName^date^user~..."
    ↓
DiagramHandler.cs :: ParseSecDiagrams(string PHPReturn)
    ↓
secdiagramList.Add(new SecurityDiagram(...))
    ↓
DiagramHandler.cs :: DisplayBPMNDiagrams() or DisplaySecurityDiagrams()
    ↓
UI populated with diagram names, last edit dates, and last users
```

### 4.3 Opening BPMN Diagram for Editing

```
User clicks BPMN diagram button in Menu
    ↓
DiagramHandler.cs :: BPMNClickHandler()
    ↓
EventSystem.current.currentSelectedGameObject.name → button index
    ↓
Find matching diagram in bpmndiagramList by name
    ↓
DiagramHandler.BPMNDiagramData = bpmndiagramList[i]._data
DiagramHandler.BPMNFileName = bpmndiagramList[i]._name
    ↓
DiagramHandler.BPMNDoc.LoadXml(BPMNDiagramData)
    ↓
SaveHandler.elementSaveDetails.Clear()
SaveHandler.sequenceFlows.Clear()
    ↓
SceneManager.LoadScene("BPMN")
    ↓
BPMN.unity loaded
    ↓
LoadElements.cs :: Start() or Awake()
    ↓
LoadElements.cs :: Reads DiagramHandler.BPMNDoc
    ↓
Parse XML → Extract BPMNShape elements
    ↓
foreach BPMNShape:
    InstantiateBPMNElement(id, type, position, text)
    ↓
    GameObject.Instantiate(taskPrefab, position, rotation)
    ↓
    bpmnShapes.Add(new BPMNShape(...))
    ↓
DrawElements.cs :: DrawSequenceFlows()
    ↓
Render 3D connections between elements using LineRenderer
```

### 4.4 Saving BPMN Diagram

```
User clicks "Save" in BPMN.unity
    ↓
HUD.cs or SaveButton.cs :: OnSaveButtonClick()
    ↓
SaveHandler.tSaveBPMN()
    ↓
SaveHandler.bpmnDiagram = GetXMLAsString(DiagramHandler.BPMNDoc)
    ↓
SaveHandler.diagramUI = userInputFileName
    ↓
SaveHandler.saveDiagram = true
    ↓
SaveHandler.cs :: LateUpdate() detects saveDiagram == true
    ↓
SaveHandler.cs :: StartCoroutine(saveBPMN())
    ↓
Check if diagram exists in DiagramHandler.bpmndiagramList
    ↓
if NEW:
    WWWForm with: diagram, uID, diagramUI, company, username
    HTTP POST → BaseURL + "/database/UserMechanics/savediagrams.php"
else EXISTING:
    WWWForm with: diagram, uID, diagramUI, company, username
    HTTP POST → BaseURL + "/database/UserMechanics/updatediagrams.php"
    ↓
IONOS PHP: INSERT or UPDATE in bpmn_diagrams table
    ↓
Response: Empty string (success) or error message
    ↓
SaveHandler.saveDiagram = false
```

### 4.5 AI Security Analysis Flow (Claude Direct Integration)

```
User selects BPMN element in Build.unity
    ↓
SecurityAnalysisUI.cs :: OnAnalyzeButtonClick()
    ↓
BPMNSecurityAnalyzer.cs :: AnalyzeElement(string elementId)
    ↓
Load DiagramHandler.BPMNDiagramData as XmlDocument
    ↓
Extract element node by ID: doc.SelectSingleNode($"//BPMNShape[@id='{elementId}']")
    ↓
BPMNSecurityAnalyzer.cs :: StartCoroutine(AnalyzeBPMNWithClaude(elementXml, elementId))
    ↓
BuildClaudePrompt(bpmnXml, elementId)
    ↓
Prompt includes:
  - Security categories (accesscontrol, privacy, integrity, accountability, attackharm, availability)
  - BPMN XML snippet
  - JSON response format specification
    ↓
Create UnityWebRequest:
  URL: https://api.anthropic.com/v1/messages
  Headers: x-api-key, anthropic-version, Content-Type
  Body: {"model": "claude-3-opus-20240229", "max_tokens": 4000, "messages": [...]}
    ↓
yield return request.SendWebRequest()
    ↓
Anthropic API: Claude processes BPMN + prompt
    ↓
Response JSON:
{
  "content": [{
    "type": "text",
    "text": "{\"elementId1\": {\"explanation\": \"...\", \"suggestedControls\": [...]}}"
  }]
}
    ↓
BPMNSecurityAnalyzer.cs :: ParseClaudeResponse(responseText)
    ↓
Extract JSON from "text" field
    ↓
Parse to Dictionary<string, List<string>>:
  Key = elementId
  Value = [control1, control2, ..., "_explanation:text"]
    ↓
BPMNSecurityAnalyzer.cs :: DisplaySuggestions(securitySuggestions, elementId)
    ↓
UI populated with:
  - Element ID
  - Explanation
  - List of suggested controls
    ↓
User clicks "Apply"
    ↓
BPMNSecurityAnalyzer.cs :: ApplySuggestions()
    ↓
foreach control in suggestedControls[elementId]:
    SecurityButtonPressed.securitySymbol = control
    ApplySecurityToElement(elementId, control)
        ↓
        Update DiagramHandler.secDoc XML:
        <bpmnElement elementID="{elementId}">
          <accesscontrol required="true"/>
          <privacy required="false"/>
          ...
        </bpmnElement>
```

### 4.6 AI BPMN Creation Flow (FastAPI Backend)

**Note:** This flow is for the FastAPI backend integration (not currently visible in Unity frontend, but architecture exists)

```
User enters text: "Create a BPMN for user registration process"
    ↓
Unity → HTTP POST to FastAPI: /determine_intent
    Body: {
      "message_history": [{"role": "user", "content": "Create a BPMN..."}],
      "model": "claude-sonnet-4-20250514"
    }
    ↓
FastAPI app.py :: _determine_intent(request)
    ↓
utils.get_llm_facade(request.model)
    ↓
LLMFacade initialized:
  - Detect provider from model string
  - Load API key from environment
  - Create provider instance (AnthropicProvider or LiteLLMProvider)
    ↓
services.determine_intent(llm_facade, message_history)
    ↓
LLM prompt: "Classify user intent: modify, suggest_security, or talk"
    ↓
LLM Response: {"intent": "modify", "confidence": 0.95}
    ↓
Unity receives: {"intent": "modify", "confidence": 0.95}
    ↓
Unity → HTTP POST to FastAPI: /modify
    Body: {
      "message_history": [{"role": "user", "content": "Create a BPMN..."}],
      "process": null,
      "model": "claude-sonnet-4-20250514"
    }
    ↓
FastAPI app.py :: _modify(request)
    ↓
BpmnModelingService.create_bpmn(llm_facade, message_history)
    ↓
PromptTemplateProcessor.render_template("create_bpmn.jinja2", message_history)
    ↓
Prompt sent to LLM:
  "Create a BPMN process in JSON format based on user request..."
    ↓
llm_facade.call(prompt, max_tokens=3000)
    ↓
LLMProvider.call(model, messages, max_tokens, temperature)
    ↓
if Provider == ANTHROPIC:
    anthropic_provider.py :: call()
    ↓
    anthropic.messages.create(
      model="claude-sonnet-4-20250514",
      max_tokens=3000,
      messages=[...],
      response_format={"type": "json_object"}  # JSON mode
    )
    ↓
    Claude API returns JSON:
    {
      "process": [
        {"type": "startEvent", "id": "start1", "text": "Start"},
        {"type": "task", "id": "task1", "text": "Register User"},
        {"type": "endEvent", "id": "end1", "text": "End"},
        ...
      ]
    }
else if Provider == OPENAI/GOOGLE/FIREWORKS:
    litellm_provider.py :: call()
    ↓
    litellm.completion(
      model=model,
      messages=[...],
      response_format={"type": "json_object"}
    )
    ↓
validate_bpmn(process)  # Ensure process structure is valid
    ↓
BpmnXmlGenerator.create_bpmn_xml(process)
    ↓
Convert JSON to BPMN XML:
    <definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL">
      <process id="process1">
        <startEvent id="start1" name="Start"/>
        <task id="task1" name="Register User"/>
        <endEvent id="end1" name="End"/>
        <sequenceFlow sourceRef="start1" targetRef="task1"/>
        <sequenceFlow sourceRef="task1" targetRef="end1"/>
      </process>
    </definitions>
    ↓
FastAPI Response:
    {
      "bpmn_xml": "<definitions>...</definitions>",
      "bpmn_json": [...]
    }
    ↓
Unity receives BPMN XML
    ↓
DiagramHandler.BPMNDoc.LoadXml(bpmn_xml)
    ↓
LoadElements.cs renders 3D BPMN diagram
```

### 4.7 Security Suggestions Flow (FastAPI Backend)

```
User has modified BPMN diagram
    ↓
Unity → HTTP POST to FastAPI: /suggest_security
    Body: {
      "modified_bpmn_xml": "<definitions>...</definitions>",
      "model": "claude-sonnet-4-20250514",
      "message_history": [...]
    }
    ↓
FastAPI app.py :: suggest_security(request)
    ↓
Parse ontology_template.xml
    ↓
extract_paths_from_xml(ontology_root)
    ↓
Available ontologies:
    [
      "root/bpmnElement/accesscontrol/authentication/personal",
      "root/bpmnElement/privacy/confidentiality/encryption",
      ...
    ]
    ↓
Build LLM prompt:
    "You are a BPMN security assistant.
     Here is the BPMN XML: {modified_bpmn_xml}
     Available ontology paths: {available_ontologies}
     Return JSON: {explanation: str, security_ontologies: [{elementID, elementText, ontology_path}]}"
    ↓
utils.send_prompt_to_llm(llm_facade, prompt)
    ↓
LLM processes BPMN + ontologies
    ↓
Response:
    {
      "explanation": "The BPMN requires authentication for user tasks...",
      "security_ontologies": [
        {
          "elementID": "task1",
          "elementText": "Login User",
          "ontology_path": ["root/bpmnElement/accesscontrol/authentication"]
        },
        {
          "elementID": "task2",
          "elementText": "Store Data",
          "ontology_path": ["root/bpmnElement/integrity/dataintegrity/hashfunction"]
        }
      ]
    }
    ↓
FastAPI returns:
    {
      "explanation": "...",
      "security_ontologies": [...],
      "suggestions": [...],
      "modification_log": [...]
    }
    ↓
Unity receives suggestions
    ↓
SecurityRequirementsManager.cs :: ParseSecuritySuggestions(response)
    ↓
foreach ontology in security_ontologies:
    Find element in DiagramHandler.reqDoc by elementID
    ↓
    if exists:
        Set ontology path as "required=true"
    else:
        Create new bpmnElement node with ontology mappings
    ↓
DiagramHandler.reqDoc updated with security requirements
```

---

## 5. Data Flow Analysis

### 5.1 BPMN Diagram Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                       Data Source                                │
├─────────────────────────────────────────────────────────────────┤
│ IONOS MySQL Database                                             │
│ - Table: bpmn_diagrams                                           │
│ - Columns: id, user_id, company, diagram_name, diagram_xml,     │
│            last_edited, last_user                                │
└────────────────┬────────────────────────────────────────────────┘
                 │
         PHP API (diagrams.php)
                 │
         Response: "name^xmlData^date^user~..."
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Unity In-Memory Storage                       │
├─────────────────────────────────────────────────────────────────┤
│ DiagramHandler.bpmndiagramList (List<BPMNDiagram>)              │
│   ├─ _name: "Process1"                                           │
│   ├─ _data: "<definitions>...</definitions>"                    │
│   ├─ _lastEdited: "2024-10-15 14:30"                            │
│   └─ _lastUser: "john.doe"                                       │
│                                                                  │
│ DiagramHandler.BPMNDiagramData (static string)                  │
│   └─ Currently selected BPMN XML                                │
│                                                                  │
│ DiagramHandler.BPMNDoc (static XmlDocument)                     │
│   └─ Parsed XML document for editing                            │
└────────────────┬────────────────────────────────────────────────┘
                 │
         User selects diagram
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    BPMN Scene Rendering                          │
├─────────────────────────────────────────────────────────────────┤
│ LoadElements.cs                                                  │
│   ├─ Parse BPMNDoc XML                                           │
│   ├─ Extract: BPMNShape, BPMNEdge elements                       │
│   └─ Instantiate 3D GameObjects                                 │
│        ├─ Task prefabs                                           │
│        ├─ Gateway prefabs                                        │
│        ├─ Event prefabs                                          │
│        └─ SequenceFlow LineRenderers                             │
│                                                                  │
│ SaveHandler.elementSaveDetails (List<elementSaveDetails>)       │
│   └─ Tracks all active BPMN elements                            │
│                                                                  │
│ SaveHandler.sequenceFlows (List<sequenceFlow>)                  │
│   └─ Tracks all connections                                     │
└────────────────┬────────────────────────────────────────────────┘
                 │
         User edits diagram (add/delete/move elements)
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Save Process                                  │
├─────────────────────────────────────────────────────────────────┤
│ SaveHandler.tSaveBPMN()                                          │
│   ├─ Iterate elementSaveDetails + sequenceFlows                 │
│   ├─ Rebuild BPMNDoc XML from current state                     │
│   └─ Convert to string: SaveHandler.bpmnDiagram                 │
│                                                                  │
│ SaveHandler.saveBPMN() [Coroutine]                              │
│   ├─ WWWForm with diagram XML + metadata                        │
│   └─ POST to IONOS PHP (savediagrams.php or updatediagrams.php) │
└────────────────┬────────────────────────────────────────────────┘
                 │
         HTTP POST
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Persistence Layer                             │
├─────────────────────────────────────────────────────────────────┤
│ IONOS PHP Backend                                                │
│   ├─ Validate user session                                       │
│   ├─ if NEW: INSERT INTO bpmn_diagrams                          │
│   └─ if UPDATE: UPDATE bpmn_diagrams SET diagram_xml = ...      │
│                                                                  │
│ MySQL Database                                                   │
│   └─ BPMN XML stored as LONGTEXT                                │
└──────────────────────────────────────────────────────────────────┘
```

### 5.2 Security Requirements Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                   Security Ontology Template                     │
├─────────────────────────────────────────────────────────────────┤
│ File: ontology_template.xml (FastAPI backend)                   │
│ Structure:                                                       │
│   root                                                           │
│     └─ bpmnElement                                               │
│         ├─ accesscontrol                                         │
│         │   ├─ authentication                                    │
│         │   │   ├─ personal                                      │
│         │   │   ├─ network                                       │
│         │   │   └─ biometric                                     │
│         │   └─ authorization                                     │
│         ├─ privacy                                               │
│         │   ├─ userconsent                                       │
│         │   └─ confidentiality                                   │
│         │       ├─ encryption                                    │
│         │       └─ keymanagement                                 │
│         ├─ integrity                                             │
│         ├─ accountability                                        │
│         ├─ attackharm                                            │
│         └─ availability                                          │
└────────────────┬────────────────────────────────────────────────┘
                 │
         User requests security analysis
                 │
         Unity → FastAPI /suggest_security
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    LLM Security Analysis                         │
├─────────────────────────────────────────────────────────────────┤
│ FastAPI suggest_security()                                       │
│   ├─ Extract ontology paths                                     │
│   ├─ Build prompt with BPMN XML + available ontologies          │
│   └─ LLM (Claude/GPT) analyzes BPMN elements                    │
│                                                                  │
│ LLM Response:                                                    │
│   {                                                              │
│     "explanation": "Login task requires authentication...",     │
│     "security_ontologies": [                                     │
│       {                                                          │
│         "elementID": "task1",                                    │
│         "elementText": "User Login",                             │
│         "ontology_path": [                                       │
│           "root/bpmnElement/accesscontrol/authentication"       │
│         ]                                                        │
│       }                                                          │
│     ]                                                            │
│   }                                                              │
└────────────────┬────────────────────────────────────────────────┘
                 │
         FastAPI → Unity JSON response
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                Unity Security Requirements                       │
├─────────────────────────────────────────────────────────────────┤
│ DiagramHandler.reqDoc (XmlDocument)                              │
│   <root>                                                         │
│     <bpmnElement elementID="task1" elementText="User Login">    │
│       <accesscontrol>                                            │
│         <authentication>                                         │
│           <personal required="true"/>                            │
│           <network required="false"/>                            │
│         </authentication>                                        │
│       </accesscontrol>                                           │
│       <privacy>                                                  │
│         <confidentiality>                                        │
│           <encryption required="true"/>                          │
│         </confidentiality>                                       │
│       </privacy>                                                 │
│     </bpmnElement>                                               │
│   </root>                                                        │
│                                                                  │
│ DiagramHandler.securityRequirements (static string)             │
│   └─ XML string version of reqDoc                               │
└────────────────┬────────────────────────────────────────────────┘
                 │
         User saves security requirements
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Save to Database                              │
├─────────────────────────────────────────────────────────────────┤
│ SaveHandler.tSaveRequirements()                                  │
│   └─ Convert reqDoc to string                                   │
│                                                                  │
│ SaveHandler.saveRequirements() [Coroutine]                      │
│   ├─ WWWForm with requirements XML                              │
│   └─ POST to IONOS PHP (saverequirements.php)                   │
│                                                                  │
│ IONOS Database                                                   │
│   └─ security_diagrams.requirements_xml = LONGTEXT              │
└──────────────────────────────────────────────────────────────────┘
```

### 5.3 User Session State Management

```
┌─────────────────────────────────────────────────────────────────┐
│                    Application Startup                           │
├─────────────────────────────────────────────────────────────────┤
│ Login.unity scene loads                                          │
│   ↓                                                              │
│ UserSession.cs (Singleton)                                       │
│   - Persists across scenes (DontDestroyOnLoad)                  │
│   - Stores ServerConnection object                              │
│   ↓                                                              │
│ ServerConnection.cs                                              │
│   - s_localHost: "http://localhost"                             │
│   - s_cyberD3sign: "http://www.cyberd3sign.com"                 │
│   - s_cyberD3signHTTPS: "https://www.cyberd3sign.com"           │
└────────────────┬────────────────────────────────────────────────┘
                 │
         User logs in
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Session Initialization                        │
├─────────────────────────────────────────────────────────────────┤
│ Login.cs :: login() successful                                   │
│   ↓                                                              │
│ Login.currentUser = "john.doe" (static string)                  │
│   ↓                                                              │
│ Menu scene loads                                                 │
│   ↓                                                              │
│ Menu.cs :: Start()                                               │
│   - Fetch user ID from server                                   │
│   - Fetch company name                                           │
│   ↓                                                              │
│ Menu.userID = "12345" (static string)                           │
│ Menu.companyName = "Acme Corp" (static string)                  │
└────────────────┬────────────────────────────────────────────────┘
                 │
         All subsequent API calls include:
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Request Context                               │
├─────────────────────────────────────────────────────────────────┤
│ WWWForm data:                                                    │
│   - username: Menu.userID                                        │
│   - company: Menu.companyName                                    │
│   - username (display): Login.currentUser                        │
│                                                                  │
│ Server URL:                                                      │
│   - UserSession.Instance.ServerConnection.BaseURL                │
│                                                                  │
│ Used by:                                                         │
│   - DiagramHandler (load diagrams)                               │
│   - SaveHandler (save diagrams)                                  │
│   - All IONOS PHP API calls                                      │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. LLM Integration Pipeline

### 6.1 Multi-Provider Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend Request                              │
├─────────────────────────────────────────────────────────────────┤
│ Unity → FastAPI: /modify or /suggest_security or /talk          │
│   Body: {                                                        │
│     "model": "claude-sonnet-4-20250514",                         │
│     "message_history": [...],                                    │
│     "process": {...}  (optional)                                 │
│   }                                                              │
└────────────────┬────────────────────────────────────────────────┘
                 │
         FastAPI app.py
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                Provider Detection Layer                          │
├─────────────────────────────────────────────────────────────────┤
│ utils.get_llm_facade(model, output_mode)                         │
│   ↓                                                              │
│ Model string analysis:                                           │
│   - "gpt-4.1" → Provider.OPENAI                                  │
│   - "claude-*" → Provider.ANTHROPIC                              │
│   - "gemini-*" → Provider.GOOGLE                                 │
│   - "llama-*" or "qwen-*" → Provider.FIREWORKS_AI                │
│   ↓                                                              │
│ Load API key from .env:                                          │
│   - OPENAI_API_KEY                                               │
│   - ANTHROPIC_API_KEY                                            │
│   - GEMINI_API_KEY                                               │
│   - FIREWORKS_AI_API_KEY                                         │
│   ↓                                                              │
│ Return: LLMFacade(provider, api_key, model, output_mode)        │
└────────────────┬────────────────────────────────────────────────┘
                 │
         LLMFacade initialization
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                LLMFacade (Unified Interface)                     │
├─────────────────────────────────────────────────────────────────┤
│ llm_facade.py                                                    │
│   ↓                                                              │
│ __init__(provider, api_key, model, output_mode)                 │
│   ↓                                                              │
│ ProviderFactory.get_provider(provider, api_key, output_mode)    │
│   ↓                                                              │
│ self.provider = AnthropicProvider or LiteLLMProvider            │
│ self.model = model string                                       │
│ self.output_mode = OutputMode.JSON or OutputMode.TEXT           │
│ self.messages = [] (conversation history)                       │
└────────────────┬────────────────────────────────────────────────┘
                 │
         Service layer calls llm_facade.call(prompt)
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                Provider-Specific Implementations                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │          AnthropicProvider (Claude)                         │ │
│ ├────────────────────────────────────────────────────────────┤ │
│ │ anthropic_provider.py                                       │ │
│ │   ↓                                                         │ │
│ │ import anthropic                                            │ │
│ │ client = anthropic.Anthropic(api_key=api_key)              │ │
│ │   ↓                                                         │ │
│ │ call(model, messages, max_tokens, temperature):            │ │
│ │   if output_mode == JSON:                                  │ │
│ │     response = client.messages.create(                     │ │
│ │       model=model,                                          │ │
│ │       max_tokens=max_tokens,                                │ │
│ │       temperature=temperature,                              │ │
│ │       messages=messages,                                    │ │
│ │       response_format={"type": "json_object"}              │ │
│ │     )                                                       │ │
│ │     return json.loads(response.content[0].text)            │ │
│ │   else (TEXT mode):                                         │ │
│ │     return response.content[0].text                        │ │
│ └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│ ┌────────────────────────────────────────────────────────────┐ │
│ │     LiteLLMProvider (OpenAI, Google, Fireworks)            │ │
│ ├────────────────────────────────────────────────────────────┤ │
│ │ litellm_provider.py                                         │ │
│ │   ↓                                                         │ │
│ │ import litellm                                              │ │
│ │ litellm.api_key = api_key                                  │ │
│ │   ↓                                                         │ │
│ │ call(model, messages, max_tokens, temperature):            │ │
│ │   if output_mode == JSON:                                  │ │
│ │     response = litellm.completion(                         │ │
│ │       model=model,                                          │ │
│ │       messages=messages,                                    │ │
│ │       max_tokens=max_tokens,                                │ │
│ │       temperature=temperature,                              │ │
│ │       response_format={"type": "json_object"}              │ │
│ │     )                                                       │ │
│ │     return json.loads(response.choices[0].message.content) │ │
│ │   else:                                                     │ │
│ │     return response.choices[0].message.content             │ │
│ │                                                             │ │
│ │ Supported models:                                           │ │
│ │   - gpt-4.1, gpt-4.1-mini, o4-mini (OpenAI)                │ │
│ │   - gemini-2.5-flash, gemini-2.5-pro (Google)              │ │
│ │   - llama-4-maverick, qwen-3-235b, deepseek-r1 (Fireworks) │ │
│ └────────────────────────────────────────────────────────────┘ │
└────────────────┬────────────────────────────────────────────────┘
                 │
         API response
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                Response Processing                               │
├─────────────────────────────────────────────────────────────────┤
│ if OutputMode.JSON:                                              │
│   - Provider returns Python dict                                │
│   - Validated against expected schema                           │
│   - Converted to JSON string for message history                │
│                                                                  │
│ if OutputMode.TEXT:                                              │
│   - Provider returns plain string                               │
│   - Used for conversational responses                           │
│                                                                  │
│ Message appended to llm_facade.messages:                        │
│   {"role": "assistant", "content": response}                    │
└────────────────┬────────────────────────────────────────────────┘
                 │
         Return to FastAPI endpoint
                 ↓
┌─────────────────────────────────────────────────────────────────┐
│                FastAPI Response                                  │
├─────────────────────────────────────────────────────────────────┤
│ /modify → {"bpmn_xml": str, "bpmn_json": dict}                  │
│ /suggest_security → {"explanation": str, "security_ontologies": │
│ /talk → {"message": str}                                         │
│ /determine_intent → {"intent": str, "confidence": float}         │
└────────────────┬────────────────────────────────────────────────┘
                 │
         Unity receives JSON response
                 ↓
         Application logic continues
```

### 6.2 LLM Prompt Templates

#### Create BPMN Prompt (create_bpmn.jinja2)

```jinja2
You are an expert in BPMN (Business Process Model and Notation).
The user wants to create a BPMN process.

Conversation history:
{{ message_history }}

Generate a BPMN process in JSON format with this structure:
{
  "process": [
    {
      "type": "startEvent",
      "id": "start1",
      "text": "Start",
      "x": 100,
      "y": 100
    },
    {
      "type": "task",
      "id": "task1",
      "text": "Task Name",
      "x": 250,
      "y": 100
    },
    {
      "type": "sequenceFlow",
      "id": "flow1",
      "sourceRef": "start1",
      "targetRef": "task1"
    },
    ...
  ]
}

Available element types:
- startEvent, endEvent, intermediateEvent
- task, userTask, serviceTask, sendTask, receiveTask
- exclusiveGateway, parallelGateway, inclusiveGateway, eventBasedGateway
- sequenceFlow

Return ONLY the JSON object, no additional text.
```

#### Determine Intent Prompt

```python
# app.py lines 90-106
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
```

#### Security Suggestion Prompt

```python
# app.py lines 189-216
prompt = f"""
You are a BPMN security assistant.

Here is the previous conversation context:
{history_text}

The user provided this BPMN XML:
{request.modified_bpmn_xml}

These are the available ontology paths:
{available_ontologies}

First, provide a **short, brief and succinct explanation** of which parts of the BPMN need what kinds of security ontologies and why.
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
```

### 6.3 Output Modes

| Mode | Value | Purpose | Provider Handling |
|------|-------|---------|-------------------|
| JSON | `OutputMode.JSON` | Structured data (BPMN processes, security suggestions) | `response_format={"type": "json_object"}` |
| TEXT | `OutputMode.TEXT` | Natural language responses (chat, explanations) | Standard text completion |

**JSON Mode Enforcement:**
- Anthropic: Uses `response_format` parameter
- OpenAI/Google/Fireworks (via LiteLLM): Uses `response_format` parameter
- Fallback: If provider doesn't support JSON mode, prompt engineering enforces JSON output

### 6.4 Reasoning Model Replacement

```python
# utils.py lines 75-86
def replace_reasoning_model(model: str) -> str:
    """
    Replaces reasoning models with more lightweight models.
    Reasoning models (o4-mini, deepseek-r1, qwen-3) don't support JSON mode.
    """
    if model == OpenAIModels.O4_MINI.value:
        return OpenAIModels.GPT_4_1_MINI.value
    elif model in [FireworksAIModels.DEEPSEEK_R1.value, FireworksAIModels.QWEN_3_235B.value]:
        return FireworksAIModels.LLAMA_4_MAVERICK.value
    return model
```

**Reason:** Reasoning models (o4-mini, deepseek-r1) perform internal chain-of-thought which conflicts with structured JSON output mode.

---

## 7. Security Framework

### 7.1 Ontology Structure

**File:** `ontology_template.xml` (FastAPI backend)

```xml
<root>
  <bpmnElement>
    <accesscontrol>
      <authentication>
        <personal/>         <!-- Username/password -->
        <network/>          <!-- IP whitelisting -->
        <biometric/>        <!-- Fingerprint, face -->
        <cryptography/>     <!-- SSL/TLS certificates -->
      </authentication>
      <identification>
        <trustlevel/>       <!-- High/medium/low -->
      </identification>
      <authorization>
        <assetclassification/>  <!-- Public, confidential, secret -->
      </authorization>
    </accesscontrol>

    <privacy>
      <userconsent>
        <anonymity/>
        <pseudonymity/>
      </userconsent>
      <datausage/>
      <confidentiality>
        <encryption/>
        <keymanagement/>
        <dataretention/>
        <pki/>              <!-- Public Key Infrastructure -->
      </confidentiality>
    </privacy>

    <integrity>
      <dataintegrity>
        <hashfunction/>
        <inputvalidation/>
      </dataintegrity>
      <hardwareintegrity>
        <physicalsecurity/>
        <assetmanagement/>
      </hardwareintegrity>
      <personnelintegrity>
        <roleassignment/>
        <delegation/>
        <separationofduties/>
      </personnelintegrity>
      <softwareintegrity>
        <antivirus/>
        <patchmanagement/>
        <sandboxing/>
      </softwareintegrity>
    </integrity>

    <accountability>
      <nonrepudiation>
        <digitalsignature/>
      </nonrepudiation>
      <audittrails>
        <userid/>
        <timestamps/>
        <accesslogs/>
      </audittrails>
    </accountability>

    <attackharm>
      <vulnerabilityassessment>
        <systemvulnerability/>
        <environmentvulnerability/>
        <servicevulnerability/>
        <personnelvulnerability/>
      </vulnerabilityassessment>
      <honeypots>
        <highinteraction/>
        <lowinteraction/>
      </honeypots>
      <firewall>
        <networklayer/>
        <applicationlayer/>
      </firewall>
      <intrusiondetection>
        <stateful/>
        <signaturebased/>
        <anomalydetection/>
      </intrusiondetection>
    </attackharm>

    <availability>
      <databackup>
        <localbackup/>
        <onlinebackup/>
      </databackup>
      <servicebackup/>
      <personnelbackup/>
      <hardwarebackup/>
    </availability>
  </bpmnElement>
</root>
```

### 7.2 Security Requirement Mapping

**Process:**
1. LLM analyzes BPMN element (e.g., "User Login" task)
2. Suggests ontology paths:
   - `root/bpmnElement/accesscontrol/authentication/personal`
   - `root/bpmnElement/privacy/confidentiality/encryption`
3. Unity creates XML structure in `DiagramHandler.reqDoc`:

```xml
<root>
  <bpmnElement elementID="task_login" elementText="User Login">
    <accesscontrol>
      <authentication>
        <personal required="true"/>
        <network required="false"/>
        <biometric required="false"/>
      </authentication>
    </accesscontrol>
    <privacy>
      <confidentiality>
        <encryption required="true"/>
        <keymanagement required="false"/>
      </confidentiality>
    </privacy>
    <integrity>
      <dataintegrity>
        <inputvalidation required="true"/>
      </dataintegrity>
    </integrity>
  </bpmnElement>
</root>
```

### 7.3 Security Visualization

**Unity Build.unity Scene:**
- Each BPMN element displays security category icons
- Color-coded indicators:
  - Green: Required security controls applied
  - Yellow: Suggested but not applied
  - Red: Missing critical security requirements

**Data Binding:**
```csharp
// SecurityRequirementsManager.cs (pseudocode)
foreach (var element in bpmnElements)
{
    XmlNode reqNode = DiagramHandler.reqDoc.SelectSingleNode($"//bpmnElement[@elementID='{element.id}']");

    if (reqNode != null)
    {
        // Check accesscontrol
        bool hasAuth = reqNode.SelectSingleNode("accesscontrol/authentication/*[@required='true']") != null;
        element.SetSecurityIcon("accesscontrol", hasAuth);

        // Check privacy
        bool hasPrivacy = reqNode.SelectSingleNode("privacy/*[@required='true']") != null;
        element.SetSecurityIcon("privacy", hasPrivacy);

        // ... (repeat for all 6 categories)
    }
}
```

---

## 8. Network Communication

### 8.1 Unity → IONOS PHP Communication

**Protocol:** HTTP/HTTPS
**Method:** POST (WWWForm)
**Encoding:** application/x-www-form-urlencoded

**Example Request (saveBPMN):**
```http
POST http://www.cyberd3sign.com/database/UserMechanics/savediagrams.php HTTP/1.1
Content-Type: application/x-www-form-urlencoded

diagram=<definitions>...</definitions>&
uID=12345&
diagramUI=MyProcess&
company=AcmeCorp&
username=john.doe
```

**Response Format:**
- Success: Empty string `""`
- Error: Plain text error message

**Unity Code:**
```csharp
// SaveHandler.cs lines 69-87
WWWForm diagramform = new WWWForm();
diagramform.AddField("diagram", bpmnDiagram);
diagramform.AddField("uID", Menu.userID);
diagramform.AddField("diagramUI", diagramUI);
diagramform.AddField("company", Menu.companyName);
diagramform.AddField("username", Login.currentUser);

WWW post = new WWW(
    UserSession.Instance.ServerConnection.BaseURL + "/database/UserMechanics/savediagrams.php",
    diagramform
);
yield return post;

string postDiagrams = post.text.Trim();
if (string.IsNullOrEmpty(postDiagrams))
{
    print("Diagram posted");
}
else
{
    print("Error: " + postDiagrams);
}
```

### 8.2 Unity → FastAPI Communication

**Protocol:** HTTPS
**Method:** POST
**Content-Type:** application/json
**Authentication:** None (relying on IONOS for auth)

**Example Request (/suggest_security):**
```http
POST http://localhost:8000/suggest_security HTTP/1.1
Content-Type: application/json

{
  "modified_bpmn_xml": "<definitions>...</definitions>",
  "model": "claude-sonnet-4-20250514",
  "message_history": [
    {"role": "user", "content": "Add security to my process"}
  ]
}
```

**Response:**
```json
{
  "explanation": "The login task requires authentication and encryption.",
  "security_ontologies": [
    {
      "elementID": "task1",
      "elementText": "User Login",
      "ontology_path": ["root/bpmnElement/accesscontrol/authentication"]
    }
  ],
  "suggestions": [...],
  "modification_log": [...]
}
```

**Unity Code (UnityWebRequest):**
```csharp
// BPMNSecurityAnalyzer.cs lines 148-173
string jsonRequestBody = "{" +
    $"\"model\": \"{claudeModel}\"," +
    "\"max_tokens\": 4000," +
    "\"messages\": [" +
        "{" +
            "\"role\": \"user\"," +
            $"\"content\": {JsonStringEscape(prompt)}" +
        "}" +
    "]" +
"}";

using (UnityWebRequest request = new UnityWebRequest(apiEndpoint, "POST"))
{
    byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonRequestBody);
    request.uploadHandler = new UploadHandlerRaw(bodyRaw);
    request.downloadHandler = new DownloadHandlerBuffer();
    request.SetRequestHeader("Content-Type", "application/json");
    request.SetRequestHeader("x-api-key", apiKey);
    request.SetRequestHeader("anthropic-version", "2023-06-01");

    yield return request.SendWebRequest();

    string responseText = request.downloadHandler.text;
    // Process response...
}
```

### 8.3 FastAPI → External LLM APIs

#### Anthropic Claude

**Endpoint:** `https://api.anthropic.com/v1/messages`

**Request:**
```http
POST https://api.anthropic.com/v1/messages HTTP/1.1
Content-Type: application/json
x-api-key: sk-ant-...
anthropic-version: 2023-06-01

{
  "model": "claude-sonnet-4-20250514",
  "max_tokens": 3000,
  "temperature": 0.3,
  "messages": [
    {"role": "user", "content": "Create a BPMN for user registration..."}
  ],
  "response_format": {"type": "json_object"}
}
```

**Response:**
```json
{
  "id": "msg_01...",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "{\"process\": [...]}"
    }
  ],
  "model": "claude-sonnet-4-20250514",
  "usage": {
    "input_tokens": 245,
    "output_tokens": 512
  }
}
```

#### OpenAI (via LiteLLM)

**Endpoint:** `https://api.openai.com/v1/chat/completions`

**Request:**
```http
POST https://api.openai.com/v1/chat/completions HTTP/1.1
Content-Type: application/json
Authorization: Bearer sk-...

{
  "model": "gpt-4.1",
  "messages": [
    {"role": "user", "content": "Create a BPMN..."}
  ],
  "max_tokens": 3000,
  "temperature": 0.3,
  "response_format": {"type": "json_object"}
}
```

#### Google Gemini (via LiteLLM)

**Endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent`

#### Fireworks AI (via LiteLLM)

**Endpoint:** `https://api.fireworks.ai/inference/v1/chat/completions`

### 8.4 CORS Configuration

**FastAPI Backend (app.py lines 34-40):**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Allow all origins (Unity can connect from anywhere)
    allow_credentials=True,
    allow_methods=["*"],      # Allow all HTTP methods
    allow_headers=["*"],      # Allow all headers
)
```

**Security Note:** Production deployment should restrict `allow_origins` to specific domains.

---

## 9. Critical Code Paths

### 9.1 BPMN Creation Path (End-to-End)

```
1. Unity BPMN.unity → User clicks "AI Assistant" button
2. UI panel opens with text input
3. User types: "Create a process for online shopping checkout"
4. Submit button clicked
5. AIAssistant.cs → SendMessageToBackend()
6. HTTP POST to FastAPI /determine_intent
7. FastAPI → utils.get_llm_facade("claude-sonnet-4")
8. LLMFacade → AnthropicProvider.call()
9. Anthropic API returns: {"intent": "modify", "confidence": 0.95}
10. Unity receives intent → triggers CreateBPMN()
11. HTTP POST to FastAPI /modify (process=null for new)
12. FastAPI → BpmnModelingService.create_bpmn()
13. PromptTemplateProcessor.render_template("create_bpmn.jinja2")
14. LLMFacade.call(prompt, max_tokens=3000)
15. Claude generates BPMN JSON process array
16. FastAPI → BpmnXmlGenerator.create_bpmn_xml(process)
17. Response: {"bpmn_xml": "<definitions>...</definitions>", "bpmn_json": [...]}
18. Unity AIAssistant.cs → OnReceiveBPMN(response)
19. DiagramHandler.BPMNDoc.LoadXml(response.bpmn_xml)
20. LoadElements.cs → RenderBPMN() triggered
21. 3D BPMN elements instantiated in scene
22. User sees completed diagram
```

### 9.2 Security Analysis Path (End-to-End)

```
1. Unity Build.unity → User has loaded BPMN diagram
2. User selects element "task_login" (User Login task)
3. UI shows "Analyze Security" button
4. Button clicked → BPMNSecurityAnalyzer.AnalyzeElement("task_login")
5. Extract element XML from DiagramHandler.BPMNDoc
6. Build Claude prompt with security categories
7. UnityWebRequest POST to https://api.anthropic.com/v1/messages
8. Request body: model=claude-3-opus, messages=[{user: prompt}]
9. Claude processes BPMN element
10. Claude identifies: Login task needs authentication + encryption
11. Response: {
     "elementId": "task_login",
     "explanation": "Login requires user authentication...",
     "suggestedControls": [
       "accesscontrol.authentication.personal",
       "privacy.confidentiality.encryption"
     ]
   }
12. BPMNSecurityAnalyzer.ParseClaudeResponse(json)
13. Display suggestions in UI panel
14. User clicks "Apply" button
15. BPMNSecurityAnalyzer.ApplySuggestions()
16. foreach control: ApplySecurityToElement("task_login", control)
17. Update DiagramHandler.reqDoc:
    <bpmnElement elementID="task_login">
      <accesscontrol>
        <authentication>
          <personal required="true"/>
        </authentication>
      </accesscontrol>
      <privacy>
        <confidentiality>
          <encryption required="true"/>
        </confidentiality>
      </privacy>
    </bpmnElement>
18. UI updates to show green security icons on element
19. User clicks "Save Security Requirements"
20. SaveHandler.tSaveRequirements() → Convert reqDoc to string
21. SaveHandler.saveRequirements() coroutine
22. HTTP POST to IONOS /database/UserMechanics/saverequirements.php
23. MySQL UPDATE security_diagrams SET requirements_xml = ...
24. Response: "" (empty = success)
25. UI shows "Security requirements saved successfully"
```

### 9.3 Data Persistence Path

```
1. User modifies BPMN diagram (adds task, moves gateway)
2. Diagram state stored in:
   - SaveHandler.elementSaveDetails (all elements)
   - SaveHandler.sequenceFlows (all connections)
3. User clicks "Save" button
4. SaveHandler.tSaveBPMN() triggered
5. Iterate elementSaveDetails → rebuild XML structure
6. foreach element:
     XmlElement node = BPMNDoc.CreateElement(element.type)
     node.SetAttribute("id", element.id)
     node.SetAttribute("name", element.text)
     // ... position, type-specific attributes
7. foreach sequenceFlow:
     XmlElement flow = BPMNDoc.CreateElement("sequenceFlow")
     flow.SetAttribute("sourceRef", flow.source)
     flow.SetAttribute("targetRef", flow.target)
8. DiagramHandler.BPMNDoc = rebuilt XML document
9. SaveHandler.bpmnDiagram = BPMNDoc.OuterXml
10. SaveHandler.saveDiagram = true
11. LateUpdate() → StartCoroutine(saveBPMN())
12. Check if diagram name exists in bpmndiagramList
13. if NEW:
      WWWForm POST → /savediagrams.php
    else:
      WWWForm POST → /updatediagrams.php
14. PHP receives POST data
15. Validate user session (userID + company)
16. if NEW:
      INSERT INTO bpmn_diagrams (user_id, company, diagram_name, diagram_xml, last_edited, last_user)
      VALUES (?, ?, ?, ?, NOW(), ?)
    else:
      UPDATE bpmn_diagrams
      SET diagram_xml = ?, last_edited = NOW(), last_user = ?
      WHERE diagram_name = ? AND user_id = ? AND company = ?
17. MySQL commits transaction
18. PHP returns empty string (success)
19. Unity receives response
20. SaveHandler.saveDiagram = false
21. UI shows "Diagram saved successfully"
```

---

## 10. Deployment Architecture

### 10.1 Production Deployment Topology

```
┌──────────────────────────────────────────────────────────────────┐
│                     End Users                                     │
│                 (Desktop Application)                             │
└────────────────┬─────────────────────────────────────────────────┘
                 │
         Unity Application
                 │
                 ├──────────────────────┬────────────────────────────┐
                 │                      │                             │
         HTTPS (Port 443)       HTTP (Port 8000)           HTTPS (Port 443)
                 │                      │                             │
                 ↓                      ↓                             ↓
┌─────────────────────────┐  ┌──────────────────────┐  ┌────────────────────┐
│   IONOS Web Server      │  │  Docker Container    │  │  External LLM APIs │
│   www.cyberd3sign.com   │  │  FastAPI Backend     │  ├────────────────────┤
├─────────────────────────┤  ├──────────────────────┤  │ • Anthropic Claude │
│ • Apache/Nginx          │  │ • Python 3.12        │  │ • OpenAI GPT       │
│ • PHP 7.x               │  │ • FastAPI 0.115.6    │  │ • Google Gemini    │
│ • MySQL 5.7             │  │ • Uvicorn ASGI       │  │ • Fireworks AI     │
│                         │  │ • Port: 8000         │  └────────────────────┘
│ Endpoints:              │  │                      │
│ /database/UserMechanics/│  │ Endpoints:           │
│   - login.php           │  │ /bpmn_to_json        │
│   - diagrams.php        │  │ /determine_intent    │
│   - savediagrams.php    │  │ /modify              │
│   - securitydiagrams.php│  │ /suggest_security    │
│   - saverequirements.php│  │ /talk                │
└─────────────────────────┘  └──────────────────────┘
         ↓                            ↓
┌─────────────────────────┐  ┌──────────────────────┐
│   MySQL Database        │  │  .env Configuration   │
│   (Persistent Storage)  │  ├──────────────────────┤
├─────────────────────────┤  │ OPENAI_API_KEY=...   │
│ Tables:                 │  │ ANTHROPIC_API_KEY=...│
│ - users                 │  │ GEMINI_API_KEY=...   │
│ - bpmn_diagrams         │  │ FIREWORKS_AI_API_KEY │
│ - security_diagrams     │  └──────────────────────┘
└─────────────────────────┘
```

### 10.2 Docker Deployment (FastAPI Backend)

**Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install uv package manager (fast dependency installer)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy application code
COPY src/ ./src/
COPY ontology_template.xml ./
COPY security_ontology.xml ./

# Expose port
EXPOSE 8000

# Run FastAPI server
CMD ["uvicorn", "src.bpmn_assistant.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  bpmn_assistant:
    image: sithuyehtun/bpmn_assistant:latest
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - FIREWORKS_AI_API_KEY=${FIREWORKS_AI_API_KEY}
    volumes:
      - ./logs:/app/logs
    networks:
      - bpmn-network
    restart: unless-stopped

networks:
  bpmn-network:
    driver: bridge
```

**Deployment Commands:**
```bash
# Build Docker image
docker-compose build

# Push to Docker Hub
docker-compose push

# Deploy on IONOS server
ssh user@ionos-server
docker pull sithuyehtun/bpmn_assistant:latest
docker run -d -p 8000:8000 \
  -e OPENAI_API_KEY=... \
  -e ANTHROPIC_API_KEY=... \
  sithuyehtun/bpmn_assistant:latest
```

### 10.3 CI/CD Pipeline

**GitHub Actions Workflow (.github/workflows/ci.yml):**
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install uv
          uv sync

      - name: Run tests
        run: |
          pytest tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: Build Docker image
        run: |
          docker-compose build

      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Push to Docker Hub
        run: |
          docker-compose push
```

### 10.4 Unity Build Configuration

**Build Targets:**
- Windows 64-bit (Primary)
- macOS (Intel/Apple Silicon)
- Linux

**Build Settings:**
```
Scenes in Build:
  0. Login.unity
  1. Menu.unity
  2. BPMN.unity
  3. Build.unity
  4. Policy.unity
  5. Loading.unity
  6. Credits.unity
  7. About.unity

Player Settings:
  Company Name: CyberD3sign
  Product Name: CyberD3sign BPMN Editor
  Version: 1.0.0
  API Compatibility Level: .NET 4.x
  Scripting Backend: Mono
  Target Architectures: x86_64
```

**Post-Build:**
1. Package executable + data folder
2. Include ReadMe.txt with server connection instructions
3. Create installer (NSIS for Windows, DMG for macOS)

---

## Appendix A: Key File Locations

### Unity Frontend

| File | Path | Purpose |
|------|------|---------|
| DiagramHandler.cs | `Assets/Scripts/DiagramHandler.cs` | BPMN/Security diagram loading |
| SaveHandler.cs | `Assets/Scripts/SaveHandler.cs` | Diagram persistence |
| Login.cs | `Assets/Scripts/Login.cs` | User authentication |
| ServerConnection.cs | `Assets/Scripts/Web/ServerConnection.cs` | Server URL configuration |
| BPMNSecurityAnalyzer.cs | `Assets/Scripts/BPMNSecurityAnalyzer.cs` | Claude API integration |
| LoadElements.cs | `Assets/Scripts/LoadElements.cs` | BPMN rendering |
| DrawElements.cs | `Assets/Scripts/DrawElements.cs` | 3D element drawing |

### FastAPI Backend

| File | Path | Purpose |
|------|------|---------|
| app.py | `src/bpmn_assistant/app.py` | Main FastAPI application |
| llm_facade.py | `src/bpmn_assistant/core/llm_facade.py` | LLM abstraction layer |
| bpmn_modeling_service.py | `src/bpmn_assistant/services/bpmn_modeling_service.py` | BPMN creation/editing |
| anthropic_provider.py | `src/bpmn_assistant/core/provider_impl/anthropic_provider.py` | Claude integration |
| litellm_provider.py | `src/bpmn_assistant/core/provider_impl/litellm_provider.py` | Multi-LLM support |
| utils.py | `src/bpmn_assistant/utils/utils.py` | Utility functions |
| ontology_template.xml | `ontology_template.xml` | Security ontology |

### Configuration

| File | Path | Purpose |
|------|------|---------|
| pyproject.toml | `pyproject.toml` | Python dependencies |
| docker-compose.yml | `docker-compose.yml` | Docker orchestration |
| Dockerfile | `Dockerfile` | Container definition |
| .env.example | `.env.example` | Environment template |

---

## Appendix B: API Endpoint Reference

### IONOS PHP Endpoints

| Endpoint | Method | Parameters | Response |
|----------|--------|------------|----------|
| `/database/UserMechanics/login.php` | POST | myform_user, myform_pass | Username or empty |
| `/database/UserMechanics/diagrams.php` | POST | username, company | `name^data^date^user~...` |
| `/database/UserMechanics/securitydiagrams.php` | POST | username, company | `name^data^req^bpmn^date^user~...` |
| `/database/UserMechanics/savediagrams.php` | POST | diagram, uID, diagramUI, company, username | Empty or error |
| `/database/UserMechanics/updatediagrams.php` | POST | diagram, uID, diagramUI, company, username | Empty or error |
| `/database/UserMechanics/savesecurity.php` | POST | diagram, uID, diagramUI, BPMNID, company, username, screenshot | Empty or error |
| `/database/UserMechanics/updatesecurity.php` | POST | diagram, uID, diagramUI, company, username, screenshot | Empty or error |
| `/database/UserMechanics/saverequirements.php` | POST | diagram, uID, diagramUI, username | Empty or error |
| `/database/UserMechanics/deletebpmn.php` | POST | name, userID | Confirmation text |
| `/database/UserMechanics/deletesecurityrequirements.php` | POST | name, userID | Confirmation text |

### FastAPI Endpoints

| Endpoint | Method | Request Body | Response |
|----------|--------|--------------|----------|
| `/bpmn_to_json` | POST | `{"bpmn_xml": str}` | JSON diagram structure |
| `/available_providers` | GET | None | `{"openai": bool, "anthropic": bool, ...}` |
| `/determine_intent` | POST | `{"message_history": [...], "model": str}` | `{"intent": str, "confidence": float}` |
| `/modify` | POST | `{"message_history": [...], "process": dict, "model": str}` | `{"bpmn_xml": str, "bpmn_json": dict}` |
| `/talk` | POST | `{"message_history": [...], "process": dict, "model": str}` | `{"message": str}` |
| `/suggest_security` | POST | `{"modified_bpmn_xml": str, "model": str, "message_history": [...]}` | `{"explanation": str, "security_ontologies": [...]}` |

---

## Appendix C: Data Model Schemas

### BPMN Element JSON Schema

```json
{
  "type": "task",
  "id": "task1",
  "text": "User Login",
  "x": 250,
  "y": 150,
  "width": 120,
  "height": 80
}
```

### Security Ontology Suggestion Schema

```json
{
  "elementID": "task1",
  "elementText": "User Login",
  "ontology_path": [
    "root/bpmnElement/accesscontrol/authentication/personal"
  ]
}
```

### Security Requirements XML Schema

```xml
<root>
  <bpmnElement elementID="task1" elementText="User Login">
    <accesscontrol>
      <authentication>
        <personal required="true"/>
      </authentication>
    </accesscontrol>
    <privacy>
      <confidentiality>
        <encryption required="true"/>
      </confidentiality>
    </privacy>
  </bpmnElement>
</root>
```

---

## Document Conclusion

This technical architecture report provides a comprehensive analysis of the CyberD3sign application, covering all aspects from frontend Unity components to backend FastAPI services, LLM integrations, and database persistence. The system demonstrates a well-architected separation of concerns with clear data flow patterns and robust integration between multiple technology stacks.

**Key Architectural Strengths:**
1. Modular LLM provider abstraction enabling multi-vendor support
2. Clear separation between IONOS legacy backend and modern FastAPI AI services
3. Comprehensive security ontology framework
4. Stateless API design with client-side session management
5. Docker-based deployment for easy scaling

**Potential Improvements:**
1. Add authentication/authorization to FastAPI endpoints
2. Implement caching for LLM responses to reduce API costs
3. Add WebSocket support for real-time collaborative editing
4. Migrate IONOS PHP backend to modern REST API
5. Implement database connection pooling for better performance

For questions or clarifications about specific components, refer to the file locations in Appendix A or consult the inline code documentation.

---

**End of Report**
