import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

os.environ["OPENAI_API_KEY"] = "api key"

async def mcpToolingWithAgent():
        fs_server_params = StdioServerParams( command ="npx",
                                              args =  [
                                                    "-y",
                                                    "@modelcontextprotocol/server-filesystem",
                                                    "C:/Users/biki/NewAIProjects/AgenticAI"
                                                     ],
                                              read_timeout_seconds= 60
                                              )

        fs_wb = McpWorkbench(fs_server_params)

        try:
            async with fs_wb as wb:
                model_client = OpenAIChatCompletionClient(model="gpt-4o")
                mcpAgent = AssistantAgent(name="mcpToolingWithAgent",
                       model_client=model_client,
                       workbench=wb,
                       system_message='write the Python dictionaries concept with example that "'
                                      ' into file using FileSystem mcp, Once you done "LESSON COMPLETED"')

                userAgent = UserProxyAgent(name = 'user')

                team = RoundRobinGroupChat(participants=[mcpAgent,userAgent],
                                       termination_condition=TextMentionTermination('LESSON COMPLETED'))

                await Console(team.run_stream(task = 'Read the content and Update file with that content'))


        finally:
            await model_client.close()


asyncio.run(mcpToolingWithAgent())