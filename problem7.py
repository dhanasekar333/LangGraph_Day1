from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END


def keep_max(old: int | None, new: int) -> int:
    if old is None:
        return new
    return max(old, new)


class State(TypedDict):
    scores: Annotated[list, add]
    best: Annotated[int, keep_max]


def judge_a(state: State) -> dict:
    return {
        "scores":[72],  
        "best": 72
    }

def judge_b(state: State) -> dict:
    return {
        "scores":[91],
        "best": 91
    }

def judge_c(state: State) -> dict:
    return {
        "scores":[85],
        "best": 85
    }

# 4. Building and structuring the Graph
builder = StateGraph(State)

builder.add_node("judge_a", judge_a)
builder.add_node("judge_b", judge_b)
builder.add_node("judge_c", judge_c)

builder.add_edge(START, "judge_a")
builder.add_edge("judge_a", "judge_b")
builder.add_edge("judge_b", "judge_c")
builder.add_edge("judge_c", END)

graph = builder.compile()


result = graph.invoke({})
print(result)

