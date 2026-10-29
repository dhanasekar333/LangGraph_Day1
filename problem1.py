import warnings
warnings.filterwarnings("ignore")

from typing import TypedDict, Annotated
from operator import add

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Define State
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add]
# Annotated with add means messages are APPENDED not replaced

llm = ChatOllama(model = "llama3.2:3b", temperature=0)

# Define Chat node
def chat_node(state:State) -> dict:
    messages = state["messages"]
    # Read messages from state
    
    response = llm.invoke(messages)

    # Return ONLY what changed — LangGraph merges with existing state
    return {"messages":[response]}
    # Because of operator.add reducer, this AIMessage gets APPENDED

# Build Graph
builder = StateGraph(State)
builder.add_node("chat",chat_node)

builder.add_edge(START, "chat")
builder.add_edge("chat",END)

# Compile with memory
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# Run
def chat(thread_id:str, user_message:str):
    config = {"configurable":{"thread_id":thread_id}}

    result = graph.invoke(
        {"messages":[HumanMessage(content=user_message)]},
        config = config
    )

    # Get AI Messages
    ai_message = result["messages"][-1]
    print(f"You: {user_message}")
    print(f"Bot: {ai_message.content}")
    print()

if __name__ == "__main__":
    # Same thread = memory persists
    chat("tharun", "My name is Tharun and I love cricket.")
    chat("tharun", "What is my name?")         # remembers
    chat("tharun", "What sport do I love?")    # remembers

    # Different thread = fresh start
    chat("rahul", "What is my name?")          # does not know

