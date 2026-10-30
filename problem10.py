# Problem 7: Guess the number (Level 3, loop with changing state)

# Goal: A graph that finds a secret number by guessing the middle of a range and narrowing the range each round. 
# The loop changes the state on every pass.

from typing import TypedDict, Literal
from langgraph.graph import StateGraph,START,END

class State(TypedDict):
    secret: int
    low: int
    high: int
    guess: int
    steps: int
    found: bool

def make_guess(state:State) -> dict:
    state['guess'] = (state['low'] + state['high'])//2
    state['steps']+=1

    return{
        "guess": state['guess'],
        "steps": state["steps"]
    }

def compare(state:State) -> dict:
    if state['guess'] < state['secret']:
        state['low'] = state['guess'] + 1
    elif state['guess'] > state['secret']:
        state['high'] = state['guess'] - 1
    elif state['guess'] == state['secret']:
        state['found'] = True

    return {
        "low": state['low'],
        "high": state['high'],
        "found": state['found']
    }

def check(state:State) -> Literal["make_guess","__end__"]:
    if state["found"] or state["low"] > state["high"]:
        return END
    return "make_guess"

builder = StateGraph(State)
builder.add_node("make_guess",make_guess)
builder.add_node("compare",compare)

builder.add_edge(START, "make_guess")
builder.add_edge("make_guess","compare")
builder.add_conditional_edges("compare",check)

graph = builder.compile()

result = graph.invoke({
    "secret": 37,
    "low": 1,
    "high": 100,
    "guess": 0,
    "steps": 0,
    "found": False,
})
print(result)