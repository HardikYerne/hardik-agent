from voice.speech_to_text import transcribe
from voice.text_to_speech import speak
from tools.tool_registry import execute_tool

def voice_to_tool():
    speak("I am listening. Say a command.")
    text = transcribe()
    print(f"You said: {text}")

    # normalize text
    text = text.lower().strip()

    if any(word in text for word in ["chrome", "browser", "internet", "google"]):
        result = execute_tool("open_chrome")
    elif any(word in text for word in ["code", "vscode", "vs code", "editor"]):
        result = execute_tool("open_vscode")
    elif any(word in text for word in ["notepad", "note", "text editor"]):
        result = execute_tool("open_notepad")
    elif any(word in text for word in ["folder", "directory", "new folder"]):
        result = execute_tool("create_folder")
    else:
        result = f"I heard: {text}. Please try again."

    speak(result)

if __name__ == "__main__":
    voice_to_tool()