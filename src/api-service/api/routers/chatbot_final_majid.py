# %%
import requests
import os
from fastapi import APIRouter, Header, Query, Body, HTTPException
from fastapi.responses import FileResponse
from typing import Dict, Any, List, Optional

# from langchain_openai import ChatOpenAI
from typing import TypedDict
from typing import Annotated, TypedDict, List, Dict, Any, Optional
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# from langchain_openai import ChatOpenAI
from langchain_google_vertexai import ChatVertexAI

# from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
# from langchain_community.tools.playwright.utils import create_async_playwright_browser
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

# from langchain_core.pydantic_v1 import BaseModel, Field
# from IPython.display import Image, display
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import (
    AnyMessage,
    SystemMessage,
    HumanMessage,
    ToolMessage,
    AIMessage,
)

# from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# import gradio as gr
import uuid
from dotenv import load_dotenv
from google.oauth2 import service_account
from langgraph.checkpoint.sqlite import SqliteSaver

# from api.utils.chat_bot_agent import ChatAgent
from api.utils.chat_bot_agent import ChatAgent


router = APIRouter()
memory = MemorySaver()
# memory = SqliteSaver.from_conn_string(":memory:")
# memory = SqliteSaver(conn_string=":memory:")

load_dotenv(override=True)
credentials = service_account.Credentials.from_service_account_file("../secrets/stock-busters-service-account.json")
llm = ChatVertexAI(model="gemini-2.5-flash", credentials=credentials)


system_prompt = """"
You are an AI assitant which is collecting financial requirements from a user. The conversation has already started where the user is about to tell his name. Be polite.

You will be asking questions one by one and if you don't get the answer or asked a clarifying the query for your input, answer by explaining politley.
If you alreayd have the user preferences, show it to user and ask if they need any changes. If they do, ask the questions again.

Here are the questions:

Q1: What is your risk appetite. low, medium, high?
Q2: What is your investment horizon? short term (less than 3 months), more than 3 months.
Q3: Is there any particular sector you are interested in.

In the begining, confirmation: bool will always be false
When you are able to answer all the questions, you may end conversation by showing the final output.
In the end ask for confirmation from the user saying here is the summary of your preferences, if that looks good, I can generate the recommendations.

**CRITICAL INSTRUCTION: The final output must be a single summary containing all collected data in the following exact format:**
### Final Financial Requirements
final_response_output = 
    long_term: bool = Field(description="Long term investment preference.")
    short_term: bool = Field(description="Short term investment preference.")
    high_risk: bool = Field(description="High risk appetite check.")
    low_risk: bool = Field(description="Low risk appetite check.")
    sectors: list = Field(description="Preferred investment sectors.")
Wait for confirmation from the user
"""


abot = ChatAgent(llm, [], system=system_prompt, checkpointer=memory)


@router.get("/chats")
async def get_chats(x_session_id: str = Header(None, alias="X-Session-ID"), limit: Optional[int] = None):
    config = {"configurable": {"thread_id": x_session_id}}
    history = []
    welcome_message = "Welcome to Stock busters. I'm your AI assistant, and I'm here to help you gather your financial requirements. To start, may I please know your name?"
    print(welcome_message)
    history = [AIMessage(content=welcome_message)]
    user_input = ""
    user_confirm = False
    while user_input.lower() != "quit":
        user_input = input("\n")
        # response = chat(user_input, history)
        response = abot.graph.invoke({"messages": [{"role": "user", "content": user_input}]}, config=config)
        print(response["messages"][-1].content)
        print("\n")
        # print(f"{response}")
        # if response['user_pref']['confirmation'].get() == True:

        user_confirm = response.get("user_pref", {}).get("confirmation")
        # print("user_confirm=", user_confirm)
        # print("*"*50)
        # print(response)
        if user_confirm == True:
            user_input = "quit"
    return response.get("user_pref")
