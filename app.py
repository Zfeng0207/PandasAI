import pandas as pd
import chainlit as cl
import os
from dotenv import load_dotenv
from pandasai import SmartDataframe
from langchain_community.llms import Ollama
from langchain_groq.chat_models import ChatGroq
from openai import AsyncOpenAI
from pandasai.llm import OpenAI

# groq key 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
# Set the environment variable

# Initialize the model with the API key
llm = OpenAI(api_token="OPENAIKEY")
@cl.on_chat_start
def start_chat():
    # set initial message history
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],)

@cl.on_message
async def main(message: cl.Message):
    # Retrieve message history
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})
    data = 'ms_cleaned.csv'
    df = SmartDataframe(data,config = {'llm':llm})
    question = message.content
    response = df.chat(question)
    msg = cl.Message(content=response)
    await msg.send()
    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
