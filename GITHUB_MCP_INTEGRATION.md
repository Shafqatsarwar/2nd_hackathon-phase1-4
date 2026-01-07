# GitHub MCP Integration

The project now includes GitHub integration through Model Context Protocol (MCP) tools. This allows the AI assistant to interact with GitHub repositories directly.

## Configuration

To use the GitHub MCP tools, set the following environment variables:

```bash
# Required
GITHUB_TOKEN=your_github_personal_access_token

# Optional (defaults to empty)
GITHUB_OWNER=your_github_username_or_org
GITHUB_REPO=your_repository_name
```

## Available GitHub Tools

The following GitHub functions are available to the AI assistant:

### 1. Create GitHub Issue
- **Function**: `create_github_issue`
- **Parameters**:
  - `title` (required): Title of the issue
  - `body` (optional): Description of the issue
  - `labels` (optional): Array of labels to apply

### 2. List GitHub Issues
- **Function**: `list_github_issues`
- **Parameters**:
  - `state` (optional): "open", "closed", or "all" (default: "open")
  - `labels` (optional): Comma-separated list of labels to filter by

### 3. Create GitHub Pull Request
- **Function**: `create_github_pull_request`
- **Parameters**:
  - `title` (required): Title of the pull request
  - `body` (optional): Description of the pull request
  - `head` (required): Source branch name
  - `base` (optional): Target branch name (default: "main")

### 4. Get Repository Info
- **Function**: `get_github_repo_info`
- **Parameters**: None

### 5. List Repository Contents
- **Function**: `list_github_repo_contents`
- **Parameters**:
  - `path` (optional): Path in the repository to list (default: "/")

### 6. Create GitHub Gist
- **Function**: `create_github_gist`
- **Parameters**:
  - `description` (required): Description of the gist
  - `files` (required): Object mapping filenames to file content objects
  - `public` (optional): Whether the gist should be public (default: true)

## Usage Examples

The AI assistant can now handle requests like:
- "Create a GitHub issue about the login bug"
- "List all open issues in the repository"
- "Create a pull request for the new feature"
- "Show me the contents of the src directory"

## Security

- GitHub tokens are accessed through environment variables and never stored in code
- All API calls are authenticated using the provided token
- Error handling prevents sensitive information from being exposed to the user