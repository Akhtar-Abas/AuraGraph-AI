from engine.state import AgentState
from engine.tools import get_search_tool

search_tool = get_search_tool()

def researcher_node(state: AgentState):
    plan = state.get("plan", [])
    all_results = []
    
    # Har topic par search karein
    for topic in plan:
        print(f"Searching for: {topic}")
        
        # Search tool se results lein
        # Slicing yahan apply karein taaki har result control mein rahe
        search_query = search_tool.invoke({"query": topic})
        
        for result in search_query:
            # 1. Sirf 800-1000 characters lein per result
            content_snippet = result['content'][:1000]
            
            # 2. Format karke list mein dalein
            formatted_snippet = f"Source: {result['url']}\nContent: {content_snippet}\n"
            all_results.append(formatted_snippet)
            
    # CRITICAL: Pure context ko bhi aik limit dein (e.g. 15,000 characters total)
    # Taaki Writer node 402 error na de
    final_context = all_results[:15] # Sirf top 15 snippets rakhein agar results bohot zyada hain
            
    return {
        "content": final_context,
        "status": f"Research gathered {len(final_context)} relevant snippets."
    }