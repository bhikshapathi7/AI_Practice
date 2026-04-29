import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ["OPENAI_API_KEY"] = ""

async   def selectGroupChat():

    model_client = OpenAIChatCompletionClient(model='gpt-4o')
    try:

        analyst = AssistantAgent(name = 'Business Analyst',
                       model_client=model_client,
                       system_message= ' you are the BA Analysis the feature and provide some deta in Jira Ticket')

        developer = AssistantAgent(name='Developer',
                       model_client = model_client,
                       system_message = 'You are the developer, Have to develop feature based on BA Analysis data')

        tester = AssistantAgent(name = 'QA Engineer',
                       model_client = model_client,
                       system_message= " you are the QA Engineer, test and give sign of " 
                                       "for that feature as 'WORKING AS EXPECTED'")

        terminate = MaxMessageTermination(max_messages= 15) | TextMentionTermination('WORKING AS EXPECTED')


        sdlc = SelectorGroupChat(participants=[developer, tester, analyst],
                                 model_client=model_client,
                                 termination_condition= terminate,
                                 allow_repeated_speaker= True)

        await Console(sdlc.run_stream(task="Test the Feature and give sign of for that"
                                           "feature When It is 'WORKING AS EXPECTED'"))

    finally:
        await model_client.close()


asyncio.run(selectGroupChat())