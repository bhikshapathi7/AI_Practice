import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

os.environ["OPENAI_API_KEY"] = "api-key"
os.environ["JIRA_URL"] = "https://your-company.atlassian.net"
os.environ["JIRA_USERNAME"] = "bhikshapathi.kummari@gft.com"
os.environ["JIRA_API_TOKEN"] = "your_jira_api_token"


async def main():

    model_client = OpenAIChatCompletionClient(model="gpt-4o")

    jira_server_params = StdioServerParams(
        command="docker",
        args=[
            "run", "-i", "--rm",
            "-e", f"JIRA_URL={os.environ['JIRA_URL']}",
            "-e", f"JIRA_USERNAME={os.environ['JIRA_USERNAME']}",
            "-e", f"JIRA_API_TOKEN={os.environ['JIRA_API_TOKEN']}",
            "ghcr.io/sooperset/mcp-atlassian:latest"
        ]
    )

    playwright_server_params = StdioServerParams(
        command="npx",
        args=["y", "@playwright/mcp@latest"]
    )

    jira_workbench = McpWorkbench(jira_server_params)
    playwright_workbench = McpWorkbench(playwright_server_params)

    async with jira_workbench as jira_wb, playwright_workbench as pw_wb:

        jira_agent = AssistantAgent(
            name="JiraAgent",
            model_client=model_client,
            workbench=jira_wb,
            system_message="""
            You are a Jira data integration specialist responsible for the first stage
            of an automated QA pipeline.

            YOUR GOAL:
            Connect to the Jira API, retrieve all recent bug-type issues, and normalize
            them into a clean, consistent JSON schema that downstream agents can reliably
            consume without any ambiguity.

            YOUR RESPONSIBILITIES:
            1. Query Jira for issues of type "Bug" created or updated in the last 14 days
               (or as specified by the user).
            2. Filter by relevant fields: status (exclude "Done"/"Closed" unless requested),
               priority (Critical, High, Medium), and project key if provided.
            3. For each bug, extract and normalize:
               - id: Jira ticket key (e.g. "PROJ-123")
               - summary: one-line description of the bug
               - description: full reproduction steps, observed vs expected behavior
               - priority: Critical | High | Medium | Low
               - status: current workflow status
               - components: list of affected components or modules
               - labels: any tags applied
               - url: direct link to the Jira issue
               - reporter: who filed it
               - assignee: who owns it
               - created_at / updated_at: ISO timestamps
            4. Handle missing or malformed fields gracefully — use null for absent values,
               never skip an issue.
            5. Deduplicate if the same bug appears across multiple queries.

            OUTPUT FORMAT:
            Return a single JSON array of normalized bug objects. Do not include any
            prose, explanation, or markdown — only the raw JSON array. Example:
            [
              {
                "id": "PROJ-123",
                "summary": "Login button unresponsive on Safari 17",
                "description": "Steps to reproduce: ...",
                "priority": "High",
                "status": "In Progress",
                "components": ["Authentication", "UI"],
                "labels": ["safari", "regression"],
                "url": "https://yourorg.atlassian.net/browse/PROJ-123",
                "reporter": "alice@example.com",
                "assignee": "bob@example.com",
                "created_at": "2025-04-10T08:30:00Z",
                "updated_at": "2025-04-12T14:00:00Z"
              }
            ]

            RULES:
            - Never invent or hallucinate bug data. Only return what Jira provides.
            - If the API call fails, return a JSON error object: {"error": "reason"}.
            - Keep descriptions verbatim from Jira — do not summarize or paraphrase.
            - Maintain consistent field names across all bugs in the array.
            """
        )

        playwright_agent = AssistantAgent(
            name="PlaywrightAgent",
            model_client=model_client,
            workbench=pw_wb,
            system_message="""
            You are a senior QA automation engineer combining deep bug analysis expertise
            with hands-on Playwright test development skills. You are the second and final
            stage of an automated QA pipeline.

            YOUR GOAL:
            Receive a list of normalized Jira bugs from the Jira Fetcher agent, analyze
            each bug to understand the broken user journey, and directly produce
            production-ready Playwright smoke tests in TypeScript — without any
            intermediate handoff.

            YOUR TWO-PHASE PROCESS (internal — do not output Phase 1 separately):

            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            PHASE 1 — BUG ANALYSIS (think, don't output)
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            For each bug, internally determine:

            1. The broken user journey — what flow was the user in when the bug occurred?
            2. Entry point — which URL or route does the test start from?
            3. Preconditions — what state must exist before the test runs?
               (e.g. "user is logged in", "cart has at least one item")
            4. User actions — ordered steps the test must perform
            5. UI elements involved — key buttons, inputs, links, modals
               and their best Playwright locator strategy:
               getByRole() → getByTestId() → getByLabel() → getByText() → CSS selector
            6. Assertions — concrete, verifiable checks (what must be true after each action)
            7. Negative checks — things that must NOT happen
            8. Edge cases or flaky risks to handle

            ANALYSIS RULES:
            - Read the bug description carefully — test the observable symptom,
              not the root cause implementation detail.
            - If reproduction steps are missing, make reasonable inferences and
              mark them with a TODO comment in the generated test.
            - If multiple bugs share the same user flow, note deduplication
              opportunities in a comment.
            - If confidence is low due to insufficient bug detail, generate a
              test skeleton with TODO placeholders rather than skipping it.

            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            PHASE 2 — PLAYWRIGHT TEST GENERATION (output this)
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            For each bug, generate a complete .spec.ts file containing:

            1. A file header comment with the Jira ticket ID, summary, and URL
            2. A describe() block named after the ticket and bug summary
            3. A beforeEach() that handles:
               - Navigation to the entry URL
               - Any preconditions (login, seeding state, cookies)
            4. A primary it() smoke test block that:
               - Follows the user flow steps in order
               - Uses best-practice Playwright locators (priority order above)
               - Includes await expect() for every assertion
               - Checks negative conditions with .not matchers
               - Adds a @smoke annotation via test.info().annotations
            5. Explicit waits only — waitForURL(), waitForSelector(),
               or expect().toBeVisible() — never page.waitForTimeout()

            CODE QUALITY STANDARDS:
            - TypeScript strict mode — no `any` type
            - Import only from '@playwright/test'
            - Test data uses environment variables — never hardcode credentials
              (e.g. process.env.TEST_USER_EMAIL)
            - Each test must be fully independent — no shared state between tests
            - Use Page Object Model pattern if 3+ tests share the same page

            HARD RULES:
            - Never use page.waitForTimeout() — forbidden without exception.
            - Never hardcode credentials, tokens, or environment-specific URLs.
            - Never skip a bug — generate a test (even a skeleton) for every input bug.
            - Never guess selectors — use a clearly marked TODO: if a selector
              cannot be confidently inferred from the bug description.
            - If a bug has insufficient detail, add this comment at the top:
              // ⚠️ WARNING: Low confidence test — reproduction steps were incomplete.
            """
        )

        team = RoundRobinGroupChat(
            participants=[jira_agent, playwright_agent],
            termination_condition=TextMessageTermination("TEST COMPLETE")
        )

        await Console(
            team.run_stream(
                task="""
                Fetch all recent Jira bugs and for each bug perform the following:

                STEP 1 — ANALYZE THE BUG:
                - Identify the broken user journey and entry URL
                - Determine preconditions needed before the test starts
                - Extract the ordered user actions (clicks, form fills, navigation)
                - Identify all UI elements with their best Playwright locator strategy:
                  getByRole() → getByTestId() → getByLabel() → getByText() → CSS selector
                - Define concrete assertions (what MUST be true after each action)
                - Define negative checks (what must NOT happen)
                - Flag any missing reproduction steps with a TODO comment

                STEP 2 — GENERATE PLAYWRIGHT SMOKE TEST:
                - Write a complete production-ready .spec.ts file for each bug
                - Name the describe() block using the Jira ticket ID and bug summary
                - Add beforeEach() for navigation and preconditions
                - Follow the analyzed user flow step by step inside the test() block
                - Use await expect() for all assertions and .not matchers for negative checks
                - Add @smoke annotation via test.info().annotations
                - Use environment variables for all credentials and base URLs
                  (process.env.BASE_URL, process.env.TEST_USER_EMAIL, process.env.TEST_USER_PASSWORD)
                - Never use page.waitForTimeout() — use waitForURL(), waitForSelector(),
                  or expect().toBeVisible() instead
                - If bug details are insufficient, generate a skeleton test with
                  TODO placeholders and add a warning comment at the top of the file

                OUTPUT:
                Return one complete .spec.ts file per bug as a fenced TypeScript code block
                labeled with the filename:

                // File: PROJ-123.smoke.spec.ts
                // Jira: https://yourorg.atlassian.net/browse/PROJ-123
                // Bug:  <bug summary>
                // Priority: <priority>

                import { test, expect } from '@playwright/test';

                test.describe('PROJ-123 | <bug summary>', () => {

                    test.beforeEach(async ({ page }) => {
                        await page.goto(process.env.BASE_URL + '/<entry_route>');
                    });

                    test('<test objective> @smoke', async ({ page }) => {
                        test.info().annotations.push({ type: 'smoke', description: 'PROJ-123' });

                        await page.getByRole('button', { name: '<label>' }).click();

                        await expect(page).toHaveURL(/.*<expected_route>/);
                        await expect(page.getByRole('heading', { name: '<heading>' })).toBeVisible();

                        await expect(page.getByRole('alert')).not.toBeVisible();
                    });

                });

                Process ALL bugs from the input list and return ALL generated .spec.ts files.
                Once all tests are generated, respond with: TEST COMPLETE
                """
            )
        )


asyncio.run(main())