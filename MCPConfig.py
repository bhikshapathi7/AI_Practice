from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench


class MCPConfig:
    @staticmethod
    def get_mysql_workbench():
        mysql_server_params = StdioServerParams(
            command="/Library/Frameworks/Python.framework/Versions/3.12/bin/uv",
            args=[
                "--derectory",
                "/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages",
                "run",
                "mysql_mcp_server"
            ],
            env={
                "MYSQL_HOST": "localhost",
                "MYSQL_PORT": "3306",
                "MYSQL_USER": "root",
                "MYSQL_PASSWORD": "root1234",
                "MYSQL_DATABASE": "rahulshettyacademy"
            })
        return McpWorkbench(server_params=mysql_server_params)

    @staticmethod
    def get_restassured_workbench():
        restassured_server_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "dkmaker-mcp-rest-api"
            ],
            env={
                "REST_BASE_URL": "https://rahulshettyacademy.com",
                "HEADER_Accept": "application/json"
            })
        return McpWorkbench(server_params=restassured_server_params)


    @staticmethod
    def get_fileserver_workbench():
        fileserver_server_params = StdioServerParams(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "C:/Users/biki/NewAIProjects/AgenticAI"
            ],
            read_timeout_seconds=60)
        return McpWorkbench(server_params=fileserver_server_params)

    @staticmethod
    def get_excelserver_workbench():
        excelserver_server_params = StdioServerParams(
            command ="cmd",
            args= ["/c", "npx", "--yes", "@negokaz/excel-mcp-server"],
            env ={
            "EXCEL_MCP_PAGING_CELLS_LIMIT": "4000"
        })
        return McpWorkbench(server_params=excelserver_server_params)

