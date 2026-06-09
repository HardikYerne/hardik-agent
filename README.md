# Hardik Agent - Voice Controlled AI Desktop Assistant

## Overview
Hardik Agent is a production-grade voice-controlled AI desktop assistant that allows users to control their entire operating system using natural language voice commands. No typing required - just speak and your computer responds.

## Features
- Voice controlled OS automation
- Natural language understanding using Ollama + Llama3
- Open any application by voice
- Open any website by voice
- Send WhatsApp messages by voice
- Search Google and YouTube by voice
- System monitoring (battery, CPU, RAM, disk)
- Screenshot capture by voice
- Volume control by voice
- File and folder management by voice
- Window management by voice
- Secure user authentication
- Works 100% offline after setup
- Cross platform - Windows, Linux, MacOS

## Tech Stack
| Component | Technology |
|-----------|------------|
| Language | Python 3.12 |
| Voice STT | OpenAI Whisper |
| AI Brain | Ollama + Llama3.2 |
| Agent Framework | LangChain + LangGraph |
| TTS | pyttsx3 |
| GUI Automation | pyautogui |
| CLI | Typer |
| Auth | bcrypt |
| Memory | ChromaDB |

## Architecture
Voice Input
↓
Whisper STT
↓
LangGraph Runtime
↓
Ollama AI Brain
↓
LangChain Tools
↓
OS Automation
↓
Voice Response
## Installation

### Requirements
- Python 3.12+
- Windows 10/11 (Linux and MacOS supported)
- Microphone
- 8GB RAM minimum
- 10GB free disk space
- Internet connection for initial setup only

### Install
`ash
pip install hardik-agent
`

### Setup
`ash
hardik-agent setup
`

This automatically:
- Detects your operating system
- Installs FFmpeg
- Installs Ollama
- Downloads Llama3 AI model
- Creates your secure account

### Start
`ash
hardik-agent start
`

## Usage

### Voice Commands

#### Open Applications
"open chrome"
"open spotify"
"open whatsapp"
"open telegram"
"open vs code"
"open notepad"
"open calculator"
"open file manager"
"open task manager""open chrome"
"open spotify"
"open whatsapp"
"open telegram"
"open vs code"
"open notepad"
"open calculator"
"open file manager"
"open task manager"


#### Open Websites
"open youtube"
"open netflix"
"open chatgpt"
"open instagram"
"open gmail"
"open whatsapp web"

#### Search

"search python tutorials on google"
"search lofi music on youtube"
"search weather in Mumbai"

#### Send WhatsApp Message
"send whatsapp message to John hello how are you"
"message mom I am coming home"

#### System Information
"what time is it"
"check my battery"
"check CPU usage"
"check RAM usage"
"check disk space"
"what is my IP address"

#### System Control
"take a screenshot"
"increase volume"
"decrease volume"
"mute volume"
"minimize window"
"maximize window"
"close window"
"show desktop"
"lock screen"
"shutdown computer"

#### File Management
"create a folder called projects"
"create new folder"

## Project Structure
hardik-agent/
│
├── main.py
├── requirements.txt
├── .env
│
├── cli/
│   ├── commands.py
│   └── setup_manager.py
│
├── config/
│   └── settings.py
│
├── auth/
│   ├── signup.py
│   ├── login.py
│   ├── password_manager.py
│   └── session.py
│
├── voice/
│   ├── microphone.py
│   ├── speech_to_text.py
│   └── text_to_speech.py
│
├── agent/
│   ├── brain.py
│   ├── langchain_brain.py
│   └── langgraph_brain.py
│
├── tools/
│   ├── app_tools.py
│   └── tool_registry.py
│
├── automation/
│   ├── gui_automation.py
│   ├── browser_automation.py
│   ├── system_automation.py
│   └── whatsapp.py
│
├── runtime/
│   ├── event_loop.py
│   ├── startup.py
│   └── tray.py
│
├── memory/
│   └── memory_manager.py
│
├── security/
│   ├── permissions.py
│   └── safe_execution.py
│
└── logs/
└── agent.log

## Development Phases
- Phase 1 - CLI Foundation
- Phase 2 - Authentication System
- Phase 3 - Voice Pipeline
- Phase 4 - Tool Execution
- Phase 5 - Voice Controls OS
- Phase 6 - Ollama AI Brain
- Phase 7 - Continuous Runtime
- Phase 8 - GUI Automation
- Phase 9 - LangChain + LangGraph
- Phase 10 - Memory System (coming soon)
- Phase 11 - Wake Word (coming soon)
- Phase 12 - Background Service (coming soon)
- Phase 13 - GUI Dashboard (coming soon)
- Phase 14 - PyPI Package (coming soon)

## How It Works
1. User speaks a command
2. Whisper converts speech to text
3. LangGraph manages the workflow
4. Ollama AI understands the intent
5. LangChain selects the right tool
6. Tool executes on the operating system
7. Result is spoken back to user

## Privacy
- All AI processing runs locally on your machine
- No data sent to external servers
- No API keys required
- No internet needed after setup
- Your commands never leave your computer

## Security
- Encrypted password storage using bcrypt
- Local profile stored at ~/.hardik-agent/
- Dangerous commands require confirmation
- No arbitrary code execution

## Future Features
- Wake word detection
- Background runtime service
- System tray application
- GUI dashboard
- Plugin system
- Memory and personalization
- Multi language support
- MCP integration
- Computer vision
- Autonomous workflows

## Author
Hardik Yerne

## License
MIT License
