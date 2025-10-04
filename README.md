# locharAI

A powerful command-line chat interface for Ollama with character roleplay, customizable personalities, and persistent conversation memory.

## Features

- 🎨 Stylized ASCII art logo
- 💬 Interactive chat with Ollama models
- 🧠 Conversation memory (maintains context throughout the session)
- 🎭 Customizable AI personality
- 🌈 Colorful terminal interface
- ⚙️ Configuration file support

## Prerequisites

Before running this application, make sure you have:

1. **Python 3.7+** installed on your system
2. **Ollama** installed and running on your machine
   - Install from: https://ollama.ai/
   - Make sure the Ollama service is running
3. **qwen2.5-coder:7b** model (or modify the model in `main.py`)
   ```bash
   ollama pull qwen2.5-coder:7b
   # or
   ollama pull llama3.2
   # or any other model you prefer
   ```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/locharAI.git
   ```

2. **Navigate to the folder:**
   ```bash
   cd locharAI
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Make sure Ollama is running:**

   ```bash
   ollama serve
   ```

3. **Run the application:**

   ```bash
   python main.py
   ```

3. **Follow the prompts:**
   - First, you'll be asked to describe the AI's personality
   - Then you can start chatting with the AI
   - Type your messages and press Enter to send
   - The AI will respond with the personality you defined

## Configuration (not working yet)

The application uses a `config.json` file to store settings:

```json
{
    "default_model": "EMPTY",
    "accent_color": "CYAN", 
    "last_personality": "EMPTY"
}
```

You can modify this file to:
- Set a different default model
- Change the accent color
- Save your preferred AI personality

## Customization

### Changing the AI Model

To use a different Ollama model, edit line 74 in `main.py`:

```python
_chat_ollama(input("> "), "your-preferred-model")
```

### Changing Colors

The application uses ANSI color codes. You can modify the colors by changing the color constants at the top of `main.py`:

```python
CYAN = '\033[96m'
ORANGE = '\033[93m'
RESET = '\033[0m'
```

## Project Structure

```
locharAI/
├── main.py          # Main application file
├── config.json      # Configuration and data storage
├── requirements.txt # Python dependencies
├── README.md        # This file
├── .gitignore       # Git ignore rules
└── venv/            # Virtual environment (created after setup)
```

## Dependencies

- `ollama` - Python client for Ollama API
- `httpx` - HTTP client (ollama dependency)
- `pydantic` - Data validation (ollama dependency)

## Model Support

LocharAI supports ANY Ollama model. Popular options:
- qwen2.5, qwen2.5-coder
- llama3.2, llama2
- mistral, mixtral
- codellama
- phi, gemma
- deepseek-coder

Change models with `/model` to see all installed models.

## Troubleshooting

### "Connection refused" or similar network errors
- Make sure Ollama is running: `ollama serve`
- Check if the model is available: `ollama list`

### "Model not found" errors
- Pull the required model: `ollama pull <model_name>`
- Use `/model` to select from installed models

### Import errors
- Make sure you're in the virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

### Config.json errors
- Ensure config.json exists and has valid JSON syntax
- Check that all required keys are present (ai, program, user)
- Remove any duplicate keys like "personality" and "all_personalities" (use "character" and "all_characters")

### Characters not responding correctly
- Ensure the character description is detailed
- Use `/character show` to verify the current character
- Try clearing conversation with `/clear` and starting fresh

## Tips for Best Results

1. **Character Descriptions** - Be detailed when creating characters. Include personality traits, speaking style, knowledge areas, and quirks.

2. **User Information** - Use `/userinfo` to provide context about yourself. This helps characters interact more naturally.

3. **Model Selection** - Different models have different strengths. Experiment with `/set model` to find what works best.

4. **Save Sessions** - Use `/save` before switching contexts to preserve important conversations.

5. **Color Themes** - Choose colors that work well with your terminal theme for better readability.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with [Ollama](https://ollama.ai/) for local AI inference
- Uses the `qwen2.5-coder:7b` model by default