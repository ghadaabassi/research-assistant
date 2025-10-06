from langchain_community.tools import DuckDuckGoSearchRun
from models.SearchAssistantState import SearchState


duck_tool = DuckDuckGoSearchRun(top_k=2)

def web_search(state: SearchState):
    result = duck_tool.run(state.query)
    return {"context": [f"DuckDuckGo:\n{result }"]}
    
