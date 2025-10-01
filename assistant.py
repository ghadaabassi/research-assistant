# from typing import TypedDict , Literal
# from langgraph.graph import StateGraph, START, END
# from operator import add
# from typing import Annotated

# class State(TypedDict):
#     text: Annotated[list[int],add]

# def echo(state: State) -> State:
#     state["output"] = f"You said: {state['input']}"
#     return state

# # Build the graph
# workflow = StateGraph(State)
# workflow.add_node("echo", echo)

# workflow.add_edge(START, "echo")
# workflow.add_edge("echo", END)

# graph = workflow.compile()


from typing import Any
from typing_extensions import TypedDict
from typing import Annotated
from operator import add

from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    # Use Annotated to declare reducer for merging
    state: str

class ReturnNodeValue:
    def __init__(self, node_secret: str):
        self._value = node_secret

    def __call__(self, state: State) -> Any:
        print(f"Adding {self._value} to {state['state']}")
        return {"state": [self._value]}

# Build graph
builder = StateGraph(State)

builder.add_node("a", ReturnNodeValue("I'm A"))
builder.add_node("b", ReturnNodeValue("I'm B"))
builder.add_node("c", ReturnNodeValue("I'm C"))
builder.add_node("d", ReturnNodeValue("I'm D"))

builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("b", "c")
builder.add_edge("c", "d")
builder.add_edge("d", END)

graph = builder.compile()

# Visualize

# Run
final_state = graph.invoke({"state": []})
print("\nFinal state:", final_state)
