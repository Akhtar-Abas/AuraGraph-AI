import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI 
from engine.state import AgentState

# Load environment variables
load_dotenv()
llm = ChatOpenAI(
    model="gpt-4o", 
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1", # Agar OpenRouter key hai toh ye line zaroori hai
    max_tokens=500,
    temperature=0.3
)

def planner_node(state: AgentState):
    query = state.get("task", "")
    
    if not query:
        print("--- ERROR: No task found in state ---")
        return {"plan": [], "status": "Failed: No query provided"}

    prompt = f"""
    You are a research planning assistant. 
    Break down the following user query into 3 to 4 distinct research topics.
    User Query: {query}
    
    Respond ONLY with a bulleted list where each line starts with '- '.
    """
    
    try:
        response = llm.invoke(prompt)
        content = response.content
        
        # Robust parsing for different AI response styles
        plan = [
            line.strip("- ").strip() 
            for line in content.split("\n") 
            if line.strip() and (line.strip().startswith("-") or line.strip()[0].isdigit())
        ]
        
        print(f"--- PLANNER SUCCESSFULLY GENERATED: {plan} ---")
        
        return {
            "plan": plan, 
            "status": f"Planner created {len(plan)} topics."
        }
        
    except Exception as e:
        print(f"--- PLANNER ERROR: {str(e)} ---")
        return {"plan": [], "status": f"Error in Planner: {str(e)}"}