DANGEROUS_COMMANDS = ['shutdown', 'shutdown_pc', 'lock_screen', 'close_window', 'empty_recycle_bin']
BLOCKED_COMMANDS = ['format_disk', 'delete_system']

def is_dangerous(action):
    return action.lower() in DANGEROUS_COMMANDS

def is_blocked(action):
    return action.lower() in BLOCKED_COMMANDS

def get_confirmation_message(action):
    messages = {
        'shutdown': 'Are you sure you want to shutdown the computer?',
        'shutdown_pc': 'Are you sure you want to shutdown the computer?',
        'lock_screen': 'Are you sure you want to lock the screen?',
        'close_window': 'Are you sure you want to close the current window?',
        'empty_recycle_bin': 'Are you sure you want to empty the recycle bin?',
    }
    return messages.get(action.lower(), f'Are you sure you want to {action}?')
