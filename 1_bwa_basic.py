from __future__ import annotations
import os
import operator
from typing import TypedDict, List, Annotated
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()



class Task(BaseModel):
    id: int
    title: str
    brief: str = Field(..., description="What to cover")


class Plan(BaseModel):
    blog_title: str
    tasks: List[Task]

class State(TypedDict):
    topic: str
    plan: Plan
    # reducer: results from workers get concatenated automatically
    sections: Annotated[List[str], operator.add]
    final: str


# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("⚠️  WARNING: OPENAI_API_KEY not set. Using demo mode with mock responses.")
    print("To use real API, set: $env:OPENAI_API_KEY = 'your-key-here'")
    print()
    # Create a mock LLM for testing
    class MockLLM:
        def __init__(self, model=None, api_key=None):
            self.model = model
            
        def with_structured_output(self, schema):
            return self
            
        def invoke(self, messages):
            # Return mock Plan
            return Plan(
                blog_title="Self Attention in Transformers",
                tasks=[
                    Task(id=1, title="Introduction", brief="Overview of self attention concept"),
                    Task(id=2, title="How It Works", brief="Mathematical explanation of self attention"),
                    Task(id=3, title="Applications", brief="Real-world uses of self attention"),
                ]
            )
    
    llm = MockLLM()
else:
    llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key)


def orchestrator(state: State) -> dict:

    plan = llm.with_structured_output(Plan).invoke(
        [
            SystemMessage(
                content=(
                    "Create a blog plan with 5-7 sections on the following topic."
                )
            ),
            HumanMessage(content=f"Topic: {state['topic']}"),
        ]
    )
    return {"plan": plan}

def fanout(state: State):
    return [Send("worker", {"task": task, "topic": state["topic"], "plan": state["plan"]})
            for task in state["plan"].tasks]

def worker(payload: dict) -> dict:

    # payload contains what we sent
    task = payload["task"]
    topic = payload["topic"]
    plan = payload["plan"]

    blog_title = plan.blog_title

    # Handle both real and mock LLM
    if isinstance(llm, ChatOpenAI):
        section_md = llm.invoke(
            [
                SystemMessage(content="Write one clean Markdown section."),
                HumanMessage(
                    content=(
                        f"Blog: {blog_title}\n"
                        f"Topic: {topic}\n\n"
                        f"Section: {task.title}\n"
                        f"Brief: {task.brief}\n\n"
                        "Return only the section content in Markdown."
                    )
                ),
            ]
        ).content.strip()
    else:
        # Mock response for testing
        section_md = f"## {task.title}\n\n{task.brief}\n\nThis is a demo section for testing purposes."

    return {"sections": [section_md]}
from pathlib import Path

def reducer(state: State) -> dict:
    
    title = state["plan"].blog_title
    body = "\n\n".join(state["sections"]).strip()

    final_md = f"# {title}\n\n{body}\n"

    # ---- save to file ----
    import re
    safe_title = re.sub(r'[^\w\s-]', '', title).strip()
    filename = safe_title.lower().replace(" ", "_") + ".md"
    output_path = Path(filename)
    output_path.write_text(final_md, encoding="utf-8")

    return {"final": final_md}
g = StateGraph(State)
g.add_node("orchestrator", orchestrator)
g.add_node("worker", worker)
g.add_node("reducer", reducer)

g.add_edge(START, "orchestrator")
g.add_conditional_edges("orchestrator", fanout, ["worker"])
g.add_edge("worker", "reducer")
g.add_edge("reducer", END)

app = g.compile()

app
out = app.invoke({"topic": "Write a blog on FastAPI", "sections": []})
print("\n--- Execution Completed Successfully ---")
print("Blog Title:", out.get("plan").blog_title if out.get("plan") else "None")
print(f"Final Output Length: {len(out.get('final', ''))} characters")

 