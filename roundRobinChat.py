import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

# get the Api key for OpenAI from https://platform.openai.com/api-keys
os.environ["OPENAI_API_KEY"] = ""
async def bk2Agents():
    model_client=OpenAIChatCompletionClient(model="gpt-4o")
    try:
        agent1 = AssistantAgent(name="MathsTeacher",
                                model_client= model_client,
                                system_message= 'Teacher should explain maths concept to Students')

        agent2 = AssistantAgent(name="Student",
                                model_client=model_client,
                                system_message='Student should get maths concepts from Teacher, and ask relavant doubts')


        team = RoundRobinGroupChat(participants=[agent1,agent2],
                                   termination_condition=MaxMessageTermination(max_messages=10))

        await Console(team.run_stream(task = 'Lets discuss Multiplication concept here'))

    finally:
        await model_client.close()

asyncio.run( bk2Agents() )