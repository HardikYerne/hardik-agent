from tools.app_tools import (
    open_chrome,
    open_vscode,
    open_notepad,
    create_folder,
    shutdown_pc
)

TOOLS = {
    "open_chrome": open_chrome,
    "open_vscode": open_vscode,
    "open_notepad": open_notepad,
    "create_folder": create_folder,
    "shutdown_pc": shutdown_pc,
}

def execute_tool(tool_name: str, **kwargs):
    tool_name = tool_name.lower().strip()
    if tool_name in TOOLS:
        return TOOLS[tool_name](**kwargs)
    return f"Unknown tool: {tool_name}"

def get_available_tools():
    return list(TOOLS.keys())