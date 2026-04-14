from langgraph.graph import StateGraph, END # Sahi import check karein
from engine.state import AgentState
from engine.nodes.planner import planner_node
from engine.nodes.researcher import researcher_node
from engine.nodes.writer import writer_node

def create_graph():
    # 1. Graph initialize karein state ke sath
    workflow = StateGraph(AgentState)

    # 2. Saare Nodes add karein
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)

    # 3. Edges define karein
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", END)

    # 4. Graph ko compile karein
    return workflow.compile()

# Final app instance jo consumers.py mein use hogi
app = create_graph()