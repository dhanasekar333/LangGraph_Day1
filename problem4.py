# Problem 1: Temperature report (Level 1)

# Goal: Take a temperature in Celsius and produce a short report.

import warnings
warnings.filterwarnings("ignore")

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    celsius: float
    fahrenheit: float
    category: str
    report: str

def to_fahrenheit(state:State)->dict:
    celsius = state["celsius"]

    fahrenheit = celsius * 9/5 + 32
    return {
        "fahrenheit":fahrenheit
    }

def classify(state:State) -> dict:
    celsius = state["celsius"]

    if celsius < 15:
        category = "cool"
    elif celsius < 30 and celsius >= 15:
        category = "warm"
    else:
        category = "hot"

    return {
        "category": category
    }

def make_report(state:State) -> dict:
    celsius = state["celsius"]
    fahrenheit = state["fahrenheit"]
    category = state["category"]

    report = f"{celsius}°C is {fahrenheit}°F, it feels {category}"

    return {
        "report":report
    }

builder = StateGraph(State)
builder.add_node("Fahrenheit",to_fahrenheit)
builder.add_node("classify_category",classify)
builder.add_node("make_report",make_report)

builder.add_edge(START, "Fahrenheit")
builder.add_edge("Fahrenheit","classify_category")
builder.add_edge("classify_category","make_report")
builder.add_edge("make_report",END)

graph = builder.compile()

for c in [5, 15, 22, 30, 35]:
    result = graph.invoke({"celsius": c})
    print(result["report"])