import json
from datetime import datetime

class ConversationContext:
    def __init__(self):
        self.history = []
        self.current_platform = None
        self.current_contact = None
        self.current_app = None
        self.last_action = None
        self.waiting_for = None

    def update(self, user_input, action, result):
        self.history.append({
            'time': datetime.now().strftime('%H:%M:%S'),
            'user': user_input,
            'action': action,
            'result': result
        })
        if len(self.history) > 10:
            self.history = self.history[-10:]

    def get_context_summary(self):
        if not self.history:
            return ''
        recent = self.history[-3:]
        summary = 'Recent conversation:\n'
        for h in recent:
            summary += f'User: {h["user"]}\n'
            summary += f'Action: {h["action"]}\n'
        return summary

    def set_platform(self, platform):
        self.current_platform = platform

    def set_contact(self, contact):
        self.current_contact = contact

    def set_app(self, app):
        self.current_app = app

    def set_waiting(self, waiting_for):
        self.waiting_for = waiting_for

    def clear_waiting(self):
        self.waiting_for = None

    def reset_contact(self):
        self.current_contact = None
        self.current_platform = None

context = ConversationContext()