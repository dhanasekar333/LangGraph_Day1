import warnings
warnings.filterwarnings("ignore")

from typing import TypedDict, Annotated
from operator import add

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    question:str
    category:str
    answer:str

llm = ChatOllama(model = "llama3.2:3b",temperature=0)

def classify_node(state:State) -> dict:
    question = state["question"]

    classifier_chain = ChatPromptTemplate.from_messages([
        ("system","""You're a helpful assistant. read the question that user asks and return the category exactly in one word.
            Categories are 'technical' and 'general'. return exactly one word. No extra text or explanation"""),
        ("human","{question}")
    ])|llm|StrOutputParser()

    # ✅ run the chain, then clean the string it returns
    category = classifier_chain.invoke({"question": question}).strip().lower()
    return {
        "category":category
    }

def answer_node(state: State) -> dict:
    question = state["question"]
    category = state["category"]

    if "technical" in category:
        answer_chain = ChatPromptTemplate.from_messages([
            ("system", """your task is to answer the question that user asks. You're a technical writer.
            Please help the user by giving great answers"""),
            ("human", "{question}")
        ]) | llm | StrOutputParser()
        answer = answer_chain.invoke({"question": question})

    elif "general" in category:
        answer_chain = ChatPromptTemplate.from_messages([
            ("system", """your task is to answer the question that user asks. You're a general assistant.
            Please help the user by giving some good answers"""),
            ("human", "{question}")
        ]) | llm | StrOutputParser()
        answer = answer_chain.invoke({"question": question})

    else:
        answer = "I cannot answer this"

    return {"answer": answer}

builder = StateGraph(State)
builder.add_node("classify",classify_node)
builder.add_node("answer",answer_node)

builder.add_edge(START,"classify")
builder.add_edge("classify","answer")
builder.add_edge("answer",END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

def ask(thread_id:str, user_question:str):
    config = {"configurable":{"thread_id":thread_id}}

    result = graph.invoke(
        {"question":user_question},
        config=config
    )

    print("="*20)
    print(f"category: {result["category"]}")
    print(f"answer: {result["answer"]}")

if __name__ == "__main__":
    ask("Tharun","What is a Python decorator?")
    ask("Tharun","Tell me a fun fact about cricket")




