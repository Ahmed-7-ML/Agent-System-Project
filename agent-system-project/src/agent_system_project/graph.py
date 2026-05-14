from .crew import run_research_crew
from typing import TypedDict
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    task: str
    output_format: str
    agent: str
    crew_result: str

# Workflow:
# Node 1: استقبال المهمة من FastAPI
# Node 2: تنفيذ CrewAI
# Node 3: إرجاع النتيجة

# LangGraph:
# LangGraph هو المسؤول عن إدارة الـ State، مش انت!
# لو عدّلت الـ State مباشرة، بتتجاوز الـ Graph وممكن يسبب مشاكل في الـ Concurrency

def router_node(state: AgentState):
    task = state["task"]
    output_format = state["output_format"]
    
    if "report" in task.lower():
        return {
        "agent": "research_agent"
        }
        
    elif "write" in task.lower():
        return {
        "agent": "writer_agent"
        }
        
    else:
        return {
            "agent": "research_agent"
            }

def crewai_node(state: AgentState):
    agent = state["agent"]
    task = state['task']
    output_format = state['output_format']
    
    # if agent == "research_agent":
    #     research_agent.execute(task)
    # elif agent == "writer_agent":
    #     writer_agent.execute(task)
    
    return {'crew_result' : 
            run_research_crew(task, output_format)
    }

# Combine all nodes into Graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("router", router_node)
workflow.add_node("crew", crewai_node)

# Set Entry Point
workflow.set_entry_point("router")

# Link Nodes
workflow.add_edge("router", "crew")
workflow.add_edge("crew", END)

# Combine the Graph
workflow_app = workflow.compile()
