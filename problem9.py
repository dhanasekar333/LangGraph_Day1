# Problem 6: Retry loop (Level 3, loops)

# Goal: Build a graph that keeps trying until it succeeds, or gives up after a limit. 
# This is how agents retry in practice, and a loop is what your branch now makes possible.

from typing import TypedDict,Literal
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    attempts:int
    max_attempts:int
    result:str
    status:str

def try_task(state:State) -> dict:
    attempts = state['attempts'] + 1

    if attempts >= 3:
        state['result'] = "done"
    else:
        state['result'] = "error"

    return{
        "attempts": attempts,
        "result": state['result']
    }

def check(state:State) -> Literal["finish","give_up","try_task"]:
    if state['result'] == "done":
        return "finish"
    elif state['attempts'] >= state['max_attempts']:
        return "give_up"
    else:
        return "try_task"

def give_up(state:State) -> dict:
    state['status'] = "failed"

    return{
        "status":state['status']
    }

def finish(state:State) -> dict:
    state['status'] = "success"

    return{
        "status":state['status']
    }

builder = StateGraph(State)
builder.add_node("try_task",try_task)
builder.add_node("give_up",give_up)
builder.add_node("finish",finish)

builder.add_edge(START, "try_task")

builder.add_conditional_edges("try_task",check)

builder.add_edge("give_up",END)
builder.add_edge("finish",END)

graph = builder.compile()

max_attempts = [5,2,3]
for n in max_attempts:
    response = graph.invoke({"attempts": 0, "max_attempts": n, "result": "", "status": ""})
    print(f"attempts: {response["attempts"]}")
    print(f"result: {response["result"]}")
    print(f"status: {response["status"]}")
    print("="*60)
    print()