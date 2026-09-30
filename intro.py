from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    message:str

def greet(state: State)->State:
    return {"message": "Hello" +" "+ state["message"] + "!"}

builder = StateGraph(State)
builder.add_node("greet",greet)
builder.add_edge(START,"greet")
builder.add_edge("greet",END)
graph = builder.compile()

result = graph.invoke({"message":"Jon Snow"})
print(result)
