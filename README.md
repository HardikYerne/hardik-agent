
---
## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12 |
| Voice STT | Google Speech Recognition |
| AI Model | Ollama + Llama3.2 |
| Agent Framework | LangChain + LangGraph |
| Memory | ChromaDB |
| GUI | CustomTkinter |
| TTS | pyttsx3 |
| GUI Automation | pyautogui |
| Authentication | bcrypt |
| CLI | Typer |
| System Tray | pystray |
| Packaging | PyPI |
---
## Security

- Encrypted password storage using bcrypt
- Local profile stored at ~/.hexa-agent/
- Dangerous commands require voice confirmation
- Action logging at ~/.hexa-agent/security.log
- No arbitrary code execution
- All AI runs locally on your machine
- No data sent to external servers

---

## Privacy

- 100% offline after setup
- No cloud dependency
- No API keys required
- No monthly costs
- Your voice commands never leave your computer
- All data stored locally

---

## Uninstall

### Using built-in command:

```bash
hexa-agent uninstall
```

### Manual uninstall:

Windows:

```powershell
pip uninstall hexa-agent -y
Remove-Item -Recurse -Force "$env:USERPROFILE\.hexa-agent"
Remove-Item -Force "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\HexaAgent.bat"
ollama rm llama3.2:1b
```

Linux/Mac:

```bash
pip uninstall hexa-agent -y
rm -rf ~/.hexa-agent
ollama rm llama3.2:1b
```

---

## Troubleshooting

### PyAudio installation fails on Windows

```powershell
pip install pipwin
pipwin install pyaudio
```

### Ollama not found after install

Close and reopen terminal, then try again.

### FFmpeg not found

```powershell
winget install ffmpeg
```

Close and reopen terminal.

### Not enough RAM for AI model

Use smaller model:

```bash
ollama pull llama3.2:1b
```

### Voice not recognized properly

- Speak slowly and clearly
- Reduce background noise
- Move closer to microphone
- Use complete sentences

### Agent opens Edge instead of Chrome

Set Chrome as default browser in Windows Settings.

---

## Version History

| Version | Changes                                      |
| ------- | -------------------------------------------- |
| 1.0.2   | Added uninstall command                      |
| 1.0.1   | Lighter package, optional heavy dependencies |
| 1.0.0   | Initial release                              |

---

## Author

Hardik Yerne

---

## License

MIT License - Free to use, modify and distribute.

---

## Links

- PyPI: https://pypi.org/project/hexa-agent
- GitHub: https://github.com/hardik/hexa-agent

---

*Hexa - Your AI Desktop Assistant*
'@

[System.IO.File]::WriteAllText((Resolve-Path "README.md").Path, $readme, (New-Object System.Text.UTF8Encoding $false))
