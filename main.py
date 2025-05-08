from dotenv import load_dotenv
import os
from typing import Annotated, Literal
from langchain_openai import ChatOpenAI  # Correct import
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.graph import START, END 

load_dotenv()

# Initialize OpenAI o4-mini correctly
llm = ChatOpenAI(model="o4-mini")  # Direct initialization

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)    

def chatbot(state: State): 
    return {"messages": [llm.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")  # Fixed parameter name
graph_builder.add_edge("chatbot", END)    # Fixed parameter name

graph = graph_builder.compile()

user_input = input("Enter your message: ")
# Fixed key from 'message' to 'messages'
state = graph.invoke({"messages": [{"role": "user", "content": user_input}]})

print(state["messages"][-1].content) #-1 to grab the last message and print it
