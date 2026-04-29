import self
from autogen_agentchat.agents import AssistantAgent

import MCPConfig

mcp_config = MCPConfig


class AgentFactory:

    def __init__(self, model_client):
        self.model_client = model_client



    async def dataBase_Agent(self,system_message):

            db_agent = AssistantAgent(name="db_agent",
                                      model_client= self.model_client,
                                      workbench=mcp_config.MCPConfig.get_mysql_workbench(),
                                      system_message= system_message)

            return db_agent


    async def restAssured_agent(self, system_message):
        rest_agent = AssistantAgent(name="rest_agent",
                                    model_client= self.model_client,
                                    workbench=mcp_config.MCPConfig.get_restassured_workbench(),
                                    system_message= system_message)
        return rest_agent

    async def excelFile_agent(self,system_message):
        excel_agent = AssistantAgent(name="excel_agent",
                                    model_client= self.model_client,
                                    workbench=mcp_config.MCPConfig.get_excelserver_workbench(),
                                    system_message= system_message)
        return excel_agent

    async def fileserver_agent(self,system_message):
        fileserver_agent = AssistantAgent(name="fileserver_agent",
                                          model_client= self.model_client,
                                          workbench=mcp_config.MCPConfig.get_fileserver_workbench(),
                                          system_message= system_message)
        return fileserver_agent

