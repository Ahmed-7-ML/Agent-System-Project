# 🤖 Agent System Project
> **An Intelligent Multi-Agent Research & Writing System**  
> Built with LangGraph · CrewAI · FastAPI · n8n

---

## 📌 Overview

A production-ready AI system that automates research and content writing through a pipeline of intelligent agents. Send a task via **n8n**, and the system will automatically research the topic on the internet and deliver a well-structured report — all without human intervention.

```
n8n Webhook  →  FastAPI  →  LangGraph  →  CrewAI Agents  →  Report ✅
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        n8n Workflow                      │
│  Webhook → HTTP Request → Edit Fields                   │
└─────────────────────┬───────────────────────────────────┘
                      │ POST /n8n_request
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    FastAPI (uvicorn)                     │
│              POST /n8n_request endpoint                  │
└─────────────────────┬───────────────────────────────────┘
                      │ invoke(state)
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  LangGraph Workflow                      │
│                                                          │
│   ┌─────────────┐         ┌─────────────────┐           │
│   │ router_node │ ──────► │  crewai_node    │           │
│   │             │         │                 │           │
│   │ Decides     │         │ Runs CrewAI     │           │
│   │ which agent │         │ Crew            │           │
│   └─────────────┘         └────────┬────────┘           │
│                                    │                     │
└────────────────────────────────────┼────────────────────┘
                                     │
                      ▼              ▼
┌─────────────────────────────────────────────────────────┐
│                    CrewAI Agents                         │
│                                                          │
│  🔍 Senior Research Analyst                             │
│     └── SerperDevTool (Google Search)                   │
│            └── Top 10 insights about topic              │
│                                                          │
│  ✍️  Professional Content Writer                        │
│     └── Context from Researcher                         │
│            └── Well-structured report                   │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

- 🔍 **Automated Research** — Searches Google in real-time using SerperDev API
- ✍️ **Intelligent Writing** — Transforms research into structured reports
- 🔄 **Smart Routing** — LangGraph routes tasks to the right agent automatically
- 🌐 **REST API** — FastAPI endpoint ready for any external integration
- 🤖 **n8n Integration** — Low-code workflow automation out of the box
- 🆓 **Free LLM** — Powered by Groq's Llama 3.3 70B (no cost!)
- 📄 **Auto-save Reports** — Results saved to `reports/report.md`

---

## 🛠️ Tech Stack

| Tool | Role | Why |
|------|------|-----|
| **FastAPI** | API Gateway | Receives requests from n8n |
| **uvicorn** | ASGI Server | Runs FastAPI on a port |
| **LangGraph** | Orchestrator | Manages state & workflow |
| **CrewAI** | Agent Framework | Runs research & writing agents |
| **Groq** | LLM Provider | Free, fast Llama 3.3 70B |
| **SerperDev** | Search Tool | Google Search API |
| **n8n** | Automation | Low-code workflow trigger |
| **Poetry** | Package Manager | Dependency management |
| **python-dotenv** | Config | Loads API keys from .env |
| **LiteLLM** | LLM Bridge | Connects CrewAI with Groq |

---

## 📁 Project Structure

```
agent-system-project/
│
├── src/
│   └── agent_system_project/
│       ├── __init__.py
│       ├── main.py          # FastAPI app & endpoint
│       ├── graph.py         # LangGraph workflow & nodes
│       └── crew.py          # CrewAI agents & tasks
│
├── reports/
│   └── report.md            # Auto-generated reports
│
├── .env                     # API Keys (not committed)
├── .gitignore
├── pyproject.toml           # Poetry dependencies
└── README.md
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python `>=3.11, <3.14`
- Poetry `>=2.4.0`
- Node.js (for n8n)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/agent-system-project.git
cd agent-system-project
```

### 2️⃣ Configure Poetry Cache (Windows)
```powershell
poetry config cache-dir "E:\\PoetryCache"
poetry config virtualenvs.path "E:\\PoetryCache\\virtualenvs"
```

### 3️⃣ Install Dependencies
```powershell
$env:TEMP = "E:\Temp"
$env:TMP = "E:\Temp"
poetry install
```

### 4️⃣ Set Up Environment Variables
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=gsk_your_key_here
SERPER_API_KEY=your_serper_key_here
```

Get your API keys from:
- 🔑 Groq: [console.groq.com](https://console.groq.com)
- 🔑 Serper: [serper.dev/api-keys](https://serper.dev/api-keys)

### 5️⃣ Run the Server
```bash
poetry run uvicorn src.agent_system_project.main:app --reload --port 8080
```

---

## 🚀 Usage

### Via FastAPI Swagger UI
Open your browser at:
```
http://127.0.0.1:8080/docs
```

Send a POST request:
```json
{
  "task": "Write a report about OpenAI company",
  "output_format": "A 10-line report"
}
```

### Via curl (Linux/Mac)
```bash
curl -X POST http://127.0.0.1:8080/n8n_request \
  -H "Content-Type: application/json" \
  -d '{"task": "Write about OpenAI", "output_format": "10-line report"}'
```

### Via PowerShell (Windows)
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8080/n8n_request" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"task": "Write about OpenAI", "output_format": "10-line report"}'
```

### Expected Response
```json
{
  "status": "received",
  "task": "Write about OpenAI",
  "output_format": "10-line report",
  "result": "Report: The Rise of OpenAI..."
}
```

---

## 🔄 n8n Workflow Setup

### Workflow Structure
```
Webhook → HTTP Request → Edit Fields
```

### Node Configuration

**Webhook Node:**
```
HTTP Method: POST
Path: /agent-request
Respond: When Last Node Finishes
```

**HTTP Request Node:**
```
Method: POST
URL: http://localhost:8080/n8n_request
Body: Using Fields Below
  - task: {{ $json.body.task }}
  - output_format: {{ $json.body.output_format }}
```

**Edit Fields Node:**
```
Result: {{ $json.result }}
```

---

## 🧠 How It Works

```
1. n8n receives a POST request with task & output_format
2. n8n forwards it to FastAPI via HTTP Request
3. FastAPI invokes the LangGraph workflow
4. router_node analyzes the task and selects the right agent
5. crewai_node runs the CrewAI crew
6. Research Agent searches Google for top 10 insights
7. Writer Agent transforms insights into a structured report
8. Result is saved to reports/report.md
9. FastAPI returns only the final report text
10. n8n delivers the result
```

---

## 🤖 Agents

### 🔍 Senior Research Analyst
```
Role: Senior Research Analyst
Goal: Extract top 10 insights about any given topic
Tools: SerperDevTool (Google Search)
LLM:  Groq Llama 3.3 70B
```

### ✍️ Professional Content Writer
```
Role: Professional Content Writer
Goal: Write well-organized reports based on research
Tools: None (uses researcher's context)
LLM:  Groq Llama 3.3 70B
```

---

## 📊 LangGraph State

```python
class AgentState(TypedDict):
    task: str           # The research/writing task
    output_format: str  # Desired output format
    agent: str          # Selected agent (set by router)
    crew_result: str    # Final output (set by crew)
```

---

## ⚠️ Known Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| `No space left on device` | C: drive full | Move Poetry cache to E: drive |
| `ModuleNotFoundError` | Wrong import style | Use relative imports (`.module`) |
| `LLM ValidationError` | Wrong LLM class | Use `crewai.LLM` not `ChatGroq` |
| `LiteLLM not installed` | Missing package | `poetry add litellm` |
| `Port 8000 forbidden` | Port in use | Use `--port 8080` |
| `JSON decode error` | Arabic encoding | Use "Fields Below" in n8n |

---

## 🔮 Future Improvements

- [ ] Add MCP (Model Context Protocol) for local data access
- [ ] Add more specialized agents (Data Analyst, Code Writer)
- [ ] Add AgentOps for monitoring & cost tracking
- [ ] Add memory/persistence between sessions
- [ ] Deploy to production server
- [ ] Add authentication to the API

---

## 📝 License

MIT License — feel free to use, modify, and distribute.

---

## 👨‍💻 Author

**Ahmed Akram Amer**  
3AI Company  
Built with ❤️ using LangGraph, CrewAI, FastAPI & n8n
