import warnings
warnings.filterwarnings("ignore")

from typing import TypedDict, Annotated
from operator import add

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

def my_reducer(current:int |None , update:int) -> int:
    if current is None:
        return 1
    return current + update

#Define State
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add]
    question: str
    turn_count: Annotated[int,my_reducer]

llm = ChatOllama(model = "llama3.2:3b",temperature = 0)

# define node
def chat_node(state:State) -> dict:
    current_question = state["question"]
    human_msg = HumanMessage(content=current_question)
    all_messages = state["messages"] + [human_msg]


    response = llm.invoke(all_messages)

    return {
        "messages":[human_msg,response],
        "turn_count": 1
        }

# Build Graph
builder = StateGraph(State)
builder.add_node("chat",chat_node)
builder.add_edge(START, "chat")
builder.add_edge("chat",END)

# compile with memory
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# run
def chat(thread_id:str,user_question:str):
    config = {"configurable":{"thread_id":thread_id}}

    result = graph.invoke(
        {"question": user_question},
        config = config
    )

    if result["turn_count"] >= 3:
        print("=== FINAL STATE REACHED (3 TURNS) ===")
        print(f"Current Question: {result['question']}")
        print(f"Total Turn Count: {result['turn_count']}")
        print("Message History:")
        for msg in result["messages"]:
            print(f"  {type(msg).__name__}: {msg.content}")
    else:
        # Standard chat printout for turns 1 and 2
        ai_message = result["messages"][-1]
        print(f"Turn {result['turn_count']} - Bot: {ai_message.content}\n")

if __name__ == "__main__":
    # Same thread = memory persists
    chat("tharun", "My name is Tharun and I love cricket.")
    chat("tharun", "What is my name?")         # remembers
    chat("tharun", "What sport do I love?")    # remembers

