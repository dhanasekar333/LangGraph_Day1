# Problem 5: First branch (Level 3, conditional edges)

# Goal: Route a support ticket to a different node depending on its text.

from typing import TypedDict, Annotated, Literal
from langgraph.graph import START,END, StateGraph

class State(TypedDict):
    text:str
    category:str
    reply:str

def classify(state: State) -> dict:
    text = state["text"].lower()       # lower once, reuse below

    if "refund" in text or "invoice" in text:
        category = "billing"
    elif "error" in text or "crash" in text:
        category = "tech"
    else:
        category = "general"

    return {"category": category}

def route(state:State) -> Literal["billing_reply","tech_reply","general_reply"]:
    if state["category"] == "billing":
        return "billing_reply"
    elif state["category"] == "tech":
        return "tech_reply"
    else:
        return "general_reply"

def billing_node(state:State) -> dict:
    return {
        "reply": "Hi, U have reached billing node"
    }

def tech_node(state:State) -> dict:
    return {
        "reply":"Hi, u have reached tech node"
    }

def general_node(state:State) -> dict:
    return {
        "reply":"Hi, this is general node where u get common answers other than tech or billing"
    }

builder = StateGraph(State)
builder.add_node("classify",classify)
builder.add_node("billing",billing_node)
builder.add_node("tech",tech_node)
builder.add_node("general",general_node)

builder.add_edge(START, "classify")
builder.add_conditional_edges(
    "classify", #source
    route, #condition function
    {
        "billing_reply": "billing",
        "tech_reply":"tech",
        "general_reply":"general"
    }
)
builder.add_edge("billing",END)
builder.add_edge("tech",END)
builder.add_edge("general",END)

graph = builder.compile()

questions = [
    "I want a REFUND for my order",
    "The app has a crash on login",
    "What are your opening hours?",
    "My invoice shows an error"
]

for question in questions:
    result = graph.invoke(
        {"text": question}
    )
    print(f"Question: {result["text"]}")
    print(f"Category: {result["category"]}")
    print(f"Reply: {result["reply"]}")
    print("="*60)
    print()


# another improved version
from typing import TypedDict, Literal
from langgraph.graph import START, END, StateGraph

class State(TypedDict):
    text: str
    category: str
    reply: str

def classify(state: State) -> dict:
    text = state["text"].lower()
    if "refund" in text or "invoice" in text:
        category = "billing"
    elif "error" in text or "crash" in text:
        category = "tech"
    else:
        category = "general"
    return {"category": category}

# 1. The router now returns the EXACT name of the destination nodes
def route(state: State) -> Literal["billing_reply", "tech_reply", "general_reply"]:
    if state["category"] == "billing":
        return "billing_reply"
    elif state["category"] == "tech":
        return "tech_reply"
    else:
        return "general_reply"

def billing_node(state: State) -> dict:
    return {"reply": "Hi, U have reached billing node"}

def tech_node(state: State) -> dict:
    return {"reply": "Hi, u have reached tech node"}

def general_node(state: State) -> dict:
    return {"reply": "Hi, this is general node where u get common answers other than tech or billing"}

builder = StateGraph(State)
builder.add_node("classify", classify)

# 2. Rename your nodes to match the router's return values exactly
builder.add_node("billing_reply", billing_node)
builder.add_node("tech_reply", tech_node)
builder.add_node("general_reply", general_node)

builder.add_edge(START, "classify")

# 3. Pass ONLY the routing function (no dictionary needed!)
builder.add_conditional_edges("classify", route)

builder.add_edge("billing_reply", END)
builder.add_edge("tech_reply", END)
builder.add_edge("general_reply", END)

graph = builder.compile()

questions = [
    "I want a REFUND for my order",
    "The app has a crash on login",
    "What are your opening hours?",
    "My invoice shows an error"
]

for question in questions:
    result = graph.invoke(
        {"text": question}
    )
    print(f"Question: {result["text"]}")
    print(f"Category: {result["category"]}")
    print(f"Reply: {result["reply"]}")
    print("="*60)
    print()