import chromadb
import os
from pathlib import Path
from datetime import datetime

# setup chromadb storage path
MEMORY_DIR = Path.home() / '.hardik-agent' / 'memory'
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

# initialize chromadb
client = chromadb.PersistentClient(path=str(MEMORY_DIR))

# create collections
command_history = client.get_or_create_collection('command_history')
user_preferences = client.get_or_create_collection('user_preferences')
app_memory = client.get_or_create_collection('app_memory')

def save_command(command: str, result: str):
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        command_history.add(
            documents=[command],
            metadatas=[{'result': result, 'time': timestamp}],
            ids=[f'cmd_{timestamp}']
        )
    except Exception as e:
        print(f'Memory save error: {e}')

def get_recent_commands(limit=5):
    try:
        results = command_history.get()
        docs = results.get('documents', [])
        metas = results.get('metadatas', [])
        recent = list(zip(docs, metas))[-limit:]
        return recent
    except Exception as e:
        print(f'Memory get error: {e}')
        return []

def save_preference(key: str, value: str):
    try:
        existing = user_preferences.get(ids=[key])
        if existing['ids']:
            user_preferences.update(
                documents=[value],
                ids=[key]
            )
        else:
            user_preferences.add(
                documents=[value],
                metadatas=[{'key': key}],
                ids=[key]
            )
        print(f'Preference saved: {key} = {value}')
    except Exception as e:
        print(f'Preference save error: {e}')

def get_preference(key: str):
    try:
        result = user_preferences.get(ids=[key])
        if result['documents']:
            return result['documents'][0]
        return None
    except Exception as e:
        print(f'Preference get error: {e}')
        return None

def save_app_path(app_name: str, path: str):
    try:
        app_memory.add(
            documents=[path],
            metadatas=[{'app': app_name}],
            ids=[f'app_{app_name}']
        )
        print(f'App path saved: {app_name} = {path}')
    except Exception as e:
        print(f'App path save error: {e}')

def get_app_path(app_name: str):
    try:
        result = app_memory.get(ids=[f'app_{app_name}'])
        if result['documents']:
            return result['documents'][0]
        return None
    except Exception as e:
        return None

def search_memory(query: str, limit=3):
    try:
        results = command_history.query(
            query_texts=[query],
            n_results=limit
        )
        docs = results.get('documents', [[]])[0]
        metas = results.get('metadatas', [[]])[0]
        return list(zip(docs, metas))
    except Exception as e:
        print(f'Search error: {e}')
        return []

def get_memory_summary():
    try:
        total = command_history.count()
        recent = get_recent_commands(3)
        summary = f'Total commands remembered: {total}\n'
        if recent:
            summary += 'Recent commands:\n'
            for cmd, meta in recent:
                summary += f'- {cmd}\n'
        return summary
    except Exception as e:
        return 'Memory system ready'
