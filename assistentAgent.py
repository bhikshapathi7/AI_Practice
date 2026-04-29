import asyncio
import os
from _pyrepl import console

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from openai.types.beta import assistant

# get the Api key for OpenAI from https://platform.openai.com/api-keys
os.environ["OPENAI_API_KEY"] = ""
async def bkAgent():
    print("Assistent Agent")
    model_client=OpenAIChatCompletionClient(
    model="gpt-4o")
    assistant = AssistantAgent(name="BkAgent", model_client= model_client)
    await Console(assistant.run_stream(task = "find the lenth of the word Engineering?"))
    await model_client.close()

asyncio.run( bkAgent() )