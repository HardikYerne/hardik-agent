from agent.brain import process_command

print('Testing AI brain with Ollama')
print('=' * 40)

result = process_command('launch my internet browser')
print(f'Result: {result}')
print()

result = process_command('I want to write some code')
print(f'Result: {result}')
print()

result = process_command('make a new folder on my desktop')
print(f'Result: {result}')
