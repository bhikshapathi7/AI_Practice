import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import  TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


# get the Api key for OpenAI from https://platform.openai.com/api-keys
os.environ["OPENAI_API_KEY"] = "api_key"

async def aiAgentWithHuman():

    model_client = OpenAIChatCompletionClient(model='gpt-4o')
    try:
        wife = AssistantAgent(name = 'Wife',
                              model_client=model_client,
                              system_message="You are the wife agent for men, lets chat with Husbend "
                              "When mens says 'Bye!' or similar to 'Bye' or 'Thanks' or 'See you soon!' "
                              "Then close the chat with 'Bye! Bye!'")

        husband = UserProxyAgent(name = 'husband')

        couple = RoundRobinGroupChat(participants=[wife,husband],
                                     termination_condition=TextMentionTermination('Bye ! Bye!'))

        await Console(couple.run_stream(task='Hey, Hi, How are you!!!'))

    finally:
        await model_client.close()


asyncio.run(aiAgentWithHuman())

