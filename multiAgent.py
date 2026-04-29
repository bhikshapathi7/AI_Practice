import asyncio
import os
from _pyrepl import console

from PIL import Image
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from openai.types.beta import assistant

# get the Api key for OpenAI from https://platform.openai.com/api-keys
os.environ["OPENAI_API_KEY"] = ""

async def bkAgent():
    model_client=OpenAIChatCompletionClient(model="gpt-4o")
    assistant = AssistantAgent(name="BkAgent", model_client= model_client)
    image = Image.from_file("./testData/e-PAN.pdf")
    multiModalMessage = MultiModalMessage(content=["What is there in that image", image], source="user")
    await Console(assistant.run_stream(task = multiModalMessage))
    await model_client.close()

asyncio.run( bkAgent() )