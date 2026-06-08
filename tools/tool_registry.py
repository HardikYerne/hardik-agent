from tools.app_tools import (
    open_chrome,
    open_vscode,
    open_notepad,
    open_file_manager,
    open_task_manager,
    open_calculator,
    open_settings,
    open_browser,
    create_folder,
    shutdown_pc,
    take_screenshot,
    open_youtube,
    open_gmail
)

TOOLS = {
    'open_chrome': open_chrome,
    'open_browser': open_browser,
    'open_vscode': open_vscode,
    'open_notepad': open_notepad,
    'open_file_manager': open_file_manager,
    'file_manager': open_file_manager,
    'open_task_manager': open_task_manager,
    'open_calculator': open_calculator,
    'open_settings': open_settings,
    'create_folder': create_folder,
    'shutdown_pc': shutdown_pc,
    'take_screenshot': take_screenshot,
    'open_youtube': open_youtube,
    'open_gmail': open_gmail,
}

def execute_tool(tool_name, **kwargs):
    tool_name = tool_name.lower().strip()
    if tool_name in TOOLS:
        return TOOLS[tool_name](**kwargs)
    return f'Unknown tool: {tool_name}'

def get_available_tools():
    return list(TOOLS.keys())
