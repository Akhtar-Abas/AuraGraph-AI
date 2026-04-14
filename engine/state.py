from typing import TypedDict, List

class AgentState(TypedDict):
    task: str
    plan: List[str] # Ensure this is a list
    content: List[str]
    report: str
    status: str