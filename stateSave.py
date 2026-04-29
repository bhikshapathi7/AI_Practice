import asyncio
import json
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ["OPENAI_API_KEY"] = "api_key"


async def stateSave():
    model_client = OpenAIChatCompletionClient(model="gpt-42")
    try:
        agent1 = AssistantAgent(name="Helper", model_client= model_client)

        agent2 = AssistantAgent(name="BackUp", model_client= model_client)

        await Console( agent1.run_stream( task = ' I am Bhikshapathi working as an Automation Tester in GFT ') )

        saveState = await agent1.save_state()

        with open('savestate,json', 'w') as f:
            json.dump(saveState, f, default= str)

        with open('savestate,json', 'r') as f:
            savedState = json.load(f)

        await  agent2.load_state(savedState)

        await Console(agent2.run_stream( task = ' Who I am and Where I am working as what? ') )

    finally:
        await model_client.close()


asyncio.run(stateSave())