# I Built a Voice-Controlled AI Desktop Assistant in Python — Here's How

## It opens Chrome, sends WhatsApp messages, checks your battery, and controls your entire computer. Just by speaking.

---

After months of building, I finally launched **Hexa** — a voice-controlled AI desktop assistant that lets you control your entire operating system using natural language voice commands.

No keyboard. No mouse. Just speak.

```bash
pip install hexa-agent
hexa-agent setup
hexa-agent start
```

Here is the full story of how I built it, what I learned, and how you can install it right now.

---

## What is Hexa?

Hexa is an AI desktop assistant that:

- Understands any natural language voice command
- Opens any app or website on your computer
- Sends WhatsApp messages by voice
- Checks system info (battery, CPU, RAM, disk)
- Controls volume, screenshots, window management
- Runs 100% offline after setup
- Works on Windows, Linux, and Mac

The best part? It runs completely locally on your machine. No cloud. No API costs. No privacy concerns. Your voice commands never leave your computer.

---

## Why I Built This

I am an AI/ML engineer and I wanted to build something that goes beyond training models and notebooks.

I wanted to build a real AI product — something that solves an actual problem and that real users can install and use.

Voice-controlled OS automation felt like the perfect project because it combines:

- Speech AI (Whisper)
- LLM reasoning (Ollama + Llama3)
- Desktop automation (pyautogui)
- Agent architecture (LangChain + LangGraph)
- Real product engineering (PyPI packaging)

All in one system.

---

## The Architecture

The complete pipeline looks like this:

```
You speak a command
        ↓
Google Speech Recognition hears it
        ↓
Ollama + Llama3 understands the meaning
        ↓
LangGraph manages the workflow
        ↓
LangChain selects the right tool
        ↓
Python executes on your OS
        ↓
Hexa speaks the result back
```

### Layer 1 — Voice Input

I used Google Speech Recognition with Indian English language settings for better accent support. The microphone captures your voice, processes it, and converts it to text.

```python
import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    audio = recognizer.listen(source, timeout=8)
    text = recognizer.recognize_google(audio, language='en-IN')
```

### Layer 2 — AI Brain (Ollama + LangGraph)

This is the most important part. I used Ollama to run Llama3 locally on the user's machine. No OpenAI API needed. No costs. No internet after setup.

LangGraph manages the stateful workflow — it handles multi-step commands like "open chrome and search for python tutorials."

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node('understand', understand_node)
workflow.add_node('execute', execute_node)
workflow.add_node('respond', respond_node)
```

### Layer 3 — Tool Execution

The AI never directly executes code. Instead it selects from a registry of safe, predefined functions.

```python
TOOLS = {
    'open_chrome': open_chrome,
    'open_vscode': open_vscode,
    'create_folder': create_folder,
    'shutdown_pc': shutdown_pc,
}
```

The AI decides which tool to call. Python executes it. This is the foundation of safe AI agent architecture.

### Layer 4 — Memory System

I used ChromaDB to give Hexa persistent memory. It remembers your commands, preferences, and workflows.

```python
command_history.add(
    documents=[command],
    metadatas=[{'result': result, 'time': timestamp}],
    ids=[f'cmd_{timestamp}']
)
```

---

## What Hexa Can Do

Here are some of the voice commands that work right now:

**Open any app:**

```
"open chrome"
"open spotify"
"open whatsapp"
"open discord"
"open vs code"
```

**Open any website:**

```
"open netflix"
"open instagram"
"open chatgpt"
"open gmail"
"open youtube"
```

**Search:**

```
"search python tutorials on google"
"search lofi music on youtube"
```

**Send WhatsApp message:**

```
"send whatsapp message to John hello how are you"
"message mom I am coming home"
```

**System info:**

```
"what time is it"
"check my battery"
"check RAM usage"
"what is my IP address"
```

**System control:**

```
"take a screenshot"
"increase volume"
"lock screen"
"show desktop"
```

---

## The Tech Stack

| Component       | Technology                |
| --------------- | ------------------------- |
| Language        | Python 3.12               |
| Voice STT       | Google Speech Recognition |
| AI Model        | Ollama + Llama3.2         |
| Agent Framework | LangChain + LangGraph     |
| Memory          | ChromaDB                  |
| GUI             | CustomTkinter             |
| TTS             | pyttsx3                   |
| Automation      | pyautogui                 |
| Auth            | bcrypt                    |
| Packaging       | PyPI                      |

---

## The GUI Dashboard

I built a dark mode GUI dashboard using CustomTkinter that shows:

- Live microphone status (green when active)
- Command history with color-coded logs
  - Green = successful commands
  - Red = errors
  - Blue = info messages
  - White = your voice input
- Real-time CPU, RAM, Disk, Battery stats
- Quick command buttons
- Command counter
- Type commands directly without voice

---

## The Hardest Parts

### 1. Voice Recognition Accuracy

Getting Whisper to accurately transcribe Indian English accents was the biggest challenge. I switched from Whisper to Google Speech Recognition with `language='en-IN'` which improved accuracy significantly.

### 2. LLM Tool Calling

Small models like Llama3.2:1b sometimes return malformed JSON. I built a robust JSON extraction function that handles edge cases:

```python
def extract_json(text):
    text = text.strip()
    while text.endswith('}}'):
        text = text[:-1]
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return json.loads(text[start:end+1])
```

### 3. Cross-Platform Compatibility

Making the same code work on Windows, Linux, and Mac required careful handling of file paths, app launching commands, and system-specific behaviors.

### 4. RAM Limitations

The full Llama3 model needs 4.6GB RAM. On laptops with limited RAM this fails. I switched to `llama3.2:1b` which needs only 1GB and works much better on consumer hardware.

---

## Security

Since Hexa controls your operating system, security is critical.

- Passwords are hashed using bcrypt — never stored in plain text
- Dangerous commands (shutdown, lock screen) require voice confirmation
- Blocked commands (format disk) are completely prevented
- All actions are logged to a security audit file
- The AI never executes arbitrary code — only predefined safe functions

---

## How to Install

```bash
# Install Python 3.12 from python.org

# Install Hexa
pip install hexa-agent

# Install Ollama from ollama.com
# Then download the AI model
ollama pull llama3.2:1b

# Setup Hexa
hexa-agent setup

# Start Hexa
hexa-agent start

# Or launch the GUI dashboard
hexa-agent dashboard
```

---

## What I Learned

Building Hexa taught me more about real AI engineering than any course or tutorial ever could.

**1. AI agents are about orchestration, not models.**
The intelligence of Hexa comes from how the components are connected — not from the model itself. LangGraph, tool registries, memory systems — these are what make it smart.

**2. Local AI is the future.**
Running Llama3 locally means zero API costs, complete privacy, and offline functionality. For desktop assistants, local models are superior to cloud APIs.

**3. Voice recognition is harder than it looks.**
Accents, background noise, microphone quality — all of these affect accuracy. Choosing the right STT library and settings matters enormously.

**4. Real products need packaging.**
Writing code is only half the work. Making it installable, documentable, and maintainable is the other half. Publishing to PyPI taught me how real Python packages work.

**5. Build incrementally.**
I built Hexa in 18 phases — one at a time, one working goal per phase. This approach prevented overwhelm and kept me making consistent progress.

---

## What's Next

I am planning to add:

- Hindi and Marathi language support
- Plugin system for Spotify, Gmail, Calendar
- MCP integration for advanced tool communication
- Computer vision for visual screen understanding
- Mobile companion app for remote control
- Auto updater for seamless version management

---

## Try It Now

```bash
pip install hexa-agent
```

PyPI: https://pypi.org/project/hexa-agent

---

## Final Thoughts

Hexa started as a personal project to learn AI systems engineering. It became a real product that anyone can install and use.

If you are an AI/ML engineer who only knows model training and notebooks — I strongly recommend building an AI agent project like this. It will teach you skills that no amount of theoretical study can replace.

The future of AI is not just training better models. It is building better systems around those models.

---

*Built with Python, Ollama, LangChain, LangGraph, and a lot of debugging.*

*Hardik Yerne — AI/ML Engineer*

---

**Tags:** Python, AI, Machine Learning, Voice Assistant, LangChain, LangGraph, Ollama, Desktop Automation, Open Source

# I Built a Voice-Controlled AI Desktop Assistant in Python — Here's How

## It opens Chrome, sends WhatsApp messages, checks your battery, and controls your entire computer. Just by speaking.

---

After months of building, I finally launched **Hexa** — a voice-controlled AI desktop assistant that lets you control your entire operating system using natural language voice commands.

No keyboard. No mouse. Just spea

# I Built a Voice-Controlled AI Desktop Assistant in Python — Here's How

## It opens Chrome, sends WhatsApp messages, checks your battery, and controls your entire computer. Just by speaking.

---

After months of building, I finally launched **Hexa** — a voice-controlled AI desktop assistant that lets you control your entire operating system using natural language voice commands.

No keyboard. No mouse. Just speak.

```bash
pip install hexa-agent
hexa-agent setup
hexa-agent start
```

Here is the full story of how I built it, what I learned, and how you can install it right now.

---

## What is Hexa?

Hexa is an AI desktop assistant that:

- Understands any natural language voice command
- Opens any app or website on your computer
- Sends WhatsApp messages by voice
- Checks system info (battery, CPU, RAM, disk)
- Controls volume, screenshots, window management
- Runs 100% offline after setup
- Works on Windows, Linux, and Mac

The best part? It runs completely locally on your machine. No cloud. No API costs. No privacy concerns. Your voice commands never leave your computer.

---

## Why I Built This

I am an AI/ML engineer and I wanted to build something that goes beyond training models and notebooks.

I wanted to build a real AI product — something that solves an actual problem and that real users can install and use.

Voice-controlled OS automation felt like the perfect project because it combines:

- Speech AI (Whisper)
- LLM reasoning (Ollama + Llama3)
- Desktop automation (pyautogui)
- Agent architecture (LangChain + LangGraph)
- Real product engineering (PyPI packaging)

All in one system.

---

## The Architecture

The complete pipeline looks like this:

```
You speak a command
        ↓
Google Speech Recognition hears it
        ↓
Ollama + Llama3 understands the meaning
        ↓
LangGraph manages the workflow
        ↓
LangChain selects the right tool
        ↓
Python executes on your OS
        ↓
Hexa speaks the result back
```

### Layer 1 — Voice Input

I used Google Speech Recognition with Indian English language settings for better accent support. The microphone captures your voice, processes it, and converts it to text.

```python
import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    audio = recognizer.listen(source, timeout=8)
    text = recognizer.recognize_google(audio, language='en-IN')
```

### Layer 2 — AI Brain (Ollama + LangGraph)

This is the most important part. I used Ollama to run Llama3 locally on the user's machine. No OpenAI API needed. No costs. No internet after setup.

LangGraph manages the stateful workflow — it handles multi-step commands like "open chrome and search for python tutorials."

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node('understand', understand_node)
workflow.add_node('execute', execute_node)
workflow.add_node('respond', respond_node)
```

### Layer 3 — Tool Execution

The AI never directly executes code. Instead it selects from a registry of safe, predefined functions.

```python
TOOLS = {
    'open_chrome': open_chrome,
    'open_vscode': open_vscode,
    'create_folder': create_folder,
    'shutdown_pc': shutdown_pc,
}
```

The AI decides which tool to call. Python executes it. This is the foundation of safe AI agent architecture.

### Layer 4 — Memory System

I used ChromaDB to give Hexa persistent memory. It remembers your commands, preferences, and workflows.

```python
command_history.add(
    documents=[command],
    metadatas=[{'result': result, 'time': timestamp}],
    ids=[f'cmd_{timestamp}']
)
```

---

## What Hexa Can Do

Here are some of the voice commands that work right now:

**Open any app:**

```
"open chrome"
"open spotify"
"open whatsapp"
"open discord"
"open vs code"
```

**Open any website:**

```
"open netflix"
"open instagram"
"open chatgpt"
"open gmail"
"open youtube"
```

**Search:**

```
"search python tutorials on google"
"search lofi music on youtube"
```

**Send WhatsApp message:**

```
"send whatsapp message to John hello how are you"
"message mom I am coming home"
```

**System info:**

```
"what time is it"
"check my battery"
"check RAM usage"
"what is my IP address"
```

**System control:**

```
"take a screenshot"
"increase volume"
"lock screen"
"show desktop"
```

---

## The Tech Stack

| Component       | Technology                |
| --------------- | ------------------------- |
| Language        | Python 3.12               |
| Voice STT       | Google Speech Recognition |
| AI Model        | Ollama + Llama3.2         |
| Agent Framework | LangChain + LangGraph     |
| Memory          | ChromaDB                  |
| GUI             | CustomTkinter             |
| TTS             | pyttsx3                   |
| Automation      | pyautogui                 |
| Auth            | bcrypt                    |
| Packaging       | PyPI                      |

---

## The GUI Dashboard

I built a dark mode GUI dashboard using CustomTkinter that shows:

- Live microphone status (green when active)
- Command history with color-coded logs
  - Green = successful commands
  - Red = errors
  - Blue = info messages
  - White = your voice input
- Real-time CPU, RAM, Disk, Battery stats
- Quick command buttons
- Command counter
- Type commands directly without voice

---

## The Hardest Parts

### 1. Voice Recognition Accuracy

Getting Whisper to accurately transcribe Indian English accents was the biggest challenge. I switched from Whisper to Google Speech Recognition with `language='en-IN'` which improved accuracy significantly.

### 2. LLM Tool Calling

Small models like Llama3.2:1b sometimes return malformed JSON. I built a robust JSON extraction function that handles edge cases:

```python
def extract_json(text):
    text = text.strip()
    while text.endswith('}}'):
        text = text[:-1]
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return json.loads(text[start:end+1])
```

### 3. Cross-Platform Compatibility

Making the same code work on Windows, Linux, and Mac required careful handling of file paths, app launching commands, and system-specific behaviors.

### 4. RAM Limitations

The full Llama3 model needs 4.6GB RAM. On laptops with limited RAM this fails. I switched to `llama3.2:1b` which needs only 1GB and works much better on consumer hardware.

---

## Security

Since Hexa controls your operating system, security is critical.

- Passwords are hashed using bcrypt — never stored in plain text
- Dangerous commands (shutdown, lock screen) require voice confirmation
- Blocked commands (format disk) are completely prevented
- All actions are logged to a security audit file
- The AI never executes arbitrary code — only predefined safe functions

---

## How to Install

```bash
# Install Python 3.12 from python.org

# Install Hexa
pip install hexa-agent

# Install Ollama from ollama.com
# Then download the AI model
ollama pull llama3.2:1b

# Setup Hexa
hexa-agent setup

# Start Hexa
hexa-agent start

# Or launch the GUI dashboard
hexa-agent dashboard
```

---

## What I Learned

Building Hexa taught me more about real AI engineering than any course or tutorial ever could.

**1. AI agents are about orchestration, not models.**
The intelligence of Hexa comes from how the components are connected — not from the model itself. LangGraph, tool registries, memory systems — these are what make it smart.

**2. Local AI is the future.**
Running Llama3 locally means zero API costs, complete privacy, and offline functionality. For desktop assistants, local models are superior to cloud APIs.

**3. Voice recognition is harder than it looks.**
Accents, background noise, microphone quality — all of these affect accuracy. Choosing the right STT library and settings matters enormously.

**4. Real products need packaging.**
Writing code is only half the work. Making it installable, documentable, and maintainable is the other half. Publishing to PyPI taught me how real Python packages work.

**5. Build incrementally.**
I built Hexa in 18 phases — one at a time, one working goal per phase. This approach prevented overwhelm and kept me making consistent progress.

---

## What's Next

I am planning to add:

- Hindi and Marathi language support
- Plugin system for Spotify, Gmail, Calendar
- MCP integration for advanced tool communication
- Computer vision for visual screen understanding
- Mobile companion app for remote control
- Auto updater for seamless version management

---

## Try It Now

```bash
pip install hexa-agent
```

PyPI: https://pypi.org/project/hexa-agent

---

## Final Thoughts

Hexa started as a personal project to learn AI systems engineering. It became a real product that anyone can install and use.

If you are an AI/ML engineer who only knows model training and notebooks — I strongly recommend building an AI agent project like this. It will teach you skills that no amount of theoretical study can replace.

The future of AI is not just training better models. It is building better systems around those models.

---

*Built with Python, Ollama, LangChain, LangGraph, and a lot of debugging.*

*Hardik Yerne — AI/ML Engineer*

---

**Tags:** Python, AI, Machine Learning, Voice Assistant, LangChain, LangGraph, Ollama, Desktop Automation, Open Source

```bash
pip install hexa-agent
hexa-agent setup
hexa-agent start
```

Here is the full story of how I built it, what I learned, and how you can install it right now.

---

## What is Hexa?

Hexa is an AI desktop assistant that:

- Understands any natural language voice command
- Opens any app or website on your computer
- Sends WhatsApp messages by voice
- Checks system info (battery, CPU, RAM, disk)
- Controls volume, screenshots, window management
- Runs 100% offline after setup
- Works on Windows, Linux, and Mac

The best part? It runs completely locally on your machine. No cloud. No API costs. No privacy concerns. Your voice commands never leave your computer.

---

## Why I Built This

I am an AI/ML engineer and I wanted to build something that goes beyond training models and notebooks.

I wanted to build a real AI product — something that solves an actual problem and that real users can install and use.

Voice-controlled OS automation felt like the perfect project because it combines:

- Speech AI (Whisper)
- LLM reasoning (Ollama + Llama3)
- Desktop automation (pyautogui)
- Agent architecture (LangChain + LangGraph)
- Real product engineering (PyPI packaging)

All in one system.

---

## The Architecture

The complete pipeline looks like this:

```
You speak a command
        ↓
Google Speech Recognition hears it
        ↓
Ollama + Llama3 understands the meaning
        ↓
LangGraph manages the workflow
        ↓
LangChain selects the right tool
        ↓
Python executes on your OS
        ↓
Hexa speaks the result back
```

### Layer 1 — Voice Input

I used Google Speech Recognition with Indian English language settings for better accent support. The microphone captures your voice, processes it, and converts it to text.

```python
import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    audio = recognizer.listen(source, timeout=8)
    text = recognizer.recognize_google(audio, language='en-IN')
```

### Layer 2 — AI Brain (Ollama + LangGraph)

This is the most important part. I used Ollama to run Llama3 locally on the user's machine. No OpenAI API needed. No costs. No internet after setup.

LangGraph manages the stateful workflow — it handles multi-step commands like "open chrome and search for python tutorials."

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node('understand', understand_node)
workflow.add_node('execute', execute_node)
workflow.add_node('respond', respond_node)
```

### Layer 3 — Tool Execution

The AI never directly executes code. Instead it selects from a registry of safe, predefined functions.

```python
TOOLS = {
    'open_chrome': open_chrome,
    'open_vscode': open_vscode,
    'create_folder': create_folder,
    'shutdown_pc': shutdown_pc,
}
```

The AI decides which tool to call. Python executes it. This is the foundation of safe AI agent architecture.

### Layer 4 — Memory System

I used ChromaDB to give Hexa persistent memory. It remembers your commands, preferences, and workflows.

```python
command_history.add(
    documents=[command],
    metadatas=[{'result': result, 'time': timestamp}],
    ids=[f'cmd_{timestamp}']
)
```

---

## What Hexa Can Do

Here are some of the voice commands that work right now:

**Open any app:**

```
"open chrome"
"open spotify"
"open whatsapp"
"open discord"
"open vs code"
```

**Open any website:**

```
"open netflix"
"open instagram"
"open chatgpt"
"open gmail"
"open youtube"
```

**Search:**

```
"search python tutorials on google"
"search lofi music on youtube"
```

**Send WhatsApp message:**

```
"send whatsapp message to John hello how are you"
"message mom I am coming home"
```

**System info:**

```
"what time is it"
"check my battery"
"check RAM usage"
"what is my IP address"
```

**System control:**

```
"take a screenshot"
"increase volume"
"lock screen"
"show desktop"
```

---

## The Tech Stack

| Component       | Technology                |
| --------------- | ------------------------- |
| Language        | Python 3.12               |
| Voice STT       | Google Speech Recognition |
| AI Model        | Ollama + Llama3.2         |
| Agent Framework | LangChain + LangGraph     |
| Memory          | ChromaDB                  |
| GUI             | CustomTkinter             |
| TTS             | pyttsx3                   |
| Automation      | pyautogui                 |
| Auth            | bcrypt                    |
| Packaging       | PyPI                      |

---

## The GUI Dashboard

I built a dark mode GUI dashboard using CustomTkinter that shows:

- Live microphone status (green when active)
- Command history with color-coded logs
  - Green = successful commands
  - Red = errors
  - Blue = info messages
  - White = your voice input
- Real-time CPU, RAM, Disk, Battery stats
- Quick command buttons
- Command counter
- Type commands directly without voice

---

## The Hardest Parts

### 1. Voice Recognition Accuracy

Getting Whisper to accurately transcribe Indian English accents was the biggest challenge. I switched from Whisper to Google Speech Recognition with `language='en-IN'` which improved accuracy significantly.

### 2. LLM Tool Calling

Small models like Llama3.2:1b sometimes return malformed JSON. I built a robust JSON extraction function that handles edge cases:

```python
def extract_json(text):
    text = text.strip()
    while text.endswith('}}'):
        text = text[:-1]
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return json.loads(text[start:end+1])
```

### 3. Cross-Platform Compatibility

Making the same code work on Windows, Linux, and Mac required careful handling of file paths, app launching commands, and system-specific behaviors.

### 4. RAM Limitations

The full Llama3 model needs 4.6GB RAM. On laptops with limited RAM this fails. I switched to `llama3.2:1b` which needs only 1GB and works much better on consumer hardware.

---

## Security

Since Hexa controls your operating system, security is critical.

- Passwords are hashed using bcrypt — never stored in plain text
- Dangerous commands (shutdown, lock screen) require voice confirmation
- Blocked commands (format disk) are completely prevented
- All actions are logged to a security audit file
- The AI never executes arbitrary code — only predefined safe functions

---

## How to Install

```bash
# Install Python 3.12 from python.org

# Install Hexa
pip install hexa-agent

# Install Ollama from ollama.com
# Then download the AI model
ollama pull llama3.2:1b

# Setup Hexa
hexa-agent setup

# Start Hexa
hexa-agent start

# Or launch the GUI dashboard
hexa-agent dashboard
```

---

## What I Learned

Building Hexa taught me more about real AI engineering than any course or tutorial ever could.

**1. AI agents are about orchestration, not models.**
The intelligence of Hexa comes from how the components are connected — not from the model itself. LangGraph, tool registries, memory systems — these are what make it smart.

**2. Local AI is the future.**
Running Llama3 locally means zero API costs, complete privacy, and offline functionality. For desktop assistants, local models are superior to cloud APIs.

**3. Voice recognition is harder than it looks.**
Accents, background noise, microphone quality — all of these affect accuracy. Choosing the right STT library and settings matters enormously.

**4. Real products need packaging.**
Writing code is only half the work. Making it installable, documentable, and maintainable is the other half. Publishing to PyPI taught me how real Python packages work.

**5. Build incrementally.**
I built Hexa in 18 phases — one at a time, one working goal per phase. This approach prevented overwhelm and kept me making consistent progress.

---

## What's Next

I am planning to add:

- Hindi and Marathi language support
- Plugin system for Spotify, Gmail, Calendar
- MCP integration for advanced tool communication
- Computer vision for visual screen understanding
- Mobile companion app for remote control
- Auto updater for seamless version management

---

## Try It Now

```bash
pip install hexa-agent
```

PyPI: https://pypi.org/project/hexa-agent

---

## Final Thoughts

Hexa started as a personal project to learn AI systems engineering. It became a real product that anyone can install and use.

If you are an AI/ML engineer who only knows model training and notebooks — I strongly recommend building an AI agent project like this. It will teach you skills that no amount of theoretical study can replace.

The future of AI is not just training better models. It is building better systems around those models.

---

*Built with Python, Ollama, LangChain, LangGraph, and a lot of debugging.*

*Hardik Yerne — AI/ML Engineer*

---





# I Built a Voice-Controlled AI Desktop Assistant in Python — Here's How

## It opens Chrome, sends WhatsApp messages, checks your battery, and controls your entire computer. Just by speaking.

---

After months of building, I finally launched **Hexa** — a voice-controlled AI desktop assistant that lets you control your entire operating system using natural language voice commands.

No keyboard. No mouse. Just speak.

```bash
pip install hexa-agent
hexa-agent setup
hexa-agent start
```

Here is the full story of how I built it, what I learned, and how you can install it right now.

---

## What is Hexa?

Hexa is an AI desktop assistant that:

- Understands any natural language voice command
- Opens any app or website on your computer
- Sends WhatsApp messages by voice
- Checks system info (battery, CPU, RAM, disk)
- Controls volume, screenshots, window management
- Runs 100% offline after setup
- Works on Windows, Linux, and Mac

The best part? It runs completely locally on your machine. No cloud. No API costs. No privacy concerns. Your voice commands never leave your computer.

---

## Why I Built This

I am an AI/ML engineer and I wanted to build something that goes beyond training models and notebooks.

I wanted to build a real AI product — something that solves an actual problem and that real users can install and use.

Voice-controlled OS automation felt like the perfect project because it combines:

- Speech AI (Whisper)
- LLM reasoning (Ollama + Llama3)
- Desktop automation (pyautogui)
- Agent architecture (LangChain + LangGraph)
- Real product engineering (PyPI packaging)

All in one system.

---

## The Architecture

The complete pipeline looks like this:

```
You speak a command
        ↓
Google Speech Recognition hears it
        ↓
Ollama + Llama3 understands the meaning
        ↓
LangGraph manages the workflow
        ↓
LangChain selects the right tool
        ↓
Python executes on your OS
        ↓
Hexa speaks the result back
```

### Layer 1 — Voice Input

I used Google Speech Recognition with Indian English language settings for better accent support. The microphone captures your voice, processes it, and converts it to text.

```python
import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    audio = recognizer.listen(source, timeout=8)
    text = recognizer.recognize_google(audio, language='en-IN')
```

### Layer 2 — AI Brain (Ollama + LangGraph)

This is the most important part. I used Ollama to run Llama3 locally on the user's machine. No OpenAI API needed. No costs. No internet after setup.

LangGraph manages the stateful workflow — it handles multi-step commands like "open chrome and search for python tutorials."

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node('understand', understand_node)
workflow.add_node('execute', execute_node)
workflow.add_node('respond', respond_node)
```

### Layer 3 — Tool Execution

The AI never directly executes code. Instead it selects from a registry of safe, predefined functions.

```python
TOOLS = {
    'open_chrome': open_chrome,
    'open_vscode': open_vscode,
    'create_folder': create_folder,
    'shutdown_pc': shutdown_pc,
}
```

The AI decides which tool to call. Python executes it. This is the foundation of safe AI agent architecture.

### Layer 4 — Memory System

I used ChromaDB to give Hexa persistent memory. It remembers your commands, preferences, and workflows.

```python
command_history.add(
    documents=[command],
    metadatas=[{'result': result, 'time': timestamp}],
    ids=[f'cmd_{timestamp}']
)
```

---

## What Hexa Can Do

Here are some of the voice commands that work right now:

**Open any app:**

```
"open chrome"
"open spotify"
"open whatsapp"
"open discord"
"open vs code"
```

**Open any website:**

```
"open netflix"
"open instagram"
"open chatgpt"
"open gmail"
"open youtube"
```

**Search:**

```
"search python tutorials on google"
"search lofi music on youtube"
```

**Send WhatsApp message:**

```
"send whatsapp message to John hello how are you"
"message mom I am coming home"
```

**System info:**

```
"what time is it"
"check my battery"
"check RAM usage"
"what is my IP address"
```

**System control:**

```
"take a screenshot"
"increase volume"
"lock screen"
"show desktop"
```

---

## The Tech Stack

| Component       | Technology                |
| --------------- | ------------------------- |
| Language        | Python 3.12               |
| Voice STT       | Google Speech Recognition |
| AI Model        | Ollama + Llama3.2         |
| Agent Framework | LangChain + LangGraph     |
| Memory          | ChromaDB                  |
| GUI             | CustomTkinter             |
| TTS             | pyttsx3                   |
| Automation      | pyautogui                 |
| Auth            | bcrypt                    |
| Packaging       | PyPI                      |

---

## The GUI Dashboard

I built a dark mode GUI dashboard using CustomTkinter that shows:

- Live microphone status (green when active)
- Command history with color-coded logs
  - Green = successful commands
  - Red = errors
  - Blue = info messages
  - White = your voice input
- Real-time CPU, RAM, Disk, Battery stats
- Quick command buttons
- Command counter
- Type commands directly without voice

---

## The Hardest Parts

### 1. Voice Recognition Accuracy

Getting Whisper to accurately transcribe Indian English accents was the biggest challenge. I switched from Whisper to Google Speech Recognition with `language='en-IN'` which improved accuracy significantly.

### 2. LLM Tool Calling

Small models like Llama3.2:1b sometimes return malformed JSON. I built a robust JSON extraction function that handles edge cases:

```python
def extract_json(text):
    text = text.strip()
    while text.endswith('}}'):
        text = text[:-1]
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return json.loads(text[start:end+1])
```

### 3. Cross-Platform Compatibility

Making the same code work on Windows, Linux, and Mac required careful handling of file paths, app launching commands, and system-specific behaviors.

### 4. RAM Limitations

The full Llama3 model needs 4.6GB RAM. On laptops with limited RAM this fails. I switched to `llama3.2:1b` which needs only 1GB and works much better on consumer hardware.

---

## Security

Since Hexa controls your operating system, security is critical.

- Passwords are hashed using bcrypt — never stored in plain text
- Dangerous commands (shutdown, lock screen) require voice confirmation
- Blocked commands (format disk) are completely prevented
- All actions are logged to a security audit file
- The AI never executes arbitrary code — only predefined safe functions

---

## How to Install

```bash
# Install Python 3.12 from python.org

# Install Hexa
pip install hexa-agent

# Install Ollama from ollama.com
# Then download the AI model
ollama pull llama3.2:1b

# Setup Hexa
hexa-agent setup

# Start Hexa
hexa-agent start

# Or launch the GUI dashboard
hexa-agent dashboard
```

---

## What I Learned

Building Hexa taught me more about real AI engineering than any course or tutorial ever could.

**1. AI agents are about orchestration, not models.**
The intelligence of Hexa comes from how the components are connected — not from the model itself. LangGraph, tool registries, memory systems — these are what make it smart.

**2. Local AI is the future.**
Running Llama3 locally means zero API costs, complete privacy, and offline functionality. For desktop assistants, local models are superior to cloud APIs.

**3. Voice recognition is harder than it looks.**
Accents, background noise, microphone quality — all of these affect accuracy. Choosing the right STT library and settings matters enormously.

**4. Real products need packaging.**
Writing code is only half the work. Making it installable, documentable, and maintainable is the other half. Publishing to PyPI taught me how real Python packages work.

**5. Build incrementally.**
I built Hexa in 18 phases — one at a time, one working goal per phase. This approach prevented overwhelm and kept me making consistent progress.

---

## What's Next

I am planning to add:

- Hindi and Marathi language support
- Plugin system for Spotify, Gmail, Calendar
- MCP integration for advanced tool communication
- Computer vision for visual screen understanding
- Mobile companion app for remote control
- Auto updater for seamless version management

---

## Try It Now

```bash
pip install hexa-agent
```

PyPI: https://pypi.org/project/hexa-agent

---

## Final Thoughts

Hexa started as a personal project to learn AI systems engineering. It became a real product that anyone can install and use.

If you are an AI/ML engineer who only knows model training and notebooks — I strongly recommend building an AI agent project like this. It will teach you skills that no amount of theoretical study can replace.

The future of AI is not just training better models. It is building better systems around those models.

---

*Built with Python, Ollama, LangChain, LangGraph, and a lot of debugging.*

*Hardik Yerne — AI/ML Engineer*

---

**Tags:** Python, AI, Machine Learning, Voice Assistant, LangChain, LangGraph, Ollama, Desktop Automation, Open Source

# I Built a Voice-Controlled AI Desktop Assistant in Python — Here's How

## It opens Chrome, sends WhatsApp messages, checks your battery, and controls your entire computer. Just by speaking.

---

After months of building, I finally launched **Hexa** — a voice-controlled AI desktop assistant that lets you control your entire operating system using natural language voice commands.

No keyboard. No mouse. Just speak.

```bash
pip install hexa-agent
hexa-agent setup
hexa-agent start
```

Here is the full story of how I built it, what I learned, and how you can install it right now.

---

## What is Hexa?

Hexa is an AI desktop assistant that:

- Understands any natural language voice command
- Opens any app or website on your computer
- Sends WhatsApp messages by voice
- Checks system info (battery, CPU, RAM, disk)
- Controls volume, screenshots, window management
- Runs 100% offline after setup
- Works on Windows, Linux, and Mac

The best part? It runs completely locally on your machine. No cloud. No API costs. No privacy concerns. Your voice commands never leave your computer.

---

## Why I Built This

I am an AI/ML engineer and I wanted to build something that goes beyond training models and notebooks.

I wanted to build a real AI product — something that solves an actual problem and that real users can install and use.

Voice-controlled OS automation felt like the perfect project because it combines:

- Speech AI (Whisper)
- LLM reasoning (Ollama + Llama3)
- Desktop automation (pyautogui)
- Agent architecture (LangChain + LangGraph)
- Real product engineering (PyPI packaging)

All in one system.

---

## The Architecture

The complete pipeline looks like this:

```
You speak a command
        ↓
Google Speech Recognition hears it
        ↓
Ollama + Llama3 understands the meaning
        ↓
LangGraph manages the workflow
        ↓
LangChain selects the right tool
        ↓
Python executes on your OS
        ↓
Hexa speaks the result back
```

### Layer 1 — Voice Input

I used Google Speech Recognition with Indian English language settings for better accent support. The microphone captures your voice, processes it, and converts it to text.

```python
import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    audio = recognizer.listen(source, timeout=8)
    text = recognizer.recognize_google(audio, language='en-IN')
```

### Layer 2 — AI Brain (Ollama + LangGraph)

This is the most important part. I used Ollama to run Llama3 locally on the user's machine. No OpenAI API needed. No costs. No internet after setup.

LangGraph manages the stateful workflow — it handles multi-step commands like "open chrome and search for python tutorials."

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node('understand', understand_node)
workflow.add_node('execute', execute_node)
workflow.add_node('respond', respond_node)
```

### Layer 3 — Tool Execution

The AI never directly executes code. Instead it selects from a registry of safe, predefined functions.

```python
TOOLS = {
    'open_chrome': open_chrome,
    'open_vscode': open_vscode,
    'create_folder': create_folder,
    'shutdown_pc': shutdown_pc,
}
```

The AI decides which tool to call. Python executes it. This is the foundation of safe AI agent architecture.

### Layer 4 — Memory System

I used ChromaDB to give Hexa persistent memory. It remembers your commands, preferences, and workflows.

```python
command_history.add(
    documents=[command],
    metadatas=[{'result': result, 'time': timestamp}],
    ids=[f'cmd_{timestamp}']
)
```

---

## What Hexa Can Do

Here are some of the voice commands that work right now:

**Open any app:**

```
"open chrome"
"open spotify"
"open whatsapp"
"open discord"
"open vs code"
```

**Open any website:**

```
"open netflix"
"open instagram"
"open chatgpt"
"open gmail"
"open youtube"
```

**Search:**

```
"search python tutorials on google"
"search lofi music on youtube"
```

**Send WhatsApp message:**

```
"send whatsapp message to John hello how are you"
"message mom I am coming home"
```

**System info:**

```
"what time is it"
"check my battery"
"check RAM usage"
"what is my IP address"
```

**System control:**

```
"take a screenshot"
"increase volume"
"lock screen"
"show desktop"
```

---

## The Tech Stack

| Component       | Technology                |
| --------------- | ------------------------- |
| Language        | Python 3.12               |
| Voice STT       | Google Speech Recognition |
| AI Model        | Ollama + Llama3.2         |
| Agent Framework | LangChain + LangGraph     |
| Memory          | ChromaDB                  |
| GUI             | CustomTkinter             |
| TTS             | pyttsx3                   |
| Automation      | pyautogui                 |
| Auth            | bcrypt                    |
| Packaging       | PyPI                      |

---

## The GUI Dashboard

I built a dark mode GUI dashboard using CustomTkinter that shows:

- Live microphone status (green when active)
- Command history with color-coded logs
  - Green = successful commands
  - Red = errors
  - Blue = info messages
  - White = your voice input
- Real-time CPU, RAM, Disk, Battery stats
- Quick command buttons
- Command counter
- Type commands directly without voice

---

## The Hardest Parts

### 1. Voice Recognition Accuracy

Getting Whisper to accurately transcribe Indian English accents was the biggest challenge. I switched from Whisper to Google Speech Recognition with `language='en-IN'` which improved accuracy significantly.

### 2. LLM Tool Calling

Small models like Llama3.2:1b sometimes return malformed JSON. I built a robust JSON extraction function that handles edge cases:

```python
def extract_json(text):
    text = text.strip()
    while text.endswith('}}'):
        text = text[:-1]
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return json.loads(text[start:end+1])
```

### 3. Cross-Platform Compatibility

Making the same code work on Windows, Linux, and Mac required careful handling of file paths, app launching commands, and system-specific behaviors.

### 4. RAM Limitations

The full Llama3 model needs 4.6GB RAM. On laptops with limited RAM this fails. I switched to `llama3.2:1b` which needs only 1GB and works much better on consumer hardware.

---

## Security

Since Hexa controls your operating system, security is critical.

- Passwords are hashed using bcrypt — never stored in plain text
- Dangerous commands (shutdown, lock screen) require voice confirmation
- Blocked commands (format disk) are completely prevented
- All actions are logged to a security audit file
- The AI never executes arbitrary code — only predefined safe functions

---

## How to Install

```bash
# Install Python 3.12 from python.org

# Install Hexa
pip install hexa-agent

# Install Ollama from ollama.com
# Then download the AI model
ollama pull llama3.2:1b

# Setup Hexa
hexa-agent setup

# Start Hexa
hexa-agent start

# Or launch the GUI dashboard
hexa-agent dashboard
```

---

## What I Learned

Building Hexa taught me more about real AI engineering than any course or tutorial ever could.

**1. AI agents are about orchestration, not models.**
The intelligence of Hexa comes from how the components are connected — not from the model itself. LangGraph, tool registries, memory systems — these are what make it smart.

**2. Local AI is the future.**
Running Llama3 locally means zero API costs, complete privacy, and offline functionality. For desktop assistants, local models are superior to cloud APIs.

**3. Voice recognition is harder than it looks.**
Accents, background noise, microphone quality — all of these affect accuracy. Choosing the right STT library and settings matters enormously.

**4. Real products need packaging.**
Writing code is only half the work. Making it installable, documentable, and maintainable is the other half. Publishing to PyPI taught me how real Python packages work.

**5. Build incrementally.**
I built Hexa in 18 phases — one at a time, one working goal per phase. This approach prevented overwhelm and kept me making consistent progress.

---

## What's Next

I am planning to add:

- Hindi and Marathi language support
- Plugin system for Spotify, Gmail, Calendar
- MCP integration for advanced tool communication
- Computer vision for visual screen understanding
- Mobile companion app for remote control
- Auto updater for seamless version management

---

## Try It Now

```bash
pip install hexa-agent
```

PyPI: https://pypi.org/project/hexa-agent

---

## Final Thoughts

Hexa started as a personal project to learn AI systems engineering. It became a real product that anyone can install and use.

If you are an AI/ML engineer who only knows model training and notebooks — I strongly recommend building an AI agent project like this. It will teach you skills that no amount of theoretical study can replace.

The future of AI is not just training better models. It is building better systems around those models.

---

*Built with Python, Ollama, LangChain, LangGraph, and a lot of debugging.*

*Hardik Yerne — AI/ML Engineer*

---

**Tags:** Python, AI, Machine Learning, Voice Assistant, LangChain, LangGraph, Ollama, Desktop Automation, Open Source

**Tags:** Python, AI, Machine Learning, Voice Assistant, LangChain, LangGraph, Ollama, Desktop Automation, Open Source

# I Built a Voice-Controlled AI Desktop Assistant in Python — Here's How

## It opens Chrome, sends WhatsApp messages, checks your battery, and controls your entire computer. Just by speaking.

---

After months of building, I finally launched **Hexa** — a voice-controlled AI desktop assistant that lets you control your entire operating system using natural language voice commands.

No keyboard. No mouse. Just speak.

```bash
pip install hexa-agent
hexa-agent setup
hexa-agent start
```

Here is the full story of how I built it, what I learned, and how you can install it right now.

---

## What is Hexa?

Hexa is an AI desktop assistant that:

- Understands any natural language voice command
- Opens any app or website on your computer
- Sends WhatsApp messages by voice
- Checks system info (battery, CPU, RAM, disk)
- Controls volume, screenshots, window management
- Runs 100% offline after setup
- Works on Windows, Linux, and Mac

The best part? It runs completely locally on your machine. No cloud. No API costs. No privacy concerns. Your voice commands never leave your computer.

---

## Why I Built This

I am an AI/ML engineer and I wanted to build something that goes beyond training models and notebooks.

I wanted to build a real AI product — something that solves an actual problem and that real users can install and use.

Voice-controlled OS automation felt like the perfect project because it combines:

- Speech AI (Whisper)
- LLM reasoning (Ollama + Llama3)
- Desktop automation (pyautogui)
- Agent architecture (LangChain + LangGraph)
- Real product engineering (PyPI packaging)

All in one system.

---

## The Architecture

The complete pipeline looks like this:

```
You speak a command
        ↓
Google Speech Recognition hears it
        ↓
Ollama + Llama3 understands the meaning
        ↓
LangGraph manages the workflow
        ↓
LangChain selects the right tool
        ↓
Python executes on your OS
        ↓
Hexa speaks the result back
```

### Layer 1 — Voice Input

I used Google Speech Recognition with Indian English language settings for better accent support. The microphone captures your voice, processes it, and converts it to text.

```python
import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    audio = recognizer.listen(source, timeout=8)
    text = recognizer.recognize_google(audio, language='en-IN')
```

### Layer 2 — AI Brain (Ollama + LangGraph)

This is the most important part. I used Ollama to run Llama3 locally on the user's machine. No OpenAI API needed. No costs. No internet after setup.

LangGraph manages the stateful workflow — it handles multi-step commands like "open chrome and search for python tutorials."

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)
workflow.add_node('understand', understand_node)
workflow.add_node('execute', execute_node)
workflow.add_node('respond', respond_node)
```

### Layer 3 — Tool Execution

The AI never directly executes code. Instead it selects from a registry of safe, predefined functions.

```python
TOOLS = {
    'open_chrome': open_chrome,
    'open_vscode': open_vscode,
    'create_folder': create_folder,
    'shutdown_pc': shutdown_pc,
}
```

The AI decides which tool to call. Python executes it. This is the foundation of safe AI agent architecture.

### Layer 4 — Memory System

I used ChromaDB to give Hexa persistent memory. It remembers your commands, preferences, and workflows.

```python
command_history.add(
    documents=[command],
    metadatas=[{'result': result, 'time': timestamp}],
    ids=[f'cmd_{timestamp}']
)
```

---

## What Hexa Can Do

Here are some of the voice commands that work right now:

**Open any app:**

```
"open chrome"
"open spotify"
"open whatsapp"
"open discord"
"open vs code"
```

**Open any website:**

```
"open netflix"
"open instagram"
"open chatgpt"
"open gmail"
"open youtube"
```

**Search:**

```
"search python tutorials on google"
"search lofi music on youtube"
```

**Send WhatsApp message:**

```
"send whatsapp message to John hello how are you"
"message mom I am coming home"
```

**System info:**

```
"what time is it"
"check my battery"
"check RAM usage"
"what is my IP address"
```

**System control:**

```
"take a screenshot"
"increase volume"
"lock screen"
"show desktop"
```

---

## The Tech Stack

| Component       | Technology                |
| --------------- | ------------------------- |
| Language        | Python 3.12               |
| Voice STT       | Google Speech Recognition |
| AI Model        | Ollama + Llama3.2         |
| Agent Framework | LangChain + LangGraph     |
| Memory          | ChromaDB                  |
| GUI             | CustomTkinter             |
| TTS             | pyttsx3                   |
| Automation      | pyautogui                 |
| Auth            | bcrypt                    |
| Packaging       | PyPI                      |

---

## The GUI Dashboard

I built a dark mode GUI dashboard using CustomTkinter that shows:

- Live microphone status (green when active)
- Command history with color-coded logs
  - Green = successful commands
  - Red = errors
  - Blue = info messages
  - White = your voice input
- Real-time CPU, RAM, Disk, Battery stats
- Quick command buttons
- Command counter
- Type commands directly without voice

---

## The Hardest Parts

### 1. Voice Recognition Accuracy

Getting Whisper to accurately transcribe Indian English accents was the biggest challenge. I switched from Whisper to Google Speech Recognition with `language='en-IN'` which improved accuracy significantly.

### 2. LLM Tool Calling

Small models like Llama3.2:1b sometimes return malformed JSON. I built a robust JSON extraction function that handles edge cases:

```python
def extract_json(text):
    text = text.strip()
    while text.endswith('}}'):
        text = text[:-1]
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return json.loads(text[start:end+1])
```

### 3. Cross-Platform Compatibility

Making the same code work on Windows, Linux, and Mac required careful handling of file paths, app launching commands, and system-specific behaviors.

### 4. RAM Limitations

The full Llama3 model needs 4.6GB RAM. On laptops with limited RAM this fails. I switched to `llama3.2:1b` which needs only 1GB and works much better on consumer hardware.

---

## Security

Since Hexa controls your operating system, security is critical.

- Passwords are hashed using bcrypt — never stored in plain text
- Dangerous commands (shutdown, lock screen) require voice confirmation
- Blocked commands (format disk) are completely prevented
- All actions are logged to a security audit file
- The AI never executes arbitrary code — only predefined safe functions

---

## How to Install

```bash
# Install Python 3.12 from python.org

# Install Hexa
pip install hexa-agent

# Install Ollama from ollama.com
# Then download the AI model
ollama pull llama3.2:1b

# Setup Hexa
hexa-agent setup

# Start Hexa
hexa-agent start

# Or launch the GUI dashboard
hexa-agent dashboard
```

---

## What I Learned

Building Hexa taught me more about real AI engineering than any course or tutorial ever could.

**1. AI agents are about orchestration, not models.**
The intelligence of Hexa comes from how the components are connected — not from the model itself. LangGraph, tool registries, memory systems — these are what make it smart.

**2. Local AI is the future.**
Running Llama3 locally means zero API costs, complete privacy, and offline functionality. For desktop assistants, local models are superior to cloud APIs.

**3. Voice recognition is harder than it looks.**
Accents, background noise, microphone quality — all of these affect accuracy. Choosing the right STT library and settings matters enormously.

**4. Real products need packaging.**
Writing code is only half the work. Making it installable, documentable, and maintainable is the other half. Publishing to PyPI taught me how real Python packages work.

**5. Build incrementally.**
I built Hexa in 18 phases — one at a time, one working goal per phase. This approach prevented overwhelm and kept me making consistent progress.

---

## What's Next

I am planning to add:

- Hindi and Marathi language support
- Plugin system for Spotify, Gmail, Calendar
- MCP integration for advanced tool communication
- Computer vision for visual screen understanding
- Mobile companion app for remote control
- Auto updater for seamless version management

---

## Try It Now

```bash
pip install hexa-agent
```

PyPI: https://pypi.org/project/hexa-agent

---

## Final Thoughts

Hexa started as a personal project to learn AI systems engineering. It became a real product that anyone can install and use.

If you are an AI/ML engineer who only knows model training and notebooks — I strongly recommend building an AI agent project like this. It will teach you skills that no amount of theoretical study can replace.

The future of AI is not just training better models. It is building better systems around those models.

---

*Built with Python, Ollama, LangChain, LangGraph, and a lot of debugging.*

*Hardik Yerne — AI/ML Engineer*

---

**Tags:** Python, AI, Machine Learning, Voice Assistant, LangChain, LangGraph, Ollama, Desktop Automation, Open Source
