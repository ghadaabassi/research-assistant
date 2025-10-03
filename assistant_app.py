from search.web_search import duckduckgo_search
from search.wikipedia_search import wikipedia_search
from models.SearchAssistantState import SearchState
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from models.LlmModel import llm

def sub_topic_generation(state: SearchState):
    prompt = [
        SystemMessage(content="You are an assistant that breaks a user question into 3-5 relevant sub-topics for better search coverage."),
        HumanMessage(content=f"Original Query: {state.query}\n\nList relevant sub-topics:")
    ]
    response = llm.invoke(prompt)
    sub_topics = [topic.strip("- ").strip() for topic in response.content.splitlines() if topic.strip()]
    return {"sub_topics": sub_topics}

def sub_topic_review(state: SearchState):
    return {} 

def after_sub_topic_review(state: SearchState):
    if state.human_feedback.strip().lower() == "approved":
        return ["web_search", "wikipedia_search"]
    else:
        if state.human_feedback:
            state.query += state.human_feedback 
        return "sub_topic_generation"


def generate_answer(state: SearchState):
    context = "\n\n".join(state.context)
    prompt = [
        SystemMessage(content="You are a helpful assistant that summarizes search results."),
        HumanMessage(content=f"Question: {state.query}\n\nContext:\n{context}")
    ]
    print("\n\n garthered context",state.context)
    print("\n\n sub-topics",state.sub_topics)

    response = llm.invoke(prompt)
    return {"answer": response.content}

builder = StateGraph(SearchState)


builder.add_node("sub_topic_generation", sub_topic_generation)
builder.add_node("sub_topic_review", sub_topic_review)

builder.add_node("web_search", duckduckgo_search)
builder.add_node("wikipedia_search", wikipedia_search)
builder.add_node("generate_answer", generate_answer)

builder.add_edge(START, "sub_topic_generation")
builder.add_edge("sub_topic_generation", "sub_topic_review")
builder.add_conditional_edges("sub_topic_review", after_sub_topic_review, ["sub_topic_generation", "web_search","wikipedia_search"])

builder.add_edge("web_search", "generate_answer")
builder.add_edge("wikipedia_search", "generate_answer")
builder.add_edge("generate_answer", END)

graph = builder.compile(interrupt_before=["sub_topic_review"])
