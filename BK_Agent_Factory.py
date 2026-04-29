from autogen_agentchat.agents import AssistantAgent
from autogen_ext.tools.mcp import McpWorkbench

import BK_MCP_Config


class BKAgentFactory:

    def __init__(self, model_client):
        self.model_client = model_client

    async def fileServerAgent(self, system_message: str) -> AssistantAgent:
        """
        Creates and returns the FileServer Agent (Agent 1).
        Responsible for reading the API spec and generating feature file + Excel registry.
        """
        workbench = McpWorkbench(BK_MCP_Config.BKMCPConfig.get_fileserver_params())
        fileserver_agent = AssistantAgent(
            name="fileServerAgent",
            model_client=self.model_client,
            workbench=workbench,
            system_message=system_message
        )
        return fileserver_agent

    async def javaAgent(self, system_message: str) -> AssistantAgent:
        """
        Creates and returns the Java Agent (Agent 2).
        Responsible for generating Java step definitions, ApiClient, TestDataFactory, and Runner.
        """
        workbench = McpWorkbench(BK_MCP_Config.BKMCPConfig.get_javaserver_params())
        java_agent = AssistantAgent(
            name="javaAgent",
            model_client=self.model_client,
            workbench=workbench,
            system_message=system_message
        )
        return java_agent

    async def restAssuredAgent(self, system_message: str) -> AssistantAgent:
        """
        Creates and returns the RestAssured Agent (Agent 3).
        Responsible for executing Cucumber tests and validating responses against Excel registry.
        """
        workbench = McpWorkbench(BK_MCP_Config.BKMCPConfig.get_restassuredserver_params())
        rest_assured_agent = AssistantAgent(
            name="restAssuredAgent",
            model_client=self.model_client,
            workbench=workbench,
            system_message=system_message
        )
        return rest_assured_agent