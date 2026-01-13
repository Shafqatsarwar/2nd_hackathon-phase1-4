import os
from openai import OpenAI
from .task_tools import MCPTaskTools
from .github_tools import GitHubMCPTools, GITHUB_TOOLS
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

    async def process_message(self, user_id: str, message: str, session: Session):
        """
        Process a user message using OpenAI agent with MCP tools and stream the response.
        """
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

        # Call the OpenAI API with function calling and streaming
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # You can change this to gpt-4 if preferred
            messages=messages,
            tools=self.tools,
            tool_choice="auto",
            stream=True
        )

        # Process the stream
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content