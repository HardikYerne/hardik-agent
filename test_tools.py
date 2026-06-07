from tools.tool_registry import execute_tool, get_available_tools

print("Available tools:", get_available_tools())
print()

# test opening chrome
result = execute_tool("open_chrome")
print(result)