# Financial Document Analyzer

A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents built with [CrewAI](https://www.crewai.com/).

## Table of Contents

- [Overview](#overview)
- [Bugs Found & Fixed](#bugs-found--fixed)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [Architecture](#architecture)

---

## Overview

This system accepts PDF financial documents (e.g., Tesla's Q2 2025 quarterly report) via a REST API and runs a multi-agent AI pipeline to produce:

- **Document verification** — confirms the upload is a valid financial report
- **Financial analysis** — extracts key metrics, trends, and notable findings
- **Investment recommendations** — provides data-driven investment insights
- **Risk assessment** — evaluates financial, market, and operational risks

---

## Bugs Found & Fixed

### Deterministic Bugs

| # | File | Bug | Fix |
|---|------|-----|-----|
| 1 | `tools.py` | `from crewai_tools import tools` — `tools` is not a valid export | Changed to `from crewai.tools import tool` (the `@tool` decorator) |
| 2 | `tools.py` | `Pdf(file_path=path).load()` — `Pdf` is undefined, no PDF library imported | Replaced with `pypdf.PdfReader` for proper PDF text extraction |
| 3 | `tools.py` | `read_data_tool` is `async` — CrewAI tools don't support async functions | Converted to a synchronous function |
| 4 | `tools.py` | `read_data_tool` is a class method without `@tool` decorator | Converted to standalone function with `@tool` decorator |
| 5 | `agents.py` | `from crewai.agents import Agent` — wrong import path | Changed to `from crewai import Agent` |
| 6 | `agents.py` | `llm = llm` — self-referencing undefined variable | Initialized actual LLM: `LLM(model="gemini/gemini-2.0-flash")` |
| 7 | `agents.py` | `tool=[...]` — wrong parameter name (singular) | Changed to `tools=[...]` (plural) |
| 8 | `agents.py` | `max_iter=1`, `max_rpm=1` — too restrictive for agents to reason | Increased to `max_iter=5`, `max_rpm=10` |
| 9 | `agents.py` | `allow_delegation=True` — causes issues with no viable delegate | Set to `False` on all agents |
| 10 | `main.py` | Endpoint function `analyze_financial_document` shadows the imported task of the same name | Renamed endpoint to `analyze_document_endpoint` |
| 11 | `main.py` | `file_path` generated but never passed to crew inputs | Added `file_path` to `crew.kickoff()` input dict |
| 12 | `main.py` | Only 1 agent and 1 task registered in `Crew(...)` | Added all 4 agents and 4 tasks |
| 13 | `main.py` | `uvicorn.run(app, ..., reload=True)` — reload requires string import | Changed to `uvicorn.run("main:app", ...)` |
| 14 | `task.py` | `verification` task assigned to `financial_analyst` instead of `verifier` agent | Assigned to correct `verifier` agent |
| 15 | `task.py` | `investment_analysis` and `risk_assessment` both assigned to `financial_analyst` | Assigned to `investment_advisor` and `risk_assessor` respectively |
| 16 | `requirements.txt` | Missing `uvicorn` — can't run the server | Added `uvicorn` |
| 17 | `requirements.txt` | Missing `python-dotenv` — `load_dotenv()` fails | Added `python-dotenv` |
| 18 | `requirements.txt` | Missing `pypdf` — no PDF reading capability | Added `pypdf` |
| 19 | `requirements.txt` | Missing `python-multipart` — FastAPI file uploads fail | Added `python-multipart` |
| 20 | `requirements.txt` | Missing `litellm` — required by `crewai.LLM` | Added `litellm` |
| 21 | `README.md` | `pip install -r requirement.txt` — filename typo | Fixed to `requirements.txt` |
| 22 | `task.py` | `{file_path}` not injected into task descriptions | Added `{file_path}` to all tasks to ensure agents read the correct file | [diff_block_end]

### Inefficient / Sabotaged Prompts

All agent and task prompts were intentionally written to produce harmful, inaccurate output:

| File | Issue | Fix |
|------|-------|-----|
| `agents.py` | All agent `role`, `goal`, and `backstory` fields encouraged fabrication, non-compliance, and fake data | Rewrote with professional personas emphasizing accuracy, data-driven analysis, and regulatory compliance |
| `task.py` | All task `description` and `expected_output` fields instructed agents to hallucinate, make up URLs, contradict themselves, and ignore user queries | Rewrote with clear, structured instructions that focus on the actual document data and user query |

---

## Setup Instructions

### Prerequisites

- Python 3.10+
- A Google Gemini API key (get one at [Google AI Studio](https://aistudio.google.com/))

### Installation

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd financial-document-analyzer-debug
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or: venv\Scripts\activate  # Windows
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```sh
   # Create a .env file in the project root
   echo "GEMINI_API_KEY=your_api_key_here" > .env

   # Optional: for internet search functionality
   echo "SERPER_API_KEY=your_serper_key_here" >> .env
   ```

5. **Add a sample financial document:**
   - Download Tesla's Q2 2025 report: https://www.tesla.com/sites/default/files/downloads/TSLA-Q2-2025-Update.pdf
   - Save it as `data/sample.pdf`

### Running the Server

```sh
python main.py
```

The API server starts at `http://localhost:8000`.

---

## API Documentation

### Health Check

```
GET /
```

**Response:**
```json
{
  "message": "Financial Document Analyzer API is running"
}
```

### Analyze Document

```
POST /analyze
```

**Parameters (multipart/form-data):**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `file` | File (PDF) | Yes | The financial document to analyze |
| `query` | String | No | Specific analysis question (default: "Analyze this financial document for investment insights") |

**Example Request:**
```sh
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@data/sample.pdf" \
  -F "query=What are the key revenue trends and risk factors?"
```

**Example Response:**
```json
{
  "status": "success",
  "query": "What are the key revenue trends and risk factors?",
  "analysis": "...",
  "file_processed": "sample.pdf"
}
```

**Error Response (500):**
```json
{
  "detail": "Error processing financial document: <error message>"
}
```

---

## Architecture

The system uses a **sequential multi-agent pipeline** powered by CrewAI:

```
Upload PDF → Verifier → Financial Analyst → Investment Advisor → Risk Assessor → Response
```

| Agent | Role |
|-------|------|
| **Verifier** | Validates the document is a real financial report |
| **Financial Analyst** | Extracts key metrics, trends, and financial insights |
| **Investment Advisor** | Provides investment recommendations based on the analysis |
| **Risk Assessor** | Evaluates financial, market, and operational risks |

### File Structure

```
├── main.py              # FastAPI server and crew orchestration
├── agents.py            # Agent definitions with LLM configuration
├── task.py              # Task definitions for the analysis pipeline
├── tools.py             # PDF reader tool and search tool
├── requirements.txt     # Python dependencies
├── data/                # Directory for uploaded/sample PDFs
│   └── sample.pdf       # Sample financial document
└── .env                 # API keys (not committed)
```
