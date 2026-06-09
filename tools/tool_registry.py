from tools.app_tools import (
    open_chrome, open_vscode, open_notepad,
    open_file_manager, open_task_manager,
    open_calculator, open_settings,
    create_folder, shutdown_pc,
    open_youtube, open_gmail
)
from automation.gui_automation import (
    take_screenshot, increase_volume,
    decrease_volume, mute_volume,
    minimize_window, maximize_window,
    close_window, show_desktop, lock_screen
)
from automation.browser_automation import (
    open_chrome_and_search,
    open_youtube_and_search,
    open_url
)
from automation.system_automation import (
    get_battery_status, get_cpu_usage,
    get_ram_usage, get_disk_usage,
    get_current_time, get_ip_address,
    list_running_apps, empty_recycle_bin,
    get_weather
)

TOOLS = {
    'open_chrome': open_chrome,
    'open_browser': open_chrome,
    'open_vscode': open_vscode,
    'open_notepad': open_notepad,
    'open_file_manager': open_file_manager,
    'file_manager': open_file_manager,
    'open_task_manager': open_task_manager,
    'open_calculator': open_calculator,
    'open_settings': open_settings,
    'create_folder': create_folder,
    'shutdown_pc': shutdown_pc,
    'open_youtube': open_youtube,
    'open_gmail': open_gmail,
    'take_screenshot': take_screenshot,
    'increase_volume': increase_volume,
    'decrease_volume': decrease_volume,
    'mute_volume': mute_volume,
    'minimize_window': minimize_window,
    'maximize_window': maximize_window,
    'close_window': close_window,
    'show_desktop': show_desktop,
    'lock_screen': lock_screen,
    'search_google': open_chrome_and_search,
    'search_youtube': open_youtube_and_search,
    'open_url': open_url,
    'get_battery': get_battery_status,
    'get_cpu': get_cpu_usage,
    'get_ram': get_ram_usage,
    'get_disk': get_disk_usage,
    'get_time': get_current_time,
    'get_ip': get_ip_address,
    'list_apps': list_running_apps,
    'empty_recycle_bin': empty_recycle_bin,
    'get_weather': get_weather,
}

def execute_tool(tool_name, **kwargs):
    tool_name = tool_name.lower().strip()
    if tool_name in TOOLS:
        return TOOLS[tool_name](**kwargs)
    return f'Unknown tool: {tool_name}'

def get_available_tools():
    return list(TOOLS.keys())
