from search.web_search import duckduckgo_search
from search.wikipedia_search import wikipedia_search
from models.SearchAssistantState import SearchState
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from models.LlmModel import llm
from langgraph.constants import Send

def generate_answer(state: SearchState):
    context = "\n\n".join(state.context)
    prompt = [
        SystemMessage(content="You are a helpful assistant that summarizes search results."),
        HumanMessage(content=f"Question: {state.query}\n\nContext:\n{context}")
    ]
    response = llm.invoke(prompt)
    return {"answer": response.content}


# Build the graph
builder = StateGraph(SearchState)

# Nodes
builder.add_node("duckduckgo_search", duckduckgo_search)
builder.add_node("wikipedia_search", wikipedia_search)
builder.add_node("generate_answer", generate_answer)

# Edges
builder.add_edge(START, "duckduckgo_search")
builder.add_edge(START, "wikipedia_search")
builder.add_edge("duckduckgo_search", "generate_answer")
builder.add_edge("wikipedia_search", "generate_answer")
builder.add_edge("generate_answer", END)

# Compile
graph = builder.compile()
