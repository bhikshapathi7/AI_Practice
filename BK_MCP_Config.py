from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench


class BKMCPConfig:

    @staticmethod
    def get_fileserver_params() -> StdioServerParams:
        """
        Returns StdioServerParams for the FileServer MCP Agent.
        Grants filesystem read/write access to the project root folder.
        """
        return StdioServerParams(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                "C:/Users/biki/NewAIProjects/AgenticAI"
            ],
            read_timeout_seconds=60
        )

    @staticmethod
    def get_javaserver_params() -> StdioServerParams:
        """
        Returns StdioServerParams for the Java MCP Agent.
        Runs a compiled Java MCP server JAR for Java code generation tasks.
        Timeout is higher to account for JVM startup time.
        """
        return StdioServerParams(
            command="java",
            args=[
                "-jar",
                "C:/Users/biki/NewAIProjects/AgenticAI/mcp-server.jar"
            ],
            read_timeout_seconds=120  # increased: JVM startup needs more time
        )

    @staticmethod
    def get_restassuredserver_params() -> StdioServerParams:
        """
        Returns StdioServerParams for the RestAssured MCP Agent.
        Uses dkmaker-mcp-rest-api to execute REST API test scenarios.
        """
        return StdioServerParams(
            command="npx",
            args=[
                "-y",
                "dkmaker-mcp-rest-api"
            ],
            env={
                "REST_BASE_URL": "https://rahulshettyacademy.com",
                "HEADER_Accept": "application/json"
            },
            read_timeout_seconds=180  # highest: test execution takes the longest
        )