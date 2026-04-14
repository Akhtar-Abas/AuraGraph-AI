from langchain_openai import ChatOpenAI
from engine.state import AgentState
from dotenv import load_dotenv
import os

load_dotenv()

# Global LLM instance with lower max_tokens to save credits
llm = ChatOpenAI(
    model="gpt-4o", 
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    max_tokens=800, # Report ke liye thore zyada tokens rakhein (500 kam ho saktay hain)
    temperature=0.3
)

def writer_node(state: AgentState):
    """
    Gathered content ko ek professional Markdown report mein convert karta hai.
    """
    task = state.get("task", "General Research")
    
    # Context ko string mein convert kar ke 8000 characters tak limit karein (Safe Zone)
    raw_data = "\n".join(state.get("content", []))[:8000] 
    
    # Sahi formatted prompt
    prompt = f"""
    You are a professional research writer.
    Summarize the following research into a professional Markdown report based on the user's request.

    User Original Request: {task}
    
    Raw Research Data (Truncated for efficiency):
    {raw_data}
    
    The report MUST have:
    1. Executive Summary
    2. Detailed Findings (with logical headers)
    3. Conclusion
    4. References (List the source URLs provided in data)
    
    Format the entire output in clean Markdown.
    """
    
    try:
        response = llm.invoke(prompt)
        return {
            "report": response.content,
            "status": "Final report generated successfully."
        }
    except Exception as e:
        print(f"--- WRITER NODE ERROR: {str(e)} ---")
        return {
            "report": f"Error generating report: {str(e)}",
            "status": "Failed to generate report."
        }