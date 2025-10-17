# CyberD3sign Application
## Complete Technical Architecture Report

---

**Document Control**

| Property | Value |
|----------|-------|
| **Document Title** | CyberD3sign Complete Technical Architecture Report |
| **Version** | 2.0 |
| **Date** | October 16, 2025 |
| **Status** | Final |
| **Author** | Sithu Ye Htun|
| **Classification** | Technical Reference |

---

## Executive Summary

CyberD3sign is a sophisticated hybrid application that combines Unity 3D visualization with AI-powered business process modeling and security analysis. The system employs a three-tier architecture with a Unity C# frontend and dual-server backend infrastructure.

**Core Technologies:**
- **Frontend**: Unity 2020.2.1f1 with C# .NET 4.x scripting
- **Backend (Dual-Server Architecture)**:
  - **Server 1 - cyberd3sign.com**: PHP backend, MySQL database, user authentication, web hosting
  - **Server 2 - IONOS Cloud (217.154.116.117:8000)**: FastAPI LLM backend with stored API keys (no GPU costs)
- **AI Integration**: Multi-provider LLM support via server-side API keys (OpenAI GPT, Anthropic Claude, Google Gemini, Fireworks AI)

**Key Capabilities:**
- AI-powered BPMN diagram generation and modification
- Intent-based conversational interface for diagram creation
- Security ontology mapping with 6-category framework
- LLM-generated diagram rendering with automatic scaling
- Real-time security analysis and recommendations

---

## Table of Contents

1. [Introduction and System Overview](#1-introduction-and-system-overview)
   - 1.1 [Purpose and Scope](#11-purpose-and-scope)
   - 1.2 [System Context](#12-system-context)
   - 1.3 [Key Features](#13-key-features)

2. [System Architecture](#2-system-architecture)
   - 2.1 [High-Level Architecture](#21-high-level-architecture)
   - 2.2 [Component Diagram](#22-component-diagram)
   - 2.3 [Technology Stack](#23-technology-stack)
   - 2.4 [Design Patterns](#24-design-patterns)

3. [AI-Powered LLM Integration Layer](#3-ai-powered-llm-integration-layer)
   - 3.1 [GPTManager Component](#31-gptmanager-component)
   - 3.2 [Intent Detection System](#32-intent-detection-system)
   - 3.3 [Conversation Management](#33-conversation-management)
   - 3.4 [API Integration Architecture](#34-api-integration-architecture)

4. [Diagram Loading and Rendering System](#4-diagram-loading-and-rendering-system)
   - 4.1 [loadBPMNDiagram Component](#41-loadbpmndiagram-component)
   - 4.2 [loadLLMDiagram Component](#42-loadllmdiagram-component)
   - 4.3 [XML Processing Pipeline](#43-xml-processing-pipeline)
   - 4.4 [Dynamic Prefab Instantiation](#44-dynamic-prefab-instantiation)

5. [Unity Frontend Layer](#5-unity-frontend-layer)
   - 5.1 [DiagramHandler](#51-diagramhandler)
   - 5.2 [SaveHandler](#52-savehandler)
   - 5.3 [Login System](#53-login-system)
   - 5.4 [Security Analysis and Visualization](#54-security-analysis-and-visualization)

6. [Python FastAPI Backend (IONOS Cloud)](#6-python-fastapi-backend-ionos-cloud-server)
   - 6.1 [Backend Architecture Overview](#61-backend-architecture-overview)
   - 6.2 [BPMN Generation: How It Actually Works](#62-bpmn-generation-how-it-actually-works)
   - 6.3 [Security Analysis: How It Actually Works](#63-security-analysis-how-it-actually-works)
   - 6.4 [API Endpoints](#64-api-endpoints)
   - 6.5 [LLM Facade Pattern](#65-llm-facade-pattern)
   - 6.6 [BPMN Modeling Service](#66-bpmn-modeling-service)
   - 6.7 [Request/Response Models](#67-requestresponse-models)

7. [cyberd3sign.com PHP Backend](#7-cyberd3signcom-php-backend)
   - 7.1 [Server Architecture](#71-server-architecture)
   - 7.2 [Database Integration](#72-database-integration)
   - 7.3 [Data Persistence](#73-data-persistence)

8. [Security Framework](#8-security-framework)
   - 8.1 [Security Ontology](#81-security-ontology)
   - 8.2 [AI-Powered Security Suggestions](#82-ai-powered-security-suggestions)
   - 8.3 [Security XML Generation](#83-security-xml-generation)

9. [Data Flow and Integration](#9-data-flow-and-integration)
   - 9.1 [User Authentication Flow](#91-user-authentication-flow)
   - 9.2 [Diagram Creation Flow](#92-diagram-creation-flow)
   - 9.3 [LLM-Powered Diagram Generation Flow](#93-llm-powered-diagram-generation-flow)
   - 9.4 [Security Analysis Flow](#94-security-analysis-flow)

10. [Technical Implementation Details](#10-technical-implementation-details)
    - 10.1 [Coroutine-Based Async Operations](#101-coroutine-based-async-operations)
    - 10.2 [XML Document Processing](#102-xml-document-processing)
    - 10.3 [Scaling and Layout Algorithms](#103-scaling-and-layout-algorithms)

11. [Deployment and Infrastructure](#11-deployment-and-infrastructure)
    - 11.1 [Server Configuration](#111-server-configuration)
    - 11.2 [API Endpoints](#112-api-endpoints)
    - 11.3 [Environment Management](#113-environment-management)

Appendices
- [Appendix A: Complete Code Reference](#appendix-a-complete-code-reference)
- [Appendix B: API Documentation](#appendix-b-api-documentation)
- [Appendix C: Security Ontology Reference](#appendix-c-security-ontology-reference)
- [Appendix D: Design Pattern Catalog](#appendix-d-design-pattern-catalog)
- [Appendix E: Glossary](#appendix-e-glossary)

---

## 1. Introduction and System Overview

### 1.1 Purpose and Scope

CyberD3sign is an enterprise-grade application designed to bridge business process modeling with cybersecurity analysis through AI-powered automation. The system enables users to create, modify, and analyze Business Process Model and Notation (BPMN) diagrams while receiving intelligent security recommendations.

**Primary Objectives:**
1. Enable natural language-based BPMN diagram creation
2. Provide real-time security analysis and recommendations
3. Support multiple LLM providers for flexibility and redundancy
4. Deliver 3D visualization of business processes
5. Integrate security ontology mapping with process elements

### 1.2 System Context

The application operates in a dual-server architecture:

```
┌──────────────────────────────────────────────────────────────┐
│                      User Interface                           │
│                    (Unity 3D Client)                          │
└────────────┬──────────────────────────┬──────────────────────┘
             │                          │
             │ REST API                 │ REST API
             │ (LLM Functions)          │ (Auth/Data)
             │                          │
┌────────────▼────────────────┐  ┌──────▼─────────────────────┐
│  SERVER 1: IONOS Cloud      │  │  SERVER 2: cyberd3sign.com │
│  IP: 217.154.116.117:8000   │  │  Domain: cyberd3sign.com   │
│  ┌──────────────────────┐   │  │  ┌─────────────────────┐   │
│  │  FastAPI Backend     │   │  │  │  PHP Backend        │   │
│  │  - Intent Detection  │   │  │  │  - User Login       │   │
│  │  - BPMN Generation   │   │  │  │  - Registration     │   │
│  │  - Security Analysis │   │  │  │  - Session Mgmt     │   │
│  │  - LLM Integration   │   │  │  │  - Diagram CRUD     │   │
│  │  - API Key Storage   │   │  │  └─────────┬───────────┘   │
│  └──────────┬───────────┘   │  │            │               │
│             │               │  │  ┌─────────▼───────────┐   │
│             │ API Calls     │  │  │  MySQL Database     │   │
│             │ (using keys)  │  │  │  - Users            │   │
│  ┌──────────▼───────────┐   │  │  │  - BPMN Diagrams    │   │
│  │  External LLM APIs   │   │  │  │  - Security Data    │   │
│  │  - OpenAI GPT        │   │  │  └─────────────────────┘   │
│  │  - Anthropic Claude  │   │  │                            │
│  │  - Google Gemini     │   │  │  Apache/PHP/MySQL Stack    │
│  │  - Fireworks AI      │   │  │                            │
│  └──────────────────────┘   │  │                            │
│                              │  │                            │
│  Python 3.12 + FastAPI       │  │  Traditional Web Hosting   │
└──────────────────────────────┘  └────────────────────────────┘

**Key Architecture Benefits:**
- **Separation of Concerns**: AI processing isolated from data persistence
- **Cost Efficiency**: IONOS Cloud stores API keys, eliminating GPU rental costs
- **Security**: LLM credentials on dedicated server, never exposed to client
- **Scalability**: Independent scaling of AI and data backends
```

### 1.3 Key Features

**AI-Powered Diagram Generation:**
- Natural language processing for intent detection
- Automatic BPMN XML generation from text descriptions
- Multi-turn conversational editing and refinement
- Support for GPT-4.1-nano and other LLM models

**Security Analysis:**
- Automated security requirement mapping
- Six-category security ontology framework
- Element-level security recommendations
- Visual security overlay rendering

**Visualization:**
- 3D Unity-based rendering engine
- Dynamic prefab instantiation
- Automatic layout and scaling
- Interactive element manipulation

---

## 2. System Architecture

### 2.1 High-Level Architecture

CyberD3sign implements a three-tier architecture pattern with dual-server backend infrastructure:

**Presentation Tier (Unity Client):**
- Unity 2020.2.1f1 with C# .NET 4.x
- 3D visualization and user interaction
- Client-side state management
- XML processing and rendering
- Communicates with both backend servers

**Application Tier (Dual-Server Backend):**

**Server 1 - IONOS Cloud (217.154.116.117:8000):**
- **FastAPI Backend** (Python 3.12):
  - AI processing and LLM integration
  - Intent detection and routing
  - BPMN generation from natural language
  - Security analysis and suggestions
  - Stores LLM API keys (OpenAI, Anthropic, Google, Fireworks)
  - No GPU infrastructure needed - uses provider APIs

**Server 2 - cyberd3sign.com:**
- **PHP Backend** (Apache):
  - User authentication and authorization
  - User registration and login
  - Session management
  - Diagram CRUD operations
  - Web hosting

**Data Tier:**
- MySQL database on cyberd3sign.com
- User accounts and credentials
- BPMN diagram storage
- Security requirements data
- JSON-based data exchange between tiers
- XML document storage for diagrams

**Cost-Saving Architecture:**
The dual-server design separates AI processing from data persistence. The IONOS Cloud server stores all LLM provider API keys, allowing the application to leverage powerful AI models (GPT-4, Claude, Gemini) without requiring expensive GPU infrastructure. The server makes API calls on behalf of the Unity client, keeping credentials secure and eliminating GPU rental costs.

### 2.2 Component Diagram

```
Unity Frontend Components:
┌──────────────────────────────────────────────────────────┐
│  GPTManager.cs                                           │
│  ├── Intent Detection (determine_intent)                │
│  ├── Diagram Modification (modify)                      │
│  ├── Conversational Interface (talk)                    │
│  └── Security Suggestions (suggest_security)            │
└────────────┬─────────────────────────────────────────────┘
             │
             │ Calls
             ▼
┌──────────────────────────────────────────────────────────┐
│  loadLLMDiagram.cs / loadBPMNDiagram.cs                 │
│  ├── XML Parsing                                        │
│  ├── Prefab Instantiation                              │
│  ├── Position Scaling (0.26x factor)                   │
│  └── Arrow Rendering                                   │
└────────────┬─────────────────────────────────────────────┘
             │
             │ Uses
             ▼
┌──────────────────────────────────────────────────────────┐
│  DiagramHandler.cs                                       │
│  ├── Static Data Storage                               │
│  ├── BPMN XML Management                                │
│  └── Security Requirements Tracking                     │
└──────────────────────────────────────────────────────────┘
```

### 2.3 Technology Stack

**Frontend Technologies:**
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Game Engine | Unity | 2020.2.1f1 | 3D rendering and application framework |
| Language | C# | .NET 4.x | Application logic |
| UI Framework | Unity UI | Built-in | User interface components |
| Text Rendering | TextMeshPro | Built-in | Advanced text display |
| Networking | UnityWebRequest | Built-in | HTTP communication |

**Backend Technologies (Dual-Server):**
| Component | Technology | Version | Server | Purpose |
|-----------|-----------|---------|--------|---------|
| AI Framework | FastAPI | Latest | IONOS Cloud | LLM processing with API keys |
| Language | Python | 3.12 | IONOS Cloud | AI backend logic |
| Data Backend | PHP | 7.x+ | cyberd3sign.com | User auth and persistence |
| Database | MySQL | 5.7+ | cyberd3sign.com | Data storage |
| Web Server | Apache | 2.4+ | cyberd3sign.com | PHP hosting |
| LLM Access | API Keys | N/A | IONOS Cloud | Server-side credentials (no GPU) |

### 2.4 Design Patterns

**Facade Pattern (llm_facade.py): (IONOS SERVER SIDE)**
```python
class UnifiedLLMFacade:
    """
    Provides a unified interface to multiple LLM providers:
    - OpenAI GPT-4
    - Anthropic Claude
    - Google Gemini
    - Fireworks AI
    """
```

**Singleton Pattern (DiagramHandler.cs):**
- Static variables for global state management
- Single source of truth for BPMN data
- Shared across all Unity components

**Factory Pattern (Prefab Instantiation):**
- Dynamic GameObject creation based on element type
- Resource loading from categorized folders (Events/Tasks/Gateways)

**Repository Pattern:**
- SaveHandler for diagram persistence
- DiagramHandler for diagram retrieval

---

## 3. AI-Powered LLM Integration Layer

### 3.1 GPTManager Component (Unity Client Side)

**File Location:** `CyberD3signUnity/Assets/Scripts/BPMN Engine/GPTManager.cs` 

**Purpose:**
GPTManager serves as the central orchestrator for all AI-powered interactions in the CyberD3sign application. It manages communication with the FastAPI backend, implements intent-based routing, and handles conversation history.

**Key Responsibilities:**

1. **Intent Detection and Routing**
2. **Multi-Endpoint API Communication**
3. **Conversation History Management**
4. **Security Suggestion Processing**
5. **BPMN Diagram Generation Coordination**

**Architecture:**

```
User Input → GPTManager.SendMessageToGPT()
                   ↓
         DetermineIntent() → FastAPI /determine_intent
                   ↓
            RouteByIntent()
                   ↓
    ┌──────────────┼──────────────┐
    │              │              │
    ▼              ▼              ▼
SendToModify() SendToTalk() SendToSuggestSecurity()
    │              │              │
    ▼              ▼              ▼
/modify        /talk        /suggest_security
```

**API Endpoint Configuration:**

```csharp
[Header("API URLs")]
private string intentUrl = "http://217.154.116.117:8000/determine_intent";
private string modifyUrl = "http://217.154.116.117:8000/modify";
private string talkUrl = "http://217.154.116.117:8000/talk";
private string suggestUrl = "http://217.154.116.117:8000/suggest_security";
```

**Server Details:**
- **Server:** IONOS Cloud (dedicated to LLM processing)
- **IP Address:** 217.154.116.117
- **Port:** 8000
- **Protocol:** HTTP (REST)
- **Content-Type:** application/json
- **API Keys Stored:** OpenAI, Anthropic, Google, Fireworks
- **Cost Model:** Pay-per-API-call (no GPU infrastructure needed)

### 3.2 Intent Detection System

**Method:** `DetermineIntent(string userMessage)`

**Flow:**
```csharp
public void SendMessageToGPT(string userMessage)
{
    if (!isRequestInProgress && !string.IsNullOrEmpty(userMessage))
    {
        // Add to conversation history
        messageHistory.Add(new Message {
            role = "user",
            content = userMessage
        });

        // Start intent detection coroutine
        StartCoroutine(DetermineIntent(userMessage));
    }
}
```

**Intent Detection Request:**

```csharp
IntentRequestWrapper wrapper = new IntentRequestWrapper
{
    model = "gpt-4.1-nano",
    message_history = messageHistory.ToArray(),
    process = new ProcessItem[0]
};

string json = JsonUtility.ToJson(wrapper);
byte[] bodyRaw = Encoding.UTF8.GetBytes(json);
```

**Supported Intents:**
1. **create_process** - Create new BPMN diagram from scratch
2. **edit_process** - Modify existing diagram
3. **modify** - Generic modification intent
4. **chat** - General conversation
5. **ask_question** - Query about the system or process
6. **talk** - Conversational interaction
7. **suggest_security** - Request security analysis

**Intent Routing Logic:**

```csharp
private void RouteByIntent(string intent, string message)
{
    Debug.Log($"Intent: {intent}");

    switch (intent)
    {
        case "create_process":
        case "edit_process":
        case "modify":
            StartCoroutine(SendToModify(message));
            break;

        case "chat":
        case "ask_question":
        case "talk":
            StartCoroutine(SendToTalk(message));
            break;

        case "suggest_security":
            StartCoroutine(SendToSuggestSecurity());
            break;

        default:
            responseText.text = $"Unsupported intent: {intent}";
            isRequestInProgress = false;
            break;
    }
}
```

### 3.3 Conversation Management

**Message History Structure:**

```csharp
[System.Serializable]
public class Message {
    public string role;      // "user" or "assistant"
    public string content;   // Message text
}

private List<Message> messageHistory = new List<Message>();
```

**Multi-Turn Conversation Support:**
- Maintains complete conversation context
- Sent with every API request for contextual understanding
- Enables follow-up questions and iterative refinement

**Example Conversation Flow:**
```
User: "Create a purchase order process"
  → Intent: create_process
  → Route: SendToModify()
  → Result: BPMN XML generated

User: "Add approval step"
  → Intent: edit_process
  → Context: Previous BPMN + conversation history
  → Route: SendToModify()
  → Result: Modified BPMN XML

User: "What security measures should I add?"
  → Intent: suggest_security
  → Route: SendToSuggestSecurity()
  → Result: Security ontology mappings
```

### 3.4 API Integration Architecture

**Modify Endpoint (BPMN Generation):**

```csharp
private IEnumerator SendToModify(string userPrompt)
{
    responseText.text = "Generating BPMN diagram...";
    messageHistory.Add(new Message {
        role = "user",
        content = userPrompt
    });

    string escapedPrompt = userPrompt.Replace("\"", "\\\"");
    string json = "{\"model\":\"gpt-4.1-nano\"," +
                  "\"message_history\":[{\"role\":\"user\"," +
                  "\"content\":\"" + escapedPrompt + "\"}]," +
                  "\"process\":null}";

    byte[] bodyRaw = Encoding.UTF8.GetBytes(json);

    using UnityWebRequest request = new UnityWebRequest(modifyUrl, "POST")
    {
        uploadHandler = new UploadHandlerRaw(bodyRaw),
        downloadHandler = new DownloadHandlerBuffer()
    };
    request.SetRequestHeader("Content-Type", "application/json");

    yield return request.SendWebRequest();

    if (request.result == UnityWebRequest.Result.Success)
    {
        ModifyResponse parsed = JsonUtility.FromJson<ModifyResponse>(
            request.downloadHandler.text
        );

        if (!string.IsNullOrEmpty(parsed.bpmn_xml))
        {
            // Store BPMN XML in global handler
            DiagramHandler.BPMNDiagramData = parsed.bpmn_xml;
            latestResponse = parsed.bpmn_xml;

            // Trigger diagram rendering
            if (loadLLMDiagramInstance != null)
            {
                loadLLMDiagramInstance.InitializeDiagram();
                responseText.text = "Diagram rendered!";
            }
        }
    }

    isRequestInProgress = false;
}
```

**Talk Endpoint (Conversational Interface):**

```csharp
private IEnumerator SendToTalk(string userPrompt)
{
    responseText.text = "Getting response...";

    TalkRequestWrapper wrapper = new TalkRequestWrapper
    {
        model = "gpt-4.1-nano",
        message_history = messageHistory.ToArray(),
        process = new ProcessItem[0],
        needs_to_be_final_comment = false
    };

    string json = JsonUtility.ToJson(wrapper);
    byte[] bodyRaw = Encoding.UTF8.GetBytes(json);

    using UnityWebRequest request = new UnityWebRequest(talkUrl, "POST")
    {
        uploadHandler = new UploadHandlerRaw(bodyRaw),
        downloadHandler = new DownloadHandlerBuffer()
    };
    request.SetRequestHeader("Content-Type", "application/json");

    yield return request.SendWebRequest();

    if (request.result == UnityWebRequest.Result.Success)
    {
        TalkResponse parsed = JsonUtility.FromJson<TalkResponse>(
            request.downloadHandler.text
        );

        responseText.text = parsed.message;

        // Add assistant response to history
        messageHistory.Add(new Message {
            role = "assistant",
            content = parsed.message
        });

        latestResponse = parsed.message;
    }

    isRequestInProgress = false;
}
```

**Security Suggestion Endpoint:**

```csharp
private IEnumerator SendToSuggestSecurity()
{
    responseText.text = "Checking for security suggestions...";

    var suggestReq = new SuggestRequestWrapper
    {
        model = "gpt-4.1-nano",
        modified_bpmn_xml = DiagramHandler.BPMNDiagramData,
        message_history = messageHistory.ToArray()
    };

    string json = JsonUtility.ToJson(suggestReq);
    byte[] bodyRaw = Encoding.UTF8.GetBytes(json);

    using UnityWebRequest request = new UnityWebRequest(suggestUrl, "POST")
    {
        uploadHandler = new UploadHandlerRaw(bodyRaw),
        downloadHandler = new DownloadHandlerBuffer()
    };
    request.SetRequestHeader("Content-Type", "application/json");

    yield return request.SendWebRequest();

    if (request.result == UnityWebRequest.Result.Success)
    {
        string rawJson = request.downloadHandler.text;
        Debug.Log("Raw Suggestions JSON: " + rawJson);

        // Parse using MiniJson for complex nested structures
        var parsed = MiniJson.Deserialize(rawJson)
            as Dictionary<string, object>;

        // Extract explanation
        string explanation = parsed.ContainsKey("explanation")
            ? parsed["explanation"].ToString()
            : null;

        if (!string.IsNullOrEmpty(explanation))
        {
            responseText.text = $"🧠 Security Summary:\n{explanation}";
            latestResponse = explanation;
        }

        // Extract security ontology mappings
        lastSecuritySuggestions = parsed.ContainsKey("security_ontologies")
            ? (List<object>)parsed["security_ontologies"]
            : null;

        if (lastSecuritySuggestions != null)
        {
            // Convert to XML and visualize
            string mergedSecurityXml =
                ConvertSecuritySuggestionsToXml(lastSecuritySuggestions);

            DiagramHandler.securityRequirements = mergedSecurityXml;
            DrawElements.Instance().DrawBPMNSecurity();
        }
    }

    isRequestInProgress = false;
}
```

**Security XML Conversion:**

This is a critical method that transforms LLM-generated security suggestions into the XML format expected by the visualization engine:

```csharp
private string ConvertSecuritySuggestionsToXml(
    List<object> suggestions)
{
    XmlDocument xmlDoc = new XmlDocument();
    XmlElement root = xmlDoc.CreateElement("ParentTaskSecurityHolder");
    xmlDoc.AppendChild(root);

    foreach (var suggestion in suggestions)
    {
        var dict = suggestion as Dictionary<string, object>;
        if (dict == null) continue;

        string taskId = dict["elementID"].ToString();
        List<object> ontologyPaths = dict["ontology_path"]
            as List<object>;

        if (ontologyPaths == null) continue;

        // Create TaskSecurityHolder for this element
        XmlElement taskHolder = xmlDoc.CreateElement(
            "TaskSecurityHolder"
        );
        taskHolder.SetAttribute("TaskID", taskId);

        foreach (string fullPath in ontologyPaths)
        {
            // Example path: root/bpmnElement/privacy/confidentiality/encryption
            string[] tags = fullPath.Split('/');
            if (tags.Length < 3) continue;

            // Skip "root" and "bpmnElement" prefixes
            int startIndex = System.Array.IndexOf(tags, "bpmnElement") + 1;
            if (startIndex <= 0 || startIndex >= tags.Length) continue;

            // Build nested XML structure
            XmlElement currentParent = taskHolder;
            for (int i = startIndex; i < tags.Length; i++)
            {
                string tag = tags[i];
                XmlElement existing = null;

                // Check if tag already exists (avoid duplicates)
                foreach (XmlNode child in currentParent.ChildNodes)
                {
                    if (child.Name == tag)
                    {
                        existing = (XmlElement)child;
                        break;
                    }
                }

                if (existing == null)
                {
                    XmlElement newNode = xmlDoc.CreateElement(tag);
                    currentParent.AppendChild(newNode);
                    currentParent = newNode;
                }
                else
                {
                    currentParent = existing;
                }
            }
        }

        root.AppendChild(taskHolder);
    }

    return xmlDoc.OuterXml;
}
```

**Data Structures:**

```csharp
[System.Serializable]
public class Message {
    public string role;
    public string content;
}

[System.Serializable]
public class IntentResponse {
    public string intent;
    public float confidence;
}

[System.Serializable]
public class ModifyResponse {
    public string bpmn_xml;
    public string bpmn_json;
}

[System.Serializable]
public class TalkResponse {
    public string message;
}

[System.Serializable]
public class TalkRequestWrapper
{
    public string model;
    public Message[] message_history;
    public ProcessItem[] process;
    public bool needs_to_be_final_comment;
}

[System.Serializable]
public class IntentRequestWrapper
{
    public string model;
    public Message[] message_history;
    public ProcessItem[] process;
}

[System.Serializable]
public class SuggestRequestWrapper
{
    public string model;
    public string modified_bpmn_xml;
    public Message[] message_history;
}

[System.Serializable]
public class ProcessItem { }
```

---

## 4. Diagram Loading and Rendering System

### 4.1 loadBPMNDiagram Component

**File Location:** `CyberD3signUnity/Assets/Scripts/BPMN Engine/loadBPMNDiagram.cs` (142 lines)

**Purpose:**
Loads and renders BPMN diagrams from XML data stored in DiagramHandler. This component handles user-created or manually-loaded diagrams (not LLM-generated diagrams, which use loadLLMDiagram).

**Key Features:**
1. XML parsing of BPMN structure
2. Dynamic prefab instantiation
3. Arrow/edge rendering
4. Position and scale application

**Initialization Flow:**

```csharp
void Start()
{
    XmlDocument xmlDoc = new XmlDocument();

    if (!string.IsNullOrEmpty(DiagramHandler.BPMNDiagramData))
    {
        xmlData = DiagramHandler.BPMNDiagramData;
        xmlDoc.LoadXml(xmlData);

        XmlNodeList bpmnElements = xmlDoc.GetElementsByTagName("BPMNShape");
        XmlNodeList bpmnArrows = xmlDoc.GetElementsByTagName("BPMNEdge");

        // Process shapes
        foreach (XmlNode bpmnShape in bpmnElements)
        {
            // Extract element data and instantiate
        }

        // Process arrows
        foreach (XmlNode bpmnEdge in bpmnArrows)
        {
            // Create arrow connections
        }
    }
    else
    {
        // Initialize empty XML structure
        XmlElement elemRoot = (XmlElement)xmlDoc.AppendChild(
            xmlDoc.CreateElement("root")
        );
        DiagramHandler.BPMNDiagramData = xmlDoc.ToString();
        DiagramHandler.BPMNDoc = xmlDoc;
    }
}
```

**Element Processing:**

```csharp
foreach (XmlNode bpmnShape in bpmnElements)
{
    // Extract attributes
    string elementType = bpmnShape.Attributes["bpmnElement"].Value;
    string ID = bpmnShape.Attributes["id"].Value;
    float height = float.Parse(
        bpmnShape.FirstChild.Attributes["height"].Value
    );
    float width = float.Parse(
        bpmnShape.FirstChild.Attributes["width"].Value
    );
    float x = float.Parse(
        bpmnShape.FirstChild.Attributes["x"].Value
    );
    float y = float.Parse(
        bpmnShape.FirstChild.Attributes["y"].Value
    );

    // Save element details for persistence
    SaveHandler.elementSaveDetails.Add(
        new elementSaveDetails(elementType, ID, height, width, x, y)
    );

    // Load appropriate prefab based on element type
    GameObject BPMNShape;

    if (elementType.Contains("Event"))
    {
        BPMNShape = Instantiate(
            Resources.Load("BPMN Engine Assets/Events/" + elementType)
        ) as GameObject;
    }
    else if (elementType.Contains("Gateway"))
    {
        BPMNShape = Instantiate(
            Resources.Load("BPMN Engine Assets/Gateways/" + elementType)
        ) as GameObject;
    }
    else if (elementType == "textHolder")
    {
        BPMNShape = Instantiate(
            Resources.Load("BPMN Engine Assets/" + elementType)
        ) as GameObject;
    }
    else
    {
        BPMNShape = Instantiate(
            Resources.Load("BPMN Engine Assets/Tasks/" + elementType)
        ) as GameObject;
    }

    // Set element text if available
    if (bpmnShape.Attributes["text"] != null)
    {
        string elementText = bpmnShape.Attributes["text"].Value;
        SaveHandler.elementSaveDetails[
            SaveHandler.elementSaveDetails.Count - 1
        ].updateElementText(elementText);
        BPMNShape.GetComponentInChildren<Text>().text = elementText;
    }

    // Position element
    BPMNShape.name = ID;
    BPMNShape.transform.position = new Vector3(
        x,
        BPMNShape.transform.position.y,
        y
    );

    // Scale pools and lanes differently
    if (elementType.Contains("pool") || elementType.Contains("lane"))
    {
        BPMNShape.transform.GetChild(5).transform.localScale =
            new Vector3(width, height, 0);
    }
}
```

**Arrow Processing:**

```csharp
foreach (XmlNode bpmnEdge in bpmnArrows)
{
    string arrowName = bpmnEdge.Attributes["id"].Value;
    string startElement = bpmnEdge.Attributes["startElement"].Value;
    string startPosition = bpmnEdge.Attributes["startPosition"].Value;
    string targetElement = bpmnEdge.Attributes["targetElement"].Value;
    string targetPosition = bpmnEdge.Attributes["targetPosition"].Value;

    List<vertexPosition> positions = new List<vertexPosition>();
    XmlNodeList arrowPositions = bpmnEdge.ChildNodes;

    // Add start position
    positions.Add(new vertexPosition(
        0,
        float.Parse(arrowPositions[0].Attributes["x"].Value),
        float.Parse(arrowPositions[0].Attributes["y"].Value)
    ));

    // Add intermediate waypoints
    for (int i = 1; i < arrowPositions.Count - 1; i++)
    {
        positions.Add(new vertexPosition(
            i,
            float.Parse(arrowPositions[i].Attributes["x"].Value),
            float.Parse(arrowPositions[i].Attributes["y"].Value)
        ));
    }

    // Add end position
    positions.Add(new vertexPosition(
        arrowPositions.Count - 1,
        float.Parse(arrowPositions[arrowPositions.Count - 1]
            .Attributes["x"].Value),
        float.Parse(arrowPositions[arrowPositions.Count - 1]
            .Attributes["y"].Value)
    ));

    // Add arrow to source element
    GameObject.Find(startElement)
        .GetComponentInChildren<createNewArrow>()
        .elementArrows.Add(
            new arrow(
                arrowName,
                startElement,
                startPosition,
                targetElement,
                targetPosition,
                positions
            )
        );
}
```

### 4.2 loadLLMDiagram Component

**File Location:** `CyberD3signUnity/Assets/Scripts/BPMN Engine/loadLLMDiagram.cs` (1000 lines, including multiple implementation iterations)

**Purpose:**
Specialized component for rendering LLM-generated BPMN diagrams. Includes advanced features like automatic scaling, gateway arrow position adjustment, and element type normalization.

**Key Differences from loadBPMNDiagram:**
1. **Automatic Scaling**: Applies 0.26x scale factor to all coordinates
2. **Gateway Arrow Optimization**: Adjusts arrow positions for better visual layout
3. **Element Type Normalization**: Maps generic types (e.g., "task") to specific prefab names (e.g., "businessTask")
4. **Enhanced Error Handling**: More robust prefab loading and instantiation

**Critical Scale Factor:**

```csharp
private const float scaleFactor = 0.26f;
// 26% of original size - tuned for LLM-generated diagrams
```

**Why Scaling is Necessary:**
LLM-generated diagrams often use standard BPMN coordinate systems (e.g., 100x100 pixel elements, 800x600 canvas), which are too large for Unity's 3D space. The 0.26 scale factor brings dimensions into an appropriate range for visualization.

**InitializeDiagram Method:**

```csharp
public void InitializeDiagram()
{
    XmlDocument xmlDoc = new XmlDocument();

    if (string.IsNullOrEmpty(DiagramHandler.BPMNDiagramData))
    {
        XmlElement root = xmlDoc.CreateElement("root");
        xmlDoc.AppendChild(root);
        DiagramHandler.BPMNDiagramData = xmlDoc.OuterXml;
        DiagramHandler.BPMNDoc = xmlDoc;
        return;
    }

    xmlData = DiagramHandler.BPMNDiagramData;
    xmlDoc.LoadXml(xmlData);

    // ✅ Adjust gateway arrow positions for better layout
    xmlDoc = AdjustGatewayArrowPositions(xmlDoc);
    DiagramHandler.AdjustedBPMNData = xmlDoc.OuterXml;

    XmlNodeList bpmnElements = xmlDoc.GetElementsByTagName("BPMNShape");
    XmlNodeList bpmnArrows = xmlDoc.GetElementsByTagName("BPMNEdge");

    // Process elements and arrows with scaling
}
```

**Element Processing with Scaling:**

```csharp
foreach (XmlNode bpmnShape in bpmnElements)
{
    try
    {
        string elementType = bpmnShape.Attributes["type"]?.Value;

        if (string.IsNullOrEmpty(elementType))
            elementType = bpmnShape.Attributes["bpmnElement"].Value;

        // ✅ Normalize element type
        elementType = NormalizeElementType(elementType);

        string ID = bpmnShape.Attributes["id"].Value;

        // ✅ Apply scale factor to all dimensions
        float height = float.Parse(
            bpmnShape["Bounds"].Attributes["height"].Value
        ) * scaleFactor;

        float width = float.Parse(
            bpmnShape["Bounds"].Attributes["width"].Value
        ) * scaleFactor;

        float x = float.Parse(
            bpmnShape["Bounds"].Attributes["x"].Value
        ) * scaleFactor;

        float y = float.Parse(
            bpmnShape["Bounds"].Attributes["y"].Value
        ) * scaleFactor;

        string elementText = bpmnShape.Attributes["text"]?.Value ?? "";

        SaveHandler.elementSaveDetails.Add(
            new elementSaveDetails(elementType, ID, height, width, x, y)
        );
        SaveHandler.elementSaveDetails[
            SaveHandler.elementSaveDetails.Count - 1
        ].updateElementText(elementText);

        // Load and instantiate prefab
        string prefabPath = GetPrefabPath(elementType);
        Object prefab = Resources.Load(prefabPath);
        if (prefab == null) continue;

        GameObject BPMNShape = Instantiate(prefab) as GameObject;
        if (BPMNShape == null) continue;

        BPMNShape.name = ID;
        BPMNShape.transform.position = new Vector3(
            x,
            BPMNShape.transform.position.y,
            y
        );

        Text label = BPMNShape.GetComponentInChildren<Text>();
        if (label != null) label.text = elementText;

        // Handle pool/lane scaling
        if (elementType.Contains("pool") || elementType.Contains("lane"))
        {
            string[] possibleNames = {
                "scale", "Resizable", "Background", "Body", "Container"
            };

            foreach (string name in possibleNames)
            {
                Transform resizable = BPMNShape.transform.Find(name);
                if (resizable != null)
                {
                    resizable.localScale = new Vector3(width, height, 0);
                    break;
                }
            }
        }
    }
    catch (System.Exception ex)
    {
        Debug.LogError("❗ Error processing BPMN shape: " + ex.Message);
    }
}
```

**Element Type Normalization:**

```csharp
private string NormalizeElementType(string rawType)
{
    switch (rawType.ToLower())
    {
        case "start": return "startEvent";
        case "end": return "endEvent";
        case "task":
        case "task1": return "businessTask";
        case "script": return "scriptTask";
        case "mail": return "mailTask";
        case "manual": return "manualTask";
        case "service": return "serviceTask";
        case "user": return "userTask";
        case "receive": return "receiveTask";
        default: return rawType;
    }
}
```

This normalization is crucial because LLMs may generate generic type names (e.g., "task", "start", "end") that don't match the specific prefab names in the Unity Resources folder.

**Gateway Arrow Position Adjustment:**

```csharp
private XmlDocument AdjustGatewayArrowPositions(XmlDocument xmlDoc)
{
    // 1. Collect all gateway IDs
    HashSet<string> gatewayIds = new HashSet<string>();
    XmlNodeList shapes = xmlDoc.GetElementsByTagName("BPMNShape");

    foreach (XmlNode shape in shapes)
    {
        string type = shape.Attributes["type"]?.Value?.ToLower();
        if (!string.IsNullOrEmpty(type) && type.Contains("gateway"))
        {
            string id = shape.Attributes["id"]?.Value;
            if (!string.IsNullOrEmpty(id))
                gatewayIds.Add(id);
        }
    }

    // 2. Group outgoing edges by startElement
    Dictionary<string, List<XmlNode>> gatewayEdges =
        new Dictionary<string, List<XmlNode>>();

    XmlNodeList edges = xmlDoc.GetElementsByTagName("BPMNEdge");

    foreach (XmlNode edge in edges)
    {
        string startElement = edge.Attributes["startElement"]?.Value;
        if (string.IsNullOrEmpty(startElement)) continue;

        if (!gatewayIds.Contains(startElement)) continue;

        if (!gatewayEdges.ContainsKey(startElement))
            gatewayEdges[startElement] = new List<XmlNode>();

        gatewayEdges[startElement].Add(edge);
    }

    // 3. Apply right, bottom, top order for each gateway
    foreach (var kvp in gatewayEdges)
    {
        string[] positions = {
            "locationRight",
            "locationBottom",
            "locationTop"
        };

        List<XmlNode> edgesList = kvp.Value;

        for (int i = 0; i < edgesList.Count; i++)
        {
            XmlNode edge = edgesList[i];
            XmlAttribute attr = edge.Attributes["startPosition"];

            if (attr == null)
            {
                attr = xmlDoc.CreateAttribute("startPosition");
                edge.Attributes.Append(attr);
            }

            // Assign position (right, bottom, top) in order
            attr.Value = positions[i % positions.Length];
        }
    }

    return xmlDoc;
}
```

**Why Gateway Adjustment Matters:**
Gateways (decision points) often have multiple outgoing arrows. Without position adjustment, all arrows might emanate from the same point, creating visual clutter. This algorithm distributes arrows to right, bottom, and top positions for clarity.

**Arrow Processing with Scaling:**

```csharp
foreach (XmlNode bpmnEdge in bpmnArrows)
{
    try
    {
        string arrowName = bpmnEdge.Attributes["id"]?.Value;
        string startElement = bpmnEdge.Attributes["startElement"]?.Value;
        string startPosition = bpmnEdge.Attributes["startPosition"]?.Value;
        string targetElement = bpmnEdge.Attributes["targetElement"]?.Value;
        string targetPosition = bpmnEdge.Attributes["targetPosition"]?.Value;

        if (string.IsNullOrEmpty(startElement)) continue;

        GameObject startGO = GameObject.Find(startElement);
        if (startGO == null || IsStaticElement(startElement)) continue;

        createNewArrow arrowComp =
            startGO.GetComponentInChildren<createNewArrow>();
        if (arrowComp == null) continue;

        if (arrowComp.elementArrows == null)
            arrowComp.elementArrows = new List<arrow>();

        List<vertexPosition> positions = new List<vertexPosition>();

        foreach (XmlNode pos in bpmnEdge.ChildNodes)
        {
            // ✅ Apply scale factor to arrow waypoints
            float vx = float.Parse(pos.Attributes["x"].Value) * scaleFactor;
            float vy = float.Parse(pos.Attributes["y"].Value) * scaleFactor;
            positions.Add(new vertexPosition(positions.Count, vx, vy));
        }

        arrow newArrow = new arrow(
            arrowName,
            startElement,
            startPosition,
            targetElement,
            targetPosition,
            positions
        );

        arrowComp.elementArrows.Add(newArrow);
    }
    catch (System.Exception ex)
    {
        Debug.LogError("❗ Error processing BPMN edge: " + ex.Message);
        Debug.Log($"📐 Diagram scaling applied with factor {scaleFactor}");
    }
}
```

**Prefab Path Resolution:**
**Note that if Prefab are not configured properly, it affects rendering process**

```csharp
private string GetPrefabPath(string elementType)
{
    string type = elementType.ToLower();

    if (type.Contains("event"))
        return $"BPMN Engine Assets/Events/{elementType}";
    else if (type.Contains("gateway"))
        return $"BPMN Engine Assets/Gateways/{elementType}";
    else if (type == "textholder")
        return $"BPMN Engine Assets/{elementType}";
    else if (type.Contains("arrow"))
        return $"BPMN Engine Assets/Arrows/{elementType}";
    else
        return $"BPMN Engine Assets/Tasks/{elementType}";
}
```

**Static Element Filtering:**

```csharp
private bool IsStaticElement(string elementId)
{
    string id = elementId.ToLower();
    return id.Contains("pool") ||
           id.Contains("lane") ||
           id.Contains("textholder");
}
```

Static elements (pools, lanes, text holders) don't emit arrows, so they're filtered out during arrow processing to avoid errors.

### 4.3 XML Processing Pipeline

**BPMN XML Structure:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<root>
  <BPMNShape bpmnElement="startEvent" id="start_1" text="Start">
    <Bounds height="80" width="80" x="100" y="200"/>
  </BPMNShape>

  <BPMNShape type="userTask" id="task_1" text="Review Order">
    <Bounds height="60" width="100" x="250" y="200"/>
  </BPMNShape>

  <BPMNShape type="exclusiveGateway" id="gateway_1" text="">
    <Bounds height="50" width="50" x="400" y="200"/>
  </BPMNShape>

  <BPMNEdge id="flow_1" startElement="start_1"
           startPosition="locationRight"
           targetElement="task_1"
           targetPosition="locationLeft">
    <waypoint x="180" y="240"/>
    <waypoint x="250" y="240"/>
  </BPMNEdge>

  <BPMNEdge id="flow_2" startElement="task_1"
           startPosition="locationRight"
           targetElement="gateway_1"
           targetPosition="locationLeft">
    <waypoint x="350" y="240"/>
    <waypoint x="400" y="240"/>
  </BPMNEdge>
</root>
```

**Parsing Flow:**

```
XML String (from DiagramHandler)
        ↓
XmlDocument.LoadXml()
        ↓
GetElementsByTagName("BPMNShape")
GetElementsByTagName("BPMNEdge")
        ↓
For each BPMNShape:
  - Extract attributes (type, id, text)
  - Parse <Bounds> child (height, width, x, y)
  - Apply scaling (loadLLMDiagram only)
  - Normalize type
  - Resolve prefab path
  - Instantiate GameObject
  - Position and scale
        ↓
For each BPMNEdge:
  - Extract attributes (id, startElement, targetElement, positions)
  - Parse <waypoint> children
  - Apply scaling (loadLLMDiagram only)
  - Create arrow object
  - Add to source element's arrow list
        ↓
Complete diagram rendered in Unity scene
```

### 4.4 Dynamic Prefab Instantiation

**Prefab Organization:**

```
Resources/
  └── BPMN Engine Assets/
      ├── Events/
      │   ├── startEvent.prefab
      │   ├── endEvent.prefab
      │   ├── intermediateEvent.prefab
      │   └── boundaryEvent.prefab
      │
      ├── Tasks/
      │   ├── businessTask.prefab
      │   ├── userTask.prefab
      │   ├── serviceTask.prefab
      │   ├── scriptTask.prefab
      │   ├── manualTask.prefab
      │   ├── receiveTask.prefab
      │   └── mailTask.prefab
      │
      ├── Gateways/
      │   ├── exclusiveGateway.prefab
      │   ├── parallelGateway.prefab
      │   ├── inclusiveGateway.prefab
      │   └── eventBasedGateway.prefab
      │
      └── Arrows/
          ├── sequenceFlow.prefab
          └── messageFlow.prefab
```

**Instantiation Process:**

```csharp
// 1. Determine prefab path based on element type
string prefabPath = GetPrefabPath(elementType);
// Example: "BPMN Engine Assets/Tasks/userTask"

// 2. Load prefab from Resources
Object prefab = Resources.Load(prefabPath);

// 3. Validate prefab exists
if (prefab == null)
{
    Debug.LogError($"Prefab not found: {prefabPath}");
    continue;
}

// 4. Instantiate GameObject
GameObject BPMNShape = Instantiate(prefab) as GameObject;

// 5. Configure GameObject
BPMNShape.name = ID;  // Set unique identifier
BPMNShape.transform.position = new Vector3(x, y_offset, y);
BPMNShape.transform.localScale = new Vector3(width, height, 1);

// 6. Set text label
Text label = BPMNShape.GetComponentInChildren<Text>();
if (label != null) label.text = elementText;
```

---

## 5. Unity Frontend Layer

### 5.1 DiagramHandler

**File Location:** `CyberD3signUnity/Assets/Scripts/BPMN Engine/DiagramHandler.cs` (889 lines)

**Purpose:**
Central repository for diagram data using static variables. Acts as a singleton-like data store accessible from all components.

**Key Static Variables:**

```csharp
public static string BPMNDiagramData;        // Current BPMN XML
public static string AdjustedBPMNData;       // Scaled/adjusted XML (from loadLLMDiagram)
public static XmlDocument BPMNDoc;           // Parsed XML document
public static string securityRequirements;   // Security ontology XML
```

**Core Methods:**

```csharp
public void getDiagrams()
{
    // Fetch diagrams from IONOS server
    // Implements pagination (10 items per page)
}

public void SecurityDiagrams()
{
    // Fetch security diagrams from server
}

public void ParseBPMN()
{
    // Parse and load selected BPMN diagram
}

public void BPMNClickHandler()
{
    // Handle diagram selection clicks
}
```

**Pagination Implementation:**

```csharp
private int currentPage = 0;
private const int itemsPerPage = 10;

public void getDiagrams()
{
    int startIndex = currentPage * itemsPerPage;
    int endIndex = startIndex + itemsPerPage;

    // Fetch items [startIndex, endIndex) from server
}
```

### 5.2 SaveHandler

**File Location:** `CyberD3signUnity/Assets/Scripts/BPMN Engine/SaveHandler.cs` (322 lines)

**Purpose:**
Manages diagram persistence including screenshot capture and XML serialization.

**Key Methods:**

```csharp
public void tSaveBPMN()
{
    // Trigger BPMN save workflow
}

public void saveBPMN()
{
    // Save BPMN diagram to IONOS server
    // Includes screenshot capture
}

public void saveSecurity()
{
    // Save security diagram
}

public void saveRequirements()
{
    // Save security requirements
}
```

**Screenshot Capture Workflow:**

```csharp
// 1. Position camera to capture diagram
Camera.main.transform.position = CalculateCenterPoint();
Camera.main.orthographicSize = CalculateOptimalZoom();

// 2. Capture screenshot
ScreenCapture.CaptureScreenshot("diagram_preview.png");

// 3. Wait for file write
yield return new WaitForSeconds(0.5f);

// 4. Read screenshot and convert to base64
byte[] imageBytes = File.ReadAllBytes("diagram_preview.png");
string base64Image = Convert.ToBase64String(imageBytes);

// 5. Include in save request
```

### 5.3 Login System

**File Location:** `CyberD3signUnity/Assets/Scripts/BPMN Engine/Login.cs` (212 lines)

**Purpose:**
User authentication against IONOS server with server toggle support.

**Server Configuration:**

```csharp
public class ServerConnection
{
    public static string localhostServer = "http://localhost/cyberd3sign/";
    public static string productionServer = "https://cyberd3sign.com/";

    public static string currentServer = productionServer;
}
```

**Authentication Flow:**

```csharp
public void LoginUser(string username, string password)
{
    string url = ServerConnection.currentServer + "login.php";

    WWWForm form = new WWWForm();
    form.AddField("username", username);
    form.AddField("password", password);

    UnityWebRequest request = UnityWebRequest.Post(url, form);

    yield return request.SendWebRequest();

    if (request.result == UnityWebRequest.Result.Success)
    {
        LoginResponse response = JsonUtility.FromJson<LoginResponse>(
            request.downloadHandler.text
        );

        if (response.success)
        {
            SessionManager.userId = response.userId;
            SessionManager.username = response.username;
            SceneManager.LoadScene("MainScene");
        }
    }
}
```

### 5.4 Security Analysis and Visualization

**File Location:** `CyberD3signUnity/Assets/Scripts/DrawElements.cs` (Lines 169-299)

**Purpose:**
Visualizes security requirements by rendering security symbols above BPMN elements based on XML data from LLM analysis.

**Security Analysis Flow:**

Security analysis in CyberD3sign works through the following integrated pipeline:

1. **User Request** → GPTManager detects "suggest_security" intent
2. **LLM Analysis** → FastAPI backend `/suggest_security` analyzes BPMN
3. **XML Generation** → GPTManager converts ontology paths to hierarchical XML
4. **Storage** → XML stored in `DiagramHandler.securityRequirements`
5. **Visualization** → DrawElements.DrawBPMNSecurity() renders security symbols

**DrawBPMNSecurity Method:**

```csharp
public void DrawBPMNSecurity()
{
    // Clear existing security visualizations
    foreach (taskSecurityLines tsl in taskLines)
    {
        Destroy(tsl.getLine());
    }
    taskLines.Clear();

    foreach (symbol s in taskSymbols)
    {
        Destroy(s.getLine());
        Destroy(s.getSecuritySymbol());
        Destroy(s.getTask());
    }
    taskSymbols.Clear();

    // Load security requirements XML
    XmlDocument xmlDoc = new XmlDocument();

    if (!string.IsNullOrEmpty(DiagramHandler.securityRequirements))
    {
        xmlDoc.LoadXml(DiagramHandler.securityRequirements);

        // Process each TaskSecurityHolder
        XmlNodeList securityHolder = xmlDoc.GetElementsByTagName("TaskSecurityHolder");

        foreach (XmlNode securityLine in securityHolder)
        {
            string taskID = securityLine.Attributes["TaskID"].Value;

            // Find corresponding BPMN element
            GameObject bpmnObject = GameObject.Find(taskID);

            if (bpmnObject != null)
            {
                // Calculate position for security line and symbols
                Vector3 pos1 = new Vector3(
                    bpmnObject.transform.position.x +
                    (bpmnObject.GetComponent<Renderer>().bounds.size.x / 2),
                    bpmnObject.transform.position.y,
                    bpmnObject.transform.position.z - 4
                );
                Vector3 pos2 = new Vector3(
                    pos1.x,
                    pos1.y + 390,  // Vertical line height
                    pos1.z
                );

                // Draw vertical line above element
                taskLines.Add(new taskSecurityLines(taskID, pos1, pos2));

                // Render security symbols hierarchically (4 levels)
                foreach (XmlNode level1 in securityLine.ChildNodes)
                {
                    // Level 1: accesscontrol, privacy, integrity, etc.
                    taskSymbols.Add(new symbol(
                        level1.Name, taskID, pos1.x, -pos1.z
                    ));

                    foreach (XmlNode level2 in level1.ChildNodes)
                    {
                        // Level 2: confidentiality, authentication, etc.
                        taskSymbols.Add(new symbol(
                            level2.Name, taskID, pos1.x, -pos1.z
                        ));

                        foreach (XmlNode level3 in level2.ChildNodes)
                        {
                            // Level 3: encryption, access_control, etc.
                            taskSymbols.Add(new symbol(
                                level3.Name, taskID, pos1.x, -pos1.z
                            ));

                            foreach (XmlNode level4 in level3.ChildNodes)
                            {
                                // Level 4: AES256, RSA, etc.
                                taskSymbols.Add(new symbol(
                                    level4.Name, taskID, pos1.x, -pos1.z
                                ));
                            }
                        }
                    }
                }
            }
        }
    }
    else
    {
        // Initialize empty security XML structure
        XmlElement elemRoot = (XmlElement)xmlDoc.AppendChild(
            xmlDoc.CreateElement("ParentTaskSecurityHolder")
        );
        DiagramHandler.securityRequirements = xmlDoc.ToString();
        DiagramHandler.reqDoc = xmlDoc;
    }
}
```

**Security Symbol Hierarchy:**

The system renders security requirements as a 4-level hierarchy of visual symbols:

- **Level 1**: Main categories (accesscontrol, privacy, integrity, accountability, attackharm, availability)
- **Level 2**: Sub-categories (confidentiality, authentication, etc.)
- **Level 3**: Specific controls (encryption, access_control, etc.)
- **Level 4**: Implementation details (AES256, RSA, SHA256, etc.)

Each level is rendered as a stacked symbol above the BPMN element, connected by a vertical line.

---

## 6. Python FastAPI Backend (IONOS Cloud Server)

**Location:** `backend_server_IONOS/bpmn_assistant_cyber3d-main/`

The FastAPI backend on the IONOS Cloud server uses a sophisticated **template-based prompt engineering system** combined with LLM intelligence to generate BPMN diagrams and security analysis. It does NOT use simple prompts alone - instead, it leverages:

1. **Jinja2 Template System** - Structured prompt templates with examples
2. **JSON Schema Definitions** - Strict BPMN representation format
3. **Example-Based Learning** - Few-shot learning with BPMN examples
4. **Ontology Templates** - Pre-defined security taxonomy (XML-based)
5. **Multi-Provider LLM Facade** - Abstraction over OpenAI, Anthropic, Google, Fireworks

### 6.1 Backend Architecture Overview

**File Structure:**
```
backend_server_IONOS/bpmn_assistant_cyber3d-main/
├── src/bpmn_assistant/
│   ├── app.py                          # FastAPI main application
│   ├── prompts/                        # Jinja2 prompt templates
│   │   ├── create_bpmn.jinja2         # BPMN generation template
│   │   ├── bpmn_representation.jinja2  # JSON schema definition
│   │   ├── bpmn_examples.jinja2       # Few-shot learning examples
│   │   ├── determine_intent.jinja2    # Intent classification
│   │   └── edit_bpmn.jinja2           # BPMN modification template
│   ├── services/                       # Business logic
│   │   ├── bpmn_modeling_service.py   # BPMN creation/editing
│   │   ├── bpmn_xml_generator.py      # JSON → XML conversion
│   │   ├── bpmn_json_generator.py     # XML → JSON conversion
│   │   └── determine_intent.py        # Intent classification
│   ├── core/                           # Core components
│   │   ├── llm_facade.py              # LLM provider abstraction
│   │   ├── provider_factory.py        # Provider selection
│   │   └── provider_impl/             # Provider implementations
│   └── ontology_template.xml          # Security taxonomy (6 categories)
```

### 6.2 BPMN Generation: How It Actually Works

**Question:** Does it use only prompts or are there templates?

**Answer:** It uses a **sophisticated template-based system** with structured examples. Here's exactly how:

#### Step-by-Step BPMN Generation Process:

**1. User Request Received**
```
POST /modify
Body: {
  "model": "gpt-4.1-nano",
  "message_history": [{"role": "user", "content": "Create a loan approval process"}],
  "process": null
}
```

**2. Load Jinja2 Template** (`prompts/create_bpmn.jinja2`)

The system loads a structured template that includes:
- **JSON Schema** for BPMN representation
- **Multiple Examples** for few-shot learning
- **Conversation History** for context

Template structure:
```jinja2
{% include 'bpmn_representation.jinja2' %}
{% include 'bpmn_examples.jinja2' %}
---
Message history:
{{ message_history }}

Create a BPMN representation of the process described in the messages.
```

**3. BPMN Representation Schema** (`prompts/bpmn_representation.jinja2`)

This defines the **exact JSON structure** the LLM must follow:

```json
{
  "process": [
    {
      "type": "startEvent" | "endEvent" | "task" | "userTask" | "serviceTask"
              | "exclusiveGateway" | "parallelGateway",
      "id": String,
      "label": String
    }
  ]
}
```

**Task Types:**
- `userTask` - Human interaction (reviewing, deciding, entering data)
- `serviceTask` - Automated system actions (calculations, emails, database)
- `task` - Generic task if not clearly classified

**Gateway Types:**
- `exclusiveGateway` - Decision point (if/else branching)
  - Each branch has: condition, path, optional next
  - Example: "If approved" vs "If rejected"
- `parallelGateway` - Concurrent execution
  - Multiple branches execute simultaneously
  - Auto-synchronized at convergence point

**4. Few-Shot Learning Examples** (`prompts/bpmn_examples.jinja2`)

The template includes **5 complete BPMN examples** showing:

**Example 1: Simple Sequential Process**
```
Description: "Student sends email to professor. Professor receives it.
             If professor agrees, he replies."

Generated JSON:
{
  "process": [
    {"type": "startEvent", "id": "start"},
    {"type": "userTask", "id": "task1", "label": "Send email to professor"},
    {"type": "task", "id": "task2", "label": "Receive the email"},
    {
      "type": "exclusiveGateway",
      "id": "exclusive1",
      "label": "Professor agrees?",
      "has_join": true,
      "branches": [
        {
          "condition": "If the professor agrees",
          "path": [{"type": "task", "id": "task3", "label": "Reply to the student"}]
        },
        {"condition": "If the professor does not agree", "path": []}
      ]
    },
    {"type": "endEvent", "id": "end1"}
  ]
}
```

**Example 2: Parallel Gateway**
```
Description: "Manager sends mail to supplier and prepares documents.
             At the same time, customer searches and picks up goods."

Generated JSON:
{
  "process": [
    {"type": "startEvent", "id": "start"},
    {
      "type": "parallelGateway",
      "id": "parallel1",
      "branches": [
        [
          {"type": "serviceTask", "id": "task1", "label": "Send mail to supplier"},
          {"type": "task", "id": "task2", "label": "Prepare the documents"}
        ],
        [
          {"type": "task", "id": "task3", "label": "Search for the goods"},
          {"type": "task", "id": "task4", "label": "Pick up the goods"}
        ]
      ]
    },
    {"type": "endEvent", "id": "end1"}
  ]
}
```

**Example 3: Loop-Back Process**
```
Description: "Take exam. If score > 50%, record grade.
             If fail, go back and retake exam."

Shows: Loops using "next": "task1" to jump back
```

**Example 4: Nested Gateways**
```
Description: "If Option A, perform Task A, then if Sub-option 1, Task A1..."

Shows: Gateways within gateway paths (nested decision trees)
```

**Example 5: Multiple End Events**
```
Description: "Process order. If valid, fulfill and deliver. If invalid, reject."

Shows: Different end points for different outcomes
```

**5. LLM Processing**

The complete prompt sent to LLM includes:
1. **Full JSON schema** (types, structure, rules)
2. **5 complete examples** (few-shot learning)
3. **User conversation** (current request context)

The LLM generates a JSON structure following the pattern.

**6. Validation and Retry** (`services/validate_bpmn.py`)

```python
def validate_bpmn(process: list) -> None:
    # Check required fields
    # Validate element types
    # Verify gateway structure
    # Ensure start/end events exist

    # If invalid, retry up to 3 times
```

**7. JSON to XML Conversion** (`services/bpmn_xml_generator.py`)

Converts JSON to Unity-compatible BPMN XML:

```python
Input JSON:
{
  "type": "userTask",
  "id": "task1",
  "label": "Submit Application"
}

Output XML:
<BPMNShape bpmnElement="userTask" id="task1" text="Submit Application">
  <Bounds height="60" width="100" x="250" y="200"/>
</BPMNShape>
```

**Automatic Layout Algorithm:**
- Sequential tasks: 150 units apart horizontally
- Gateways: Add vertical spacing for branches
- Parallel paths: Offset vertically
- Calculate positions based on graph structure

### 6.3 Security Analysis: How It Actually Works

**Question:** How does security analysis use templates and ontology?

**Answer:** It uses a **pre-defined XML ontology template** + LLM analysis.

#### Step-by-Step Security Analysis:

**1. Load Ontology Template** (`ontology_template.xml`)

This is a **comprehensive security taxonomy** with 6 main categories:

```xml
<root>
  <bpmnElement>
    <accesscontrol>
      <authentication>
        <persauthentication>
          <credentials usernameRequired passwordRequired pinRequired/>
          <smartcard contactless pinRequired_SC/>
          <biometric biometricType/>
        </persauthentication>
        <networkauthentication>
          <cryptprotocol protocol/>
          <vpn/>
        </networkauthentication>
      </authentication>
      <identification>
        <trustlevel minimumLevel/>
      </identification>
      <authorisation>
        <assetclassification>
          <serviceclassification serviceLevel/>
          <dataclassification dataLevel/>
        </assetclassification>
        <statetransition>
          <bibamodel/>
          <belllapadula/>
        </statetransition>
      </authorisation>
    </accesscontrol>

    <privacy>
      <userconsent onceOnly everyTime>
        <anonymity compulsoryAnonymity>
          <pseudonymity compulsoryPseudonymity/>
        </anonymity>
        <datausage onceOnlyDataUsage everyTimeDataUsage/>
      </userconsent>
      <confidentiality>
        <needtoknow/>
        <encryption keyType size/>
        <dataretention minimumRetention maximumRetention/>
        <pki/>
      </confidentiality>
    </privacy>

    <integrity>
      <dataintegrity>
        <hashfunction/>
        <constraints>
          <inputvalidation date numbersOnly textOnly noNumbers noText noSymbols/>
        </constraints>
      </dataintegrity>
      <hardwareintegrity>
        <physicalsecurity>
          <personnel personnelRequired/>
          <location barriers videoSurveillance alarm lighting/>
        </physicalsecurity>
        <assetmanagement>
          <assetmaintenance maintenanceInterval/>
          <assetregister description serialNumber purchaseDate/>
        </assetmanagement>
      </hardwareintegrity>
      <personnelintegrity>
        <roleassignment>
          <bindingofduty/>
          <separationofduty minimumEntities/>
        </roleassignment>
        <delegation forbidden/>
      </personnelintegrity>
      <softwareintegrity>
        <immunity scanInterval/>
        <patchmanagement patchScanInterval patchInstallTime/>
        <sandbox/>
      </softwareintegrity>
    </integrity>

    <accountability>
      <nonrepudiation>
        <digitalsignature/>
      </nonrepudiation>
      <audittrail userID timeStamp affectedEntity read write modify/>
    </accountability>

    <attackharm>
      <vulnerabilityassessment>
        <systemassessment systemInterval/>
        <environmentassessment environmentInterval/>
        <serviceassessment serviceInterval/>
        <personnelassessment personnelInterval/>
      </vulnerabilityassessment>
      <honeypot>
        <high-interaction/>
        <low-interaction/>
      </honeypot>
      <firewall>
        <networklayer/>
        <applicationlayer/>
      </firewall>
      <intrusiondetection>
        <statefulprotocol/>
        <signaturebased/>
        <anomalydetection/>
      </intrusiondetection>
    </attackharm>

    <availability percentage monthlyDowntime>
      <databackup minimumDataBackups backupFrequency>
        <localbackup minimumLocalBackups/>
        <onlinebackup minimumOnlineBackups/>
      </databackup>
      <servicebackup minimumServiceBackups/>
      <personnelbackup minimumPersonnelBackups/>
      <hardwarebackup minimumHardwareBackups/>
    </availability>
  </bpmnElement>
</root>
```

**2. Extract All Ontology Paths** (`app.py:suggest_security`)

```python
def extract_paths_from_xml(element, current_path="", paths=None):
    path = f"{current_path}/{element.tag}"
    if no_children:
        paths.append(path)  # Leaf node - complete path
    else:
        for child in children:
            extract_paths_from_xml(child, path, paths)
    return paths

available_ontologies = [
  "root/bpmnElement/accesscontrol/authentication/persauthentication/credentials",
  "root/bpmnElement/accesscontrol/authentication/persauthentication/smartcard",
  "root/bpmnElement/accesscontrol/authentication/persauthentication/biometric",
  "root/bpmnElement/privacy/confidentiality/encryption",
  "root/bpmnElement/integrity/dataintegrity/hashfunction",
  "root/bpmnElement/accountability/audittrail",
  ... // ~100+ paths extracted
]
```

**3. Build LLM Prompt with Ontology Paths**

```python
prompt = f"""
You are a BPMN security assistant.

Here is the previous conversation context:
{history_text}

The user provided this BPMN XML:
{request.modified_bpmn_xml}

These are the available ontology paths:
{available_ontologies}

First, provide a short explanation of which parts of the BPMN need
what kinds of security ontologies and why.

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

**4. LLM Analyzes BPMN Against Ontology**

The LLM:
1. Reads the BPMN XML structure
2. Identifies sensitive elements (payment, authentication, data storage)
3. Maps each element to appropriate ontology paths
4. Returns structured JSON

**Example LLM Response:**
```json
{
  "explanation": "Payment processing requires encryption and authentication.
                  User verification needs biometric authentication.
                  Order data needs integrity checks.",
  "security_ontologies": [
    {
      "elementID": "task_payment",
      "elementText": "Process Payment",
      "ontology_path": [
        "root/bpmnElement/privacy/confidentiality/encryption",
        "root/bpmnElement/accesscontrol/authentication/persauthentication/credentials",
        "root/bpmnElement/accountability/audittrail"
      ]
    },
    {
      "elementID": "task_verify",
      "elementText": "Verify User",
      "ontology_path": [
        "root/bpmnElement/accesscontrol/authentication/persauthentication/biometric",
        "root/bpmnElement/accountability/nonrepudiation/digitalsignature"
      ]
    }
  ]
}
```

**5. Response Processing**

The backend:
- Parses LLM response (handles dict or JSON string)
- Validates structure
- Logs to debug file
- Returns to Unity client

**6. Unity Conversion** (GPTManager.cs)

Unity's `ConvertSecuritySuggestionsToXml()` transforms paths to nested XML that DrawElements can visualize.

### 6.4 API Endpoints
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.post("/determine_intent")
async def determine_intent(request: IntentRequest):
    """
    Analyzes user message to determine intent:
    - create_process
    - edit_process
    - talk
    - suggest_security
    """
    # Use LLM to classify intent
    intent = llm_facade.classify_intent(
        request.message_history,
        request.model
    )
    return {"intent": intent, "confidence": 0.95}

@app.post("/modify")
async def modify_diagram(request: ModifyRequest):
    """
    Creates or modifies BPMN diagram based on user prompt
    Returns BPMN XML and JSON
    """
    bpmn_xml = bpmn_modeling_service.generate_bpmn(
        request.message_history,
        request.process,
        request.model
    )
    return {"bpmn_xml": bpmn_xml, "bpmn_json": convert_to_json(bpmn_xml)}

@app.post("/talk")
async def talk(request: TalkRequest):
    """
    Conversational endpoint for general questions
    """
    response = llm_facade.chat(
        request.message_history,
        request.model
    )
    return {"message": response}

@app.post("/suggest_security")
async def suggest_security(request: SecurityRequest):
    """
    Analyzes BPMN and suggests security ontology mappings
    """
    suggestions = llm_facade.analyze_security(
        request.modified_bpmn_xml,
        request.message_history,
        request.model
    )
    return {
        "explanation": suggestions["explanation"],
        "security_ontologies": suggestions["mappings"]
    }

@app.post("/bpmn_to_json")
async def bpmn_to_json(request: BPMNConvertRequest):
    """
    Converts BPMN XML to JSON format
    """
    return {"bpmn_json": convert_xml_to_json(request.bpmn_xml)}
```

**Request Models:**

```python
class Message(BaseModel):
    role: str
    content: str

class IntentRequest(BaseModel):
    model: str
    message_history: list[Message]
    process: list

class ModifyRequest(BaseModel):
    model: str
    message_history: list[Message]
    process: Optional[dict]

class TalkRequest(BaseModel):
    model: str
    message_history: list[Message]
    process: list
    needs_to_be_final_comment: bool

class SecurityRequest(BaseModel):
    model: str
    modified_bpmn_xml: str
    message_history: list[Message]
```

### 6.5 LLM Facade Pattern

**File Location:** `backend/llm_facade.py` (81 lines)

**Purpose:**
Unified interface to multiple LLM providers for flexibility and failover.

**Implementation:**

```python
class UnifiedLLMFacade:
    def __init__(self):
        self.providers = {
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "google": GoogleProvider(),
            "fireworks": FireworksProvider()
        }

    def detect_provider(self, model: str) -> str:
        """
        Determines LLM provider from model name
        """
        if "gpt" in model.lower():
            return "openai"
        elif "claude" in model.lower():
            return "anthropic"
        elif "gemini" in model.lower():
            return "google"
        elif "fireworks" in model.lower():
            return "fireworks"
        else:
            return "openai"  # default

    def generate(self, prompt: str, model: str) -> str:
        """
        Unified generation interface
        """
        provider_name = self.detect_provider(model)
        provider = self.providers[provider_name]
        return provider.generate(prompt, model)

    def chat(self, messages: list, model: str) -> str:
        """
        Unified chat interface
        """
        provider_name = self.detect_provider(model)
        provider = self.providers[provider_name]
        return provider.chat(messages, model)
```

### 6.6 BPMN Modeling Service

**File Location:** `backend/bpmn_modeling_service.py` (82 lines)

**Purpose:**
BPMN creation and editing using LLM integration.

**Core Method:**

```python
class BPMNModelingService:
    def __init__(self, llm_facade):
        self.llm = llm_facade

    def generate_bpmn(
        self,
        message_history: list,
        existing_process: dict,
        model: str
    ) -> str:
        """
        Generates BPMN XML from natural language description
        """
        # Construct prompt
        prompt = self._construct_prompt(message_history, existing_process)

        # Generate with LLM
        response = self.llm.generate(prompt, model)

        # Extract BPMN XML from response
        bpmn_xml = self._extract_xml(response)

        # Validate and format
        bpmn_xml = self._validate_bpmn(bpmn_xml)

        return bpmn_xml

    def _construct_prompt(self, messages, process):
        """
        Constructs detailed prompt for BPMN generation
        """
        prompt = """You are a BPMN diagram generator.
        Given a process description, generate valid BPMN 2.0 XML.

        Requirements:
        - Use standard BPMN elements (tasks, events, gateways)
        - Include proper positioning (x, y coordinates)
        - Add text labels for each element
        - Create sequence flows (arrows) between elements

        Process description:
        """

        for msg in messages:
            prompt += f"\n{msg['role']}: {msg['content']}"

        if process:
            prompt += f"\n\nExisting process:\n{process}"

        prompt += "\n\nGenerate BPMN XML:"

        return prompt
```

### 6.7 Request/Response Models

**Pydantic Validation:**

```python
from pydantic import BaseModel, Field
from typing import Optional, List

class Message(BaseModel):
    role: str = Field(..., description="Role: user or assistant")
    content: str = Field(..., description="Message content")

class IntentRequest(BaseModel):
    model: str
    message_history: List[Message]
    process: List = []

class IntentResponse(BaseModel):
    intent: str
    confidence: float

class ModifyRequest(BaseModel):
    model: str
    message_history: List[Message]
    process: Optional[dict] = None

class ModifyResponse(BaseModel):
    bpmn_xml: str
    bpmn_json: str

class SecurityRequest(BaseModel):
    model: str
    modified_bpmn_xml: str
    message_history: List[Message]

class SecurityResponse(BaseModel):
    explanation: str
    security_ontologies: List[dict]

class OntologyMapping(BaseModel):
    elementID: str
    elementText: str
    ontology_path: List[str]
```

---

## 7. cyberd3sign.com PHP Backend

### 7.1 Server Architecture

**Hosting:** cyberd3sign.com (traditional web hosting)

**Purpose:** User authentication, session management, and data persistence

**Technology Stack:**
- PHP 7.x+
- MySQL 5.7+
- Apache web server

**Note:** This is separate from the IONOS Cloud server (217.154.116.117) which handles LLM processing. The cyberd3sign.com server focuses on Unity-related functions: user login, registration, diagram storage, and database operations.

**File Structure:**

```
/cyberd3sign/
  ├── login.php
  ├── register.php
  ├── get_diagrams.php
  ├── save_diagram.php
  ├── get_security_diagrams.php
  ├── save_security.php
  └── config/
      └── database.php
```

### 7.2 Database Integration

**Connection Configuration:**

```php
<?php
// config/database.php

class Database {
    private $host = "localhost";
    private $db_name = "cyberd3sign_db";
    private $username = "cyberd3sign_user";
    private $password = "your_password";
    public $conn;

    public function getConnection() {
        $this->conn = null;

        try {
            $this->conn = new PDO(
                "mysql:host=" . $this->host .
                ";dbname=" . $this->db_name,
                $this->username,
                $this->password
            );
            $this->conn->setAttribute(
                PDO::ATTR_ERRMODE,
                PDO::ERRMODE_EXCEPTION
            );
        } catch(PDOException $exception) {
            echo "Connection error: " . $exception->getMessage();
        }

        return $this->conn;
    }
}
?>
```

**Database Schema:**

```sql
-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- BPMN diagrams table
CREATE TABLE bpmn_diagrams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    diagram_name VARCHAR(100) NOT NULL,
    bpmn_xml TEXT NOT NULL,
    screenshot LONGBLOB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Security diagrams table
CREATE TABLE security_diagrams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bpmn_diagram_id INT NOT NULL,
    security_xml TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (bpmn_diagram_id) REFERENCES bpmn_diagrams(id)
);
```

### 7.3 Data Persistence

**Login Endpoint:**

```php
<?php
// login.php

require_once 'config/database.php';

header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

$database = new Database();
$db = $database->getConnection();

$username = $_POST['username'];
$password = $_POST['password'];

$query = "SELECT id, username, password_hash FROM users
          WHERE username = :username";
$stmt = $db->prepare($query);
$stmt->bindParam(":username", $username);
$stmt->execute();

if ($stmt->rowCount() > 0) {
    $row = $stmt->fetch(PDO::FETCH_ASSOC);

    if (password_verify($password, $row['password_hash'])) {
        echo json_encode([
            "success" => true,
            "userId" => $row['id'],
            "username" => $row['username']
        ]);
    } else {
        echo json_encode([
            "success" => false,
            "message" => "Invalid credentials"
        ]);
    }
} else {
    echo json_encode([
        "success" => false,
        "message" => "User not found"
    ]);
}
?>
```

**Save Diagram Endpoint:**

```php
<?php
// save_diagram.php

require_once 'config/database.php';

header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

$database = new Database();
$db = $database->getConnection();

$user_id = $_POST['user_id'];
$diagram_name = $_POST['diagram_name'];
$bpmn_xml = $_POST['bpmn_xml'];
$screenshot = $_POST['screenshot']; // Base64 encoded

// Decode screenshot
$screenshot_binary = base64_decode($screenshot);

$query = "INSERT INTO bpmn_diagrams
          (user_id, diagram_name, bpmn_xml, screenshot)
          VALUES (:user_id, :diagram_name, :bpmn_xml, :screenshot)";

$stmt = $db->prepare($query);
$stmt->bindParam(":user_id", $user_id);
$stmt->bindParam(":diagram_name", $diagram_name);
$stmt->bindParam(":bpmn_xml", $bpmn_xml);
$stmt->bindParam(":screenshot", $screenshot_binary);

if ($stmt->execute()) {
    echo json_encode([
        "success" => true,
        "diagram_id" => $db->lastInsertId()
    ]);
} else {
    echo json_encode([
        "success" => false,
        "message" => "Failed to save diagram"
    ]);
}
?>
```

**Get Diagrams Endpoint:**

```php
<?php
// get_diagrams.php

require_once 'config/database.php';

header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

$database = new Database();
$db = $database->getConnection();

$user_id = $_GET['user_id'];
$page = isset($_GET['page']) ? intval($_GET['page']) : 0;
$limit = 10;
$offset = $page * $limit;

$query = "SELECT id, diagram_name, created_at, updated_at
          FROM bpmn_diagrams
          WHERE user_id = :user_id
          ORDER BY updated_at DESC
          LIMIT :limit OFFSET :offset";

$stmt = $db->prepare($query);
$stmt->bindParam(":user_id", $user_id);
$stmt->bindParam(":limit", $limit, PDO::PARAM_INT);
$stmt->bindParam(":offset", $offset, PDO::PARAM_INT);
$stmt->execute();

$diagrams = [];
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $diagrams[] = $row;
}

echo json_encode([
    "success" => true,
    "diagrams" => $diagrams,
    "page" => $page
]);
?>
```

---

## 8. Security Framework

### 8.1 Security Ontology

CyberD3sign implements a six-category security ontology framework:

```
root/
└── bpmnElement/
    ├── 1. Privacy/
    │   ├── confidentiality/
    │   │   ├── encryption
    │   │   ├── access_control
    │   │   └── data_masking
    │   ├── anonymization/
    │   └── consent_management/
    │
    ├── 2. Integrity/
    │   ├── data_validation/
    │   ├── checksums/
    │   ├── digital_signatures/
    │   └── version_control/
    │
    ├── 3. Availability/
    │   ├── redundancy/
    │   ├── backup/
    │   ├── load_balancing/
    │   └── disaster_recovery/
    │
    ├── 4. Authentication/
    │   ├── multi_factor_auth/
    │   ├── biometrics/
    │   ├── password_policies/
    │   └── session_management/
    │
    ├── 5. Authorization/
    │   ├── role_based_access/
    │   ├── permission_models/
    │   ├── least_privilege/
    │   └── segregation_of_duties/
    │
    └── 6. Non-Repudiation/
        ├── audit_logs/
        ├── digital_signatures/
        ├── timestamps/
        └── transaction_logging/
```

### 8.2 AI-Powered Security Suggestions

**Suggestion Generation Process:**

```
User Request: "Suggest security measures"
        ↓
GPTManager.SendToSuggestSecurity()
        ↓
FastAPI /suggest_security endpoint
        ↓
LLM analyzes BPMN elements:
  - Identifies sensitive tasks (e.g., "Process Payment")
  - Maps to security categories (e.g., encryption, authentication)
  - Generates ontology paths
        ↓
Returns JSON:
{
  "explanation": "Payment processing requires encryption...",
  "security_ontologies": [
    {
      "elementID": "task_payment",
      "elementText": "Process Payment",
      "ontology_path": [
        "root/bpmnElement/privacy/confidentiality/encryption",
        "root/bpmnElement/authentication/multi_factor_auth"
      ]
    }
  ]
}
        ↓
GPTManager.ConvertSecuritySuggestionsToXml()
        ↓
XML stored in DiagramHandler.securityRequirements
        ↓
DrawElements.DrawBPMNSecurity() visualizes
```

### 8.3 Security XML Generation

**Conversion Algorithm:**

```csharp
private string ConvertSecuritySuggestionsToXml(
    List<object> suggestions)
{
    XmlDocument xmlDoc = new XmlDocument();
    XmlElement root = xmlDoc.CreateElement("ParentTaskSecurityHolder");
    xmlDoc.AppendChild(root);

    foreach (var suggestion in suggestions)
    {
        var dict = suggestion as Dictionary<string, object>;
        string taskId = dict["elementID"].ToString();
        List<object> ontologyPaths = dict["ontology_path"] as List<object>;

        XmlElement taskHolder = xmlDoc.CreateElement("TaskSecurityHolder");
        taskHolder.SetAttribute("TaskID", taskId);

        foreach (string fullPath in ontologyPaths)
        {
            // Parse path: "root/bpmnElement/privacy/confidentiality/encryption"
            string[] tags = fullPath.Split('/');

            // Skip "root" and "bpmnElement"
            int startIndex = Array.IndexOf(tags, "bpmnElement") + 1;

            // Build nested XML: <privacy><confidentiality><encryption/>
            XmlElement currentParent = taskHolder;
            for (int i = startIndex; i < tags.Length; i++)
            {
                string tag = tags[i];

                // Check if child already exists
                XmlElement existing = null;
                foreach (XmlNode child in currentParent.ChildNodes)
                {
                    if (child.Name == tag)
                    {
                        existing = (XmlElement)child;
                        break;
                    }
                }

                if (existing == null)
                {
                    XmlElement newNode = xmlDoc.CreateElement(tag);
                    currentParent.AppendChild(newNode);
                    currentParent = newNode;
                }
                else
                {
                    currentParent = existing;
                }
            }
        }

        root.AppendChild(taskHolder);
    }

    return xmlDoc.OuterXml;
}
```

**Example Output:**

```xml
<ParentTaskSecurityHolder>
  <TaskSecurityHolder TaskID="task_payment">
    <privacy>
      <confidentiality>
        <encryption/>
      </confidentiality>
    </privacy>
    <authentication>
      <multi_factor_auth/>
    </authentication>
  </TaskSecurityHolder>

  <TaskSecurityHolder TaskID="task_review">
    <authorization>
      <role_based_access/>
    </authorization>
    <non_repudiation>
      <audit_logs/>
    </non_repudiation>
  </TaskSecurityHolder>
</ParentTaskSecurityHolder>
```

---

## 9. Data Flow and Integration

### 9.1 User Authentication Flow

```
User enters credentials
        ↓
Login.cs → LoginUser()
        ↓
UnityWebRequest → POST cyberd3sign.com/login.php
        ↓
PHP verifies credentials against MySQL
        ↓
Response: {success: true, userId: 123, username: "john"}
        ↓
SessionManager stores user data
        ↓
SceneManager.LoadScene("MainScene")
```

### 9.2 Diagram Creation Flow

**Manual Creation:**

```
User drags BPMN element from toolbar
        ↓
Instantiate prefab at mouse position
        ↓
User connects elements with arrows
        ↓
SaveHandler captures:
  - Element positions
  - Element types
  - Arrow connections
        ↓
Generate BPMN XML
        ↓
SaveHandler.saveBPMN()
        ↓
POST cyberd3sign.com/save_diagram.php
        ↓
MySQL stores diagram
```

### 9.3 LLM-Powered Diagram Generation Flow

**AI-Assisted Creation:**

```
User types: "Create a loan approval process"
        ↓
GPTManager.SendMessageToGPT()
        ↓
POST 217.154.116.117:8000/determine_intent
        ↓
Response: {intent: "create_process"}
        ↓
GPTManager.RouteByIntent() → SendToModify()
        ↓
POST 217.154.116.117:8000/modify
Body: {
  model: "gpt-4.1-nano",
  message_history: [{role: "user", content: "Create a loan approval process"}]
}
        ↓
FastAPI → BPMNModelingService.generate_bpmn()
        ↓
LLM generates BPMN XML with:
  - Start event
  - Tasks (Submit Application, Credit Check, Approval Decision)
  - Gateway (Approved?)
  - End events (Approved, Rejected)
        ↓
Response: {bpmn_xml: "<?xml version...>"}
        ↓
DiagramHandler.BPMNDiagramData = bpmn_xml
        ↓
loadLLMDiagramInstance.InitializeDiagram()
        ↓
Parse XML → Instantiate prefabs → Render diagram
```

### 9.4 Security Analysis Flow

**Complete End-to-End Security Analysis Pipeline:**

```
Step 1: User Request
User types: "suggest security" or clicks security analysis button
        ↓

Step 2: Intent Detection (GPTManager.cs)
GPTManager.SendMessageToGPT("suggest security")
        ↓
POST http://217.154.116.117:8000/determine_intent
Body: {
  model: "gpt-4.1-nano",
  message_history: [{role: "user", content: "suggest security"}],
  process: []
}
        ↓
Response: {intent: "suggest_security", confidence: 0.95}
        ↓

Step 3: Route to Security Handler (GPTManager.cs:76-103)
RouteByIntent("suggest_security") → SendToSuggestSecurity()
        ↓

Step 4: Call LLM Backend (GPTManager.cs:187-265)
POST http://217.154.116.117:8000/suggest_security
Body: {
  model: "gpt-4.1-nano",
  modified_bpmn_xml: DiagramHandler.BPMNDiagramData,
  message_history: [...]
}
        ↓

Step 5: LLM Analysis (IONOS Cloud FastAPI Server)
- Parse BPMN XML structure
- Identify sensitive elements (e.g., "Process Payment", "Verify Identity")
- Analyze business logic and data flows
- Map to 6-category security ontology
- Generate ontology paths for each element
        ↓

Response: {
  explanation: "Payment processing requires encryption and authentication...",
  security_ontologies: [
    {
      elementID: "task_payment",
      elementText: "Process Payment",
      ontology_path: [
        "root/bpmnElement/privacy/confidentiality/encryption",
        "root/bpmnElement/accesscontrol/authentication/mfa"
      ]
    },
    {
      elementID: "task_verify",
      elementText: "Verify Identity",
      ontology_path: [
        "root/bpmnElement/accesscontrol/authentication/biometric",
        "root/bpmnElement/accountability/audit/accesslog"
      ]
    }
  ]
}
        ↓

Step 6: Convert to Hierarchical XML (GPTManager.cs:267-326)
ConvertSecuritySuggestionsToXml(security_ontologies)

For each element and ontology path:
  - Parse path: "root/bpmnElement/privacy/confidentiality/encryption"
  - Skip "root" and "bpmnElement" prefixes
  - Build nested XML structure

Generated XML:
<ParentTaskSecurityHolder>
  <TaskSecurityHolder TaskID="task_payment">
    <privacy>
      <confidentiality>
        <encryption/>
      </confidentiality>
    </privacy>
    <accesscontrol>
      <authentication>
        <mfa/>
      </authentication>
    </accesscontrol>
  </TaskSecurityHolder>

  <TaskSecurityHolder TaskID="task_verify">
    <accesscontrol>
      <authentication>
        <biometric/>
      </authentication>
    </accesscontrol>
    <accountability>
      <audit>
        <accesslog/>
      </audit>
    </accountability>
  </TaskSecurityHolder>
</ParentTaskSecurityHolder>
        ↓

Step 7: Store Security Requirements (GPTManager.cs:251-253)
DiagramHandler.securityRequirements = mergedSecurityXml;
DrawElements.Instance().DrawBPMNSecurity();
        ↓

Step 8: Visualize Security Symbols (DrawElements.cs:169-299)
DrawBPMNSecurity() {
  - Clear existing security visualizations
  - Parse security XML
  - For each TaskSecurityHolder:
    - Find BPMN element by TaskID
    - Calculate position above element
    - Draw vertical line (pos1 to pos1 + 390 units)
    - Render 4-level symbol hierarchy:
      * Level 1: privacy, accesscontrol (main category)
      * Level 2: confidentiality, authentication (sub-category)
      * Level 3: encryption, mfa, biometric (control)
      * Level 4: AES256, TOTP, fingerprint (implementation)
}
        ↓

Step 9: Display to User
Visual security overlay appears on diagram:
- Vertical lines above secure elements
- Stacked security symbols showing requirements
- User can click symbols for details
- Security requirements saved with diagram
```

**Key Components:**

| Component | Responsibility |
|-----------|---------------|
| GPTManager.cs | Orchestrates security analysis request |
| IONOS Cloud FastAPI | LLM analysis and ontology mapping |
| ConvertSecuritySuggestionsToXml() | Transforms ontology paths to XML |
| DiagramHandler.securityRequirements | Stores security XML data |
| DrawElements.DrawBPMNSecurity() | Renders visual security symbols |
| symbol.cs | Individual security symbol rendering |
| taskSecurityLines.cs | Vertical line rendering |

---

## 10. Technical Implementation Details

### 10.1 Coroutine-Based Async Operations

Unity uses coroutines for asynchronous operations:

```csharp
// Starting a coroutine
StartCoroutine(DetermineIntent(userMessage));

// Coroutine implementation
private IEnumerator DetermineIntent(string userMessage)
{
    // Prepare request
    UnityWebRequest request = ...;

    // Yield until request completes
    yield return request.SendWebRequest();

    // Process response
    if (request.result == UnityWebRequest.Result.Success)
    {
        // Handle success
    }
}
```

**Benefits:**
- Non-blocking I/O for network requests
- Smooth UI during long operations
- Sequential async code without callbacks

### 10.2 XML Document Processing

**XML Parsing Patterns:**

```csharp
// Load XML from string
XmlDocument xmlDoc = new XmlDocument();
xmlDoc.LoadXml(xmlString);

// Query by tag name
XmlNodeList shapes = xmlDoc.GetElementsByTagName("BPMNShape");

// Iterate nodes
foreach (XmlNode shape in shapes)
{
    // Access attributes
    string id = shape.Attributes["id"].Value;

    // Access child elements
    XmlNode bounds = shape.FirstChild;
    float height = float.Parse(bounds.Attributes["height"].Value);
}

// Create new elements
XmlElement newElement = xmlDoc.CreateElement("TaskSecurityHolder");
newElement.SetAttribute("TaskID", "task_1");
xmlDoc.AppendChild(newElement);

// Serialize to string
string xmlOutput = xmlDoc.OuterXml;
```

### 10.3 Scaling and Layout Algorithms

**Scale Factor Calculation:**

```csharp
// LLM-generated diagrams use large coordinates (e.g., 800x600 canvas)
// Unity 3D space typically uses smaller units (e.g., 10x10 visible area)

private const float scaleFactor = 0.26f;

// Apply to all coordinates
float scaledX = originalX * scaleFactor;
float scaledY = originalY * scaleFactor;
float scaledWidth = originalWidth * scaleFactor;
float scaledHeight = originalHeight * scaleFactor;
```

**Why 0.26?**
- Standard BPMN coordinates: ~800x600 canvas, 100x80 elements
- Unity visible area: ~200x150 units
- Ratio: 200/800 = 0.25, tuned to 0.26 for optimal spacing

**Gateway Arrow Distribution:**

```csharp
// Distribute arrows to avoid overlap
string[] positions = { "locationRight", "locationBottom", "locationTop" };

for (int i = 0; i < outgoingArrows.Count; i++)
{
    string position = positions[i % 3];
    outgoingArrows[i].startPosition = position;
}
```

**Arrow Path Optimization:**

```csharp
// Simplify arrow paths with intermediate waypoints
List<vertexPosition> positions = new List<vertexPosition>();

// Start point (element edge)
positions.Add(new vertexPosition(0, startX, startY));

// Optional: Add midpoint for curved arrows
if (needsCurve)
{
    float midX = (startX + endX) / 2;
    float midY = (startY + endY) / 2 + curveOffset;
    positions.Add(new vertexPosition(1, midX, midY));
}

// End point (target element edge)
positions.Add(new vertexPosition(positions.Count, endX, endY));
```

---

## 11. Deployment and Infrastructure

### 11.1 Server Configuration

**Server 1 - IONOS Cloud (LLM Backend):**
- **Server IP:** 217.154.116.117
- **Port:** 8000
- **Protocol:** HTTP
- **Framework:** FastAPI (Python 3.12)
- **Deployment:** Docker or systemd service on IONOS Cloud
- **Purpose:** AI processing with stored LLM API keys
- **API Keys:** OpenAI, Anthropic, Google, Fireworks (server-side storage)
- **Cost Savings:** No GPU infrastructure needed

**Server 2 - cyberd3sign.com (Data Backend):**
- **Domain:** cyberd3sign.com
- **Hosting:** Traditional web hosting
- **Server:** Apache
- **Database:** MySQL 5.7+
- **SSL:** HTTPS enabled
- **Purpose:** User authentication, diagram storage, web hosting

### 11.2 API Endpoints

**Server 1 - IONOS Cloud FastAPI (217.154.116.117:8000):**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /determine_intent | POST | Intent classification using LLM |
| /modify | POST | BPMN generation/editing via LLM |
| /talk | POST | Conversational interface with LLM |
| /suggest_security | POST | Security analysis using LLM |
| /bpmn_to_json | POST | XML to JSON conversion |

**Server 2 - cyberd3sign.com PHP:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| /login.php | POST | User authentication |
| /register.php | POST | User registration |
| /get_diagrams.php | GET | Fetch user diagrams from MySQL |
| /save_diagram.php | POST | Save BPMN diagram to MySQL |
| /get_security_diagrams.php | GET | Fetch security diagrams |
| /save_security.php | POST | Save security mappings |

### 11.3 Environment Management

**Unity Build Configuration:**

```csharp
public class ServerConnection
{
    #if UNITY_EDITOR
    public static string currentServer = localhostServer;
    #else
    public static string currentServer = productionServer;
    #endif

    public static string localhostServer = "http://localhost/cyberd3sign/";
    public static string productionServer = "https://cyberd3sign.com/";
}
```

**FastAPI Environment Variables (IONOS Cloud Server):**

```python
import os

# LLM API Keys (stored on IONOS Cloud server)
# These keys enable AI functionality without GPU infrastructure
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
DEBUG = os.getenv("DEBUG", "False") == "True"
```

**Key Benefits:**
- API keys stored server-side on IONOS Cloud
- Unity client never handles LLM credentials
- No GPU infrastructure costs
- Pay-per-API-call pricing model

**Docker Deployment (Likely Configuration):**

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Appendix A: Complete Code Reference

### A.1 GPTManager.cs Key Methods

**File:** `CyberD3signUnity/Assets/Scripts/BPMN Engine/GPTManager.cs` (369 lines)

**Public Methods:**
- `SendMessageToGPT(string userMessage)` - Entry point for all user interactions

**Private Methods:**
- `DetermineIntent(string userMessage)` - Intent classification via LLM
- `RouteByIntent(string intent, string message)` - Routes to appropriate handler
- `SendToModify(string userPrompt)` - BPMN creation/editing
- `SendToTalk(string userPrompt)` - Conversational responses
- `SendToSuggestSecurity()` - Security analysis
- `ConvertSecuritySuggestionsToXml(List<object> suggestions)` - XML conversion

### A.2 loadLLMDiagram.cs Key Methods

**File:** `CyberD3signUnity/Assets/Scripts/BPMN Engine/loadLLMDiagram.cs` (1000 lines)

**Public Methods:**
- `InitializeDiagram()` - Main rendering entry point

**Private Methods:**
- `AdjustGatewayArrowPositions(XmlDocument xmlDoc)` - Arrow layout optimization
- `NormalizeElementType(string rawType)` - Type name mapping
- `GetPrefabPath(string elementType)` - Prefab path resolution
- `IsStaticElement(string elementId)` - Static element filtering

### A.3 loadBPMNDiagram.cs Key Methods

**File:** `CyberD3signUnity/Assets/Scripts/BPMN Engine/loadBPMNDiagram.cs` (142 lines)

**Public Methods:**
- `Start()` - Unity lifecycle initialization

**Processing Flow:**
1. Load XML from DiagramHandler
2. Parse BPMNShape elements
3. Instantiate prefabs
4. Parse BPMNEdge elements
5. Create arrow connections

---

## Appendix B: API Documentation

### B.1 FastAPI Endpoints

**POST /determine_intent**

Request:
```json
{
  "model": "gpt-4.1-nano",
  "message_history": [
    {"role": "user", "content": "Create a purchase order process"}
  ],
  "process": []
}
```

Response:
```json
{
  "intent": "create_process",
  "confidence": 0.95
}
```

**POST /modify**

Request:
```json
{
  "model": "gpt-4.1-nano",
  "message_history": [
    {"role": "user", "content": "Create a purchase order process"}
  ],
  "process": null
}
```

Response:
```json
{
  "bpmn_xml": "<?xml version=\"1.0\"?><root>...</root>",
  "bpmn_json": "{...}"
}
```

**POST /suggest_security**

Request:
```json
{
  "model": "gpt-4.1-nano",
  "modified_bpmn_xml": "<root><BPMNShape>...</BPMNShape></root>",
  "message_history": []
}
```

Response:
```json
{
  "explanation": "Payment processing requires encryption and authentication...",
  "security_ontologies": [
    {
      "elementID": "task_payment",
      "elementText": "Process Payment",
      "ontology_path": [
        "root/bpmnElement/privacy/confidentiality/encryption",
        "root/bpmnElement/authentication/multi_factor_auth"
      ]
    }
  ]
}
```

### B.2 IONOS PHP Endpoints

**POST /login.php**

Request (Form Data):
```
username=john
password=secure123
```

Response:
```json
{
  "success": true,
  "userId": 123,
  "username": "john"
}
```

**GET /get_diagrams.php**

Request:
```
?user_id=123&page=0
```

Response:
```json
{
  "success": true,
  "diagrams": [
    {
      "id": 1,
      "diagram_name": "Purchase Order Process",
      "created_at": "2025-10-15 14:30:00",
      "updated_at": "2025-10-16 09:15:00"
    }
  ],
  "page": 0
}
```

---

## Appendix C: Security Ontology Reference

### C.1 Complete Ontology Tree

```
root/bpmnElement/
│
├── privacy/
│   ├── confidentiality/
│   │   ├── encryption
│   │   ├── access_control
│   │   ├── data_masking
│   │   └── secure_communication
│   ├── anonymization/
│   │   ├── data_anonymization
│   │   └── pseudonymization
│   └── consent_management/
│       ├── user_consent
│       └── consent_tracking
│
├── integrity/
│   ├── data_validation/
│   │   ├── input_validation
│   │   └── schema_validation
│   ├── checksums/
│   ├── digital_signatures/
│   └── version_control/
│
├── availability/
│   ├── redundancy/
│   │   ├── server_redundancy
│   │   └── data_redundancy
│   ├── backup/
│   │   ├── regular_backup
│   │   └── offsite_backup
│   ├── load_balancing/
│   └── disaster_recovery/
│
├── authentication/
│   ├── multi_factor_auth/
│   │   ├── two_factor
│   │   └── biometric
│   ├── biometrics/
│   ├── password_policies/
│   │   ├── complexity_requirements
│   │   └── rotation_policy
│   └── session_management/
│       ├── timeout
│       └── secure_cookies
│
├── authorization/
│   ├── role_based_access/
│   │   ├── rbac
│   │   └── abac
│   ├── permission_models/
│   ├── least_privilege/
│   └── segregation_of_duties/
│
└── non_repudiation/
    ├── audit_logs/
    │   ├── access_logs
    │   └── transaction_logs
    ├── digital_signatures/
    ├── timestamps/
    └── transaction_logging/
```

### C.2 Ontology Mapping Examples

**Task: "Process Payment"**

Suggested Security Mappings:
- `root/bpmnElement/privacy/confidentiality/encryption` - Encrypt payment data
- `root/bpmnElement/authentication/multi_factor_auth` - Require MFA for high-value transactions
- `root/bpmnElement/integrity/digital_signatures` - Sign transaction records
- `root/bpmnElement/non_repudiation/audit_logs` - Log all payment attempts

**Task: "Access Customer Records"**

Suggested Security Mappings:
- `root/bpmnElement/authorization/role_based_access` - Restrict to authorized personnel
- `root/bpmnElement/privacy/confidentiality/access_control` - Implement access controls
- `root/bpmnElement/non_repudiation/audit_logs/access_logs` - Log all record accesses
- `root/bpmnElement/authentication/session_management` - Secure session handling

---

## Appendix D: Design Pattern Catalog

### D.1 Facade Pattern

**Implementation:** `llm_facade.py`

**Purpose:** Provide unified interface to multiple LLM providers

**Benefits:**
- Single point of integration for client code
- Easy to add new providers
- Provider-specific logic encapsulated

### D.2 Singleton Pattern

**Implementation:** `DiagramHandler.cs` (static variables)

**Purpose:** Global state management for diagram data

**Benefits:**
- Single source of truth
- Accessible from any component
- No need to pass references

### D.3 Factory Pattern

**Implementation:** Prefab instantiation in loadBPMNDiagram and loadLLMDiagram

**Purpose:** Dynamic GameObject creation based on element type

**Benefits:**
- Centralized object creation logic
- Easy to add new element types
- Type-safe instantiation

### D.4 Repository Pattern

**Implementation:** SaveHandler and DiagramHandler

**Purpose:** Abstract data persistence and retrieval

**Benefits:**
- Separation of data access from business logic
- Easy to swap storage backends
- Consistent interface for CRUD operations

---

## Appendix E: Glossary

**BPMN** - Business Process Model and Notation, a standard for business process diagrams

**Coroutine** - Unity's mechanism for asynchronous operations using yield statements

**DiagramHandler** - Static class managing global diagram state

**FastAPI** - Modern Python web framework for building APIs

**Gateway** - BPMN decision point with multiple outgoing paths

**GPTManager** - Component orchestrating LLM interactions

**IONOS** - Web hosting provider for PHP backend

**loadBPMNDiagram** - Component for rendering user-created diagrams

**loadLLMDiagram** - Component for rendering AI-generated diagrams with scaling

**LLM** - Large Language Model (GPT, Claude, Gemini)

**Ontology** - Structured framework for categorizing security requirements

**Prefab** - Unity template for GameObject instantiation

**Scale Factor** - 0.26 multiplier applied to LLM-generated coordinates

**UnityWebRequest** - Unity's HTTP client for REST API calls

**XML** - Extensible Markup Language used for BPMN storage

---

## Document Conclusion

This comprehensive technical architecture report documents the complete CyberD3sign application, including the previously missing components:

1. **GPTManager.cs** - AI orchestration layer with intent detection, multi-endpoint routing, and security suggestion processing
2. **loadLLMDiagram.cs** - Specialized rendering for AI-generated diagrams with automatic scaling and layout optimization
3. **loadBPMNDiagram.cs** - Standard BPMN diagram loading and rendering

The application represents a sophisticated integration of:
- **Unity 3D** for visualization
- **AI/LLM** for natural language processing
- **FastAPI** for intelligent backend services
- **PHP/MySQL** for data persistence
- **Multi-tier architecture** for scalability

**Key Technical Achievements:**
- Intent-based conversational interface
- Multi-provider LLM abstraction
- Automatic diagram scaling (0.26x factor)
- Six-category security ontology framework
- Real-time security analysis and visualization
- Hybrid architecture with dual backends

**Version:** 2.0 - Complete
**Date:** October 16, 2025
**Status:** Final with Full Component Coverage
