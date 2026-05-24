# 🚀 AI Blog Writer Agent

A multi-agent AI blog generation system built using LangGraph, LangChain, OpenAI, Tavily, Gemini Image Generation, and Streamlit.

The system uses an agentic workflow architecture with:
- intelligent routing
- research-aware planning
- parallel workers
- reducer pipelines
- automated technical image generation

to generate high-quality technical blogs.

---

# ✨ Features

- Intelligent Router (Closed-book / Hybrid / Open-book)
- Tavily-powered web research
- Parallel section generation using LangGraph workers
- Evidence-grounded content generation
- Automated technical diagram generation
- Reducer-based aggregation pipeline
- Streamlit frontend UI
- Markdown export support
- Structured outputs using Pydantic

---

# 🧠 Architecture

```text
                ┌──────────────┐
                │    START     │
                └──────┬───────┘
                       │
                ┌──────▼──────┐
                │   Router    │
                └──────┬──────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
 ┌──────▼──────┐              ┌───────▼────────┐
 │  Research   │              │  Orchestrator  │
 └──────┬──────┘              └───────┬────────┘
        │                              │
        └──────────────┬──────────────┘
                       │
                ┌──────▼──────┐
                │   Workers   │
                │ (Parallel)  │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │   Reducer   │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │  Final Blog │
                └─────────────┘
```

---

# ⚡ Tech Stack

- Python
- LangGraph
- LangChain
- OpenAI GPT-4o-mini
- Tavily Search API
- Gemini Image API
- Streamlit
- Pydantic

---

# 🔥 Core Concepts Used

- Agentic Workflows
- StateGraph Orchestration
- Conditional Routing
- Fanout / Fanin Patterns
- Parallel Workers
- Reducer Pipelines
- Structured Outputs
- Evidence Grounding

---

# 📂 Project Structure

```text
.
├── app.py
├── blog_writer.py
├── images/
├── requirements.txt
├── .env
└── README.md
```

---

# 🔧 Installation

## Clone Repository

```bash
git clone <your_repo_url>
cd ai-blog-writer
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_api_key
```

---

# ▶️ Run Application

```bash
streamlit run app.py
```

---

# ⚙️ Workflow

## Router
Determines whether the topic needs:
- closed-book generation
- hybrid generation
- open-book research

---

## Research Layer
Fetches fresh evidence using Tavily Search.

---

## Orchestrator
Creates:
- blog outline
- tasks
- goals
- section constraints

---

## Parallel Workers
Generates blog sections independently using LangGraph fanout patterns.

---

## Reducer
- merges sections
- plans diagrams/images
- generates visuals
- produces final markdown blog

---

# 📸 Screenshots

Add:
- Streamlit UI
- LangGraph graph visualization
- Generated blog examples

---

# 🚀 Future Improvements

- LangSmith tracing
- Streaming responses
- Human-in-the-loop review
- Vector retrieval
- PDF export

---

# 👨‍💻 Author

Suraj Dhakad

---

# 📜 License

MIT License