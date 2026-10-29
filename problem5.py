# Problem 2: Shopping cart (Level 1 to 2, state updates)

# Goal: Total a shopping cart in a graph.

import warnings
warnings.filterwarnings("ignore")

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    prices:list
    discount_percent: int
    total: float
    message: str

def add_up(state:State) -> dict:
    total = state["total"]
    price = state["prices"]

    return {"total": sum(state["prices"])}

def apply_discount(state:State)->dict:
    total = state["total"]
    discount_percent = state["discount_percent"]

    total = total * (1 - discount_percent / 100 )

    return {
        "total":total
    }

def finish(state:State)->dict:
    total = state["total"]
    discount_percent = state["discount_percent"]
    message = state["message"]

    message = f"Pay {total:.2f} after {discount_percent}% off"
    return {
        "message":message
    }

builder = StateGraph(State)
builder.add_node("add_up",add_up)
builder.add_node("apply_discount",apply_discount)
builder.add_node("finish",finish)

builder.add_edge(START,"add_up")
builder.add_edge("add_up","apply_discount")
builder.add_edge("apply_discount","finish")
builder.add_edge("finish",END)

graph = builder.compile()

result = graph.invoke(
    {"prices": [120.0, 50.5, 300.0], "discount_percent": 10, "total": 0.0, "message": ""}
)
result1 = graph.invoke(
    {"prices": [100.0], "discount_percent": 0, "total": 0.0, "message": ""}
)
result2 = graph.invoke(
    {"prices": [], "discount_percent": 50, "total": 0.0, "message": ""}
)
print(result)
print(result1)
print(result2)