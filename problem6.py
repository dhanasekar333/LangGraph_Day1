# Problem 3: Add a log with a reducer (Level 2)

# Redo the cart graph, but add a log field that records what each node did.

# Problem 3: Shopping cart with a log (reducer)

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

# Empty cart decision: total stays 0.00 and the message says "Pay 0.00 ..."

class State(TypedDict):
    prices: list
    discount_percent: int
    total: float
    message: str
    log: Annotated[list, add]

def add_up(state: State) -> dict:
    total = sum(state["prices"])          # compute first, then log the NEW value
    return {
        "total": total,
        "log": [f"add_up: total={total:.2f}"],
    }

def apply_discount(state: State) -> dict:
    total = state["total"] * (1 - state["discount_percent"] / 100)
    return {
        "total": total,
        "log": [f"apply_discount: total={total:.2f}"],
    }

def finish(state: State) -> dict:
    message = f"Pay {state['total']:.2f} after {state['discount_percent']}% off"
    return {
        "message": message,
        "log": [f"finish: {message}"],
    }

builder = StateGraph(State)
builder.add_node("add_up", add_up)
builder.add_node("apply_discount", apply_discount)
builder.add_node("finish", finish)

builder.add_edge(START, "add_up")
builder.add_edge("add_up", "apply_discount")
builder.add_edge("apply_discount", "finish")
builder.add_edge("finish", END)

graph = builder.compile()

tests = [
    {"prices": [120.0, 50.5, 300.0], "discount_percent": 10},
    {"prices": [100.0], "discount_percent": 0},
    {"prices": [], "discount_percent": 50},
]

for t in tests:
    result = graph.invoke({**t, "total": 0.0, "message": ""})
    print(result["message"])
    print(result["log"])
    print()