from typing import Dict, Any, List
from openai import OpenAI
import json
import os
from .task_tools import MCPTaskTools
from .github_tools import GitHubMCPTools, GITHUB_TOOLS
from .web_search import search_web
from .weather_service import get_weather_info, get_weather_forecast
from ..database import get_session
from sqlmodel import Session


class TodoOpenAIAgent:
    """
    OpenAI Agent that uses MCP tools to interact with the todo system
    """

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is not set. "
                "Please configure it in your .env file or environment variables."
            )
        self.client = OpenAI(api_key=api_key)

        # Initialize tools
        self.github_tools = GitHubMCPTools()
        self.task_tools = MCPTaskTools(get_session)

        # Define the tools that the agent can use
        self.tools = [
            # Task management tools
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "title": {"type": "string", "description": "Task title"},
                            "description": {"type": "string", "description": "Task description (optional)"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"], "default": "medium", "description": "Task priority level"},
                            "is_recurring": {"type": "boolean", "default": False, "description": "Whether the task is recurring"},
                            "recurrence_interval": {"type": "string", "description": "How often the task recurs (e.g., daily, weekly, monthly)"}
                        },
                        "required": ["user_id", "title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve tasks from the list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "status": {"type": "string", "enum": ["all", "pending", "completed"], "default": "all"}
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "task_id": {"type": "integer", "description": "The task ID to complete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a task from the list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "task_id": {"type": "integer", "description": "The task ID to delete"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Modify task title or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {"type": "string", "description": "The user ID"},
                            "task_id": {"type": "integer", "description": "The task ID to update"},
                            "title": {"type": "string", "description": "New title (optional)"},
                            "description": {"type": "string", "description": "New description (optional)"},
                            "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "New priority level (optional)"},
                            "is_recurring": {"type": "boolean", "description": "Whether the task is recurring (optional)"},
                            "recurrence_interval": {"type": "string", "description": "How often the task recurs (optional)"}
                        },
                        "required": ["user_id", "task_id"]
                    }
                }
            }
        ]

        # Add GitHub tools to the agent
        self.tools.extend(GITHUB_TOOLS)

        # Add web search tool to the agent
        self.tools.append({
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Search the web for current information, news, market rates, and other public information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query for information"}
                    },
                    "required": ["query"]
                }
            }
        })

        # Add weather tools to the agent
        self.tools.append({
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get current weather information for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "Location to get weather for (e.g., 'Lahore, Pakistan', 'Karachi', 'Islamabad')"}
                    },
                    "required": ["location"]
                }
            }
        })

        self.tools.append({
            "type": "function",
            "function": {
                "name": "get_weather_forecast",
                "description": "Get weather forecast for a specific location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "Location to get forecast for (e.g., 'Lahore, Pakistan', 'Karachi', 'Islamabad')"}
                    },
                    "required": ["location"]
                }
            }
        })

    def process_message(self, user_id: str, message: str, session: Session) -> str:
        """
        Process a user message using OpenAI agent with MCP tools
        """
        # Create a temporary task_tools instance with the current session
        temp_task_tools = MCPTaskTools(lambda: session)

        # Prepare the messages for the OpenAI API
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a highly capable AI assistant. Your primary roles are:\n"
                    "1. Manage tasks/todos using the provided tools.\n"
                    "2. Orchestrate GitHub operations via MCP tools.\n"
                    "3. Answer ANY additional user questions by searching the web for real-time, accurate information.\n\n"
                    "If a user asks about news, facts, external events, or anything not in their task list, ALWAYS use the 'web_search' tool to provide a helpful, cited response. "
                    "Always use the appropriate tool for the user's request. "
                    "Only use the tools provided, do not try to access the database directly.\n"
                    f"The current user ID is: {user_id}"
                )
            },
            {
                "role": "user",
                "content": message
            }
        ]

        # Call the OpenAI API with function calling
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change this to gpt-4 if preferred
            messages=messages,
            tools=self.tools,
            tool_choice="auto"
        )

        # Process the response
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Append the assistant message (the one that requested tools) to the history,
        # so that the following tool responses correctly follow a message with tool_calls.
        assistant_message = {
            "role": response_message.role,
            "content": response_message.content or "",
        }
        if response_message.tool_calls:
            assistant_message["tool_calls"] = [
                {
                    "id": tool_call.id,
                    "type": getattr(tool_call, "type", "function"),
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments,
                    },
                }
                for tool_call in response_message.tool_calls
            ]
        messages.append(assistant_message)

        if tool_calls:
            # Process tool calls
            tool_results = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Add the user_id to the function args if not present
                if "user_id" not in function_args:
                    function_args["user_id"] = user_id

                # Call the appropriate MCP tool function
                if function_name == "add_task":
                    result = temp_task_tools.add_task(
                        user_id=function_args["user_id"],
                        title=function_args["title"],
                        description=function_args.get("description"),
                        priority=function_args.get("priority", "medium"),
                        is_recurring=function_args.get("is_recurring", False),
                        recurrence_interval=function_args.get("recurrence_interval")
                    )
                elif function_name == "list_tasks":
                    result = temp_task_tools.list_tasks(
                        user_id=function_args["user_id"],
                        status=function_args.get("status", "all")
                    )
                elif function_name == "complete_task":
                    result = temp_task_tools.complete_task(
                        user_id=function_args["user_id"],
                        task_id=function_args["task_id"]
                    )
                elif function_name == "delete_task":
                    result = temp_task_tools.delete_task(
                        user_id=function_args["user_id"],
                        task_id=function_args["task_id"]
                    )
                elif function_name == "update_task":
                    result = temp_task_tools.update_task(
                        user_id=function_args["user_id"],
                        task_id=function_args["task_id"],
                        title=function_args.get("title"),
                        description=function_args.get("description"),
                        priority=function_args.get("priority"),
                        is_recurring=function_args.get("is_recurring"),
                        recurrence_interval=function_args.get("recurrence_interval")
                    )
                # GitHub tool functions
                elif function_name == "create_github_issue":
                    result = self.github_tools.create_issue(
                        title=function_args["title"],
                        body=function_args.get("body", ""),
                        labels=function_args.get("labels")
                    )
                elif function_name == "list_github_issues":
                    result = self.github_tools.list_issues(
                        state=function_args.get("state", "open"),
                        labels=function_args.get("labels")
                    )
                elif function_name == "create_github_pull_request":
                    result = self.github_tools.create_pull_request(
                        title=function_args["title"],
                        body=function_args.get("body", ""),
                        head=function_args["head"],
                        base=function_args.get("base", "main")
                    )
                elif function_name == "get_github_repo_info":
                    result = self.github_tools.get_repo_info()
                elif function_name == "list_github_repo_contents":
                    result = self.github_tools.list_repo_contents(
                        path=function_args.get("path", "/")
                    )
                elif function_name == "create_github_gist":
                    result = self.github_tools.create_gist(
                        description=function_args["description"],
                        files=function_args["files"],
                        public=function_args.get("public", True)
                    )
                elif function_name == "web_search":
                    result = search_web(query=function_args["query"])
                elif function_name == "get_current_weather":
                    result = get_weather_info(location=function_args["location"])
                elif function_name == "get_weather_forecast":
                    result = get_weather_forecast(location=function_args["location"])
                else:
                    result = {"error": f"Unknown tool: {function_name}"}

                tool_results.append({
                    "role": "tool",
                    "type": "function",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

            # If there were tool calls, get the final response from the assistant
            if tool_results:
                # Add the tool results to the messages
                for tool_result in tool_results:
                    messages.append(tool_result)

                # Get the final response from the assistant
                final_response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )

                return final_response.choices[0].message.content

        # If no tool calls were made, return the assistant's response
        if response_message.content:
            return response_message.content

        return "I processed your request, but I don't have a specific response to share."