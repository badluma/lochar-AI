# LocharAI

A powerful command-line chat interface for Ollama with character roleplay, customizable personalities, and persistent conversation memory.

## Features

- Beautiful ASCII art logo with customizable colors
- Interactive chat with any Ollama model
- Character roleplay system with personality profiles
- Persistent conversation memory across sessions
- Save and load multiple characters with conversation history
- Customizable terminal color themes
- User profile system for personalized AI interactions
- Session management for switching between different conversations
- Streaming responses with animated loading indicator

## Prerequisites

Before running this application, make sure you have:

1. **Python 3.7+** installed on your system
2. **Ollama** installed and running on your machine
   - Install from: https://ollama.ai/
   - Make sure the Ollama service is running
3. **At least one Ollama model** downloaded
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

3. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

4. **Activate the virtual environment:**
   
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   venv\Scripts\activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Make sure Ollama is running:**
   ```bash
   ollama serve
   ```

2. **Run the application:**
   ```bash
   python main.py
   ```

3. **Start chatting:**
   - Type your messages and press Enter
   - Use `/help` to see all available commands
   - Create characters with `/character new`
   - Customize colors with `/color`

## Commands

### Session Management
- `/save [name]` - Save your current session
- `/load [name]` - Load a saved session (or list all)
- `/clear` - Clear conversation history
- `/show` - Show current configuration
- `/model` - Set your prefered model
- `/bye` - Exit the program

### Character Management
- `/character new` - Create a new character interactively
- `/character save` - Save current character with history
- `/character load <name>` - Load a saved character
- `/character list` - List all saved characters
- `/character show` - Show current character description
- `/character clear` - Clear message history only
- `/character remove <name>` - Delete a saved character

### User Settings
- `/username [name]` - Set or show your username
- `/userinfo` - Edit information about yourself that the AI will know
- `/color [color_name]` - Set the accent color

### Help
- `/help` or `/?` - Show all commands

## Configuration

The `config.json` file stores all settings and data:

```json
{
    "ai": {
        "model": "qwen2.5-coder:7b",
        "character": "Character description...",
        "all_characters": {
            "character_name": {
                "name": "Character Name",
                "tagline": "Short description",
                "description": "Full character description",
                "message_history": []
            }
        }
    },
    "program": {
        "accent_color": "\\u001b[1;32m"
    },
    "user": {
        "user_name": "Your Name",
        "user_info": {
            "bio": "About you",
            "preferences": "Your preferences",
            "background": "Your background"
        }
    },
    "sessions": {
        "session_name": {
            "name": "Session Name",
            "model": "model_name",
            "character": "Character description",
            "messages": [],
            "username": "Your Name"
        }
    }
}
```

## Character System

LocharAI features a powerful character roleplay system:

1. **Create Characters** - Define personalities with name, tagline, and detailed description
2. **Save Conversations** - Characters remember entire conversation histories
3. **Switch Characters** - Load different characters with their unique personalities
4. **Persistent Memory** - All character data is saved in config.json

### Example Character Creation

```
>> /character new
Name: Sherlock Holmes
Tagline: The world's greatest detective
Description: Sherlock Holmes is a brilliant detective known for his exceptional 
observational skills, logical reasoning, and deductive abilities. He is often 
perceived as aloof and eccentric, with a sharp wit and little patience for those 
who cannot keep up with his rapid thinking.
```

## Color Customization

Available accent colors:
- red, light_red
- green, light_green
- blue, light_blue
- purple, light_purple
- cyan, light_cyan
- yellow, white

Change colors with: `/color <color_name>`

## User Information System

Use `/user` to tell the AI about yourself:
- Bio/description
- Preferences/likes
- Background/context

This information is automatically included in the character's system prompt, allowing for more personalized interactions.

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

This project is open source and available under the MIT License.

## Acknowledgments

- Built with Ollama for local AI inference
- Supports all Ollama models
- Inspired by the need for a powerful, customizable CLI chat interface

Made by badluma (and some help from Claude)