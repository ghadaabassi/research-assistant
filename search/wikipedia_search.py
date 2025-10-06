from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from models.SearchAssistantState import SearchState

wiki_tool = WikipediaAPIWrapper(top_k_results=2)

def wikipedia_search(state: SearchState):
    result = wiki_tool.run(state.query)
    return {"context": [f"Wikipedia:\n{result}"]}
    