import ollama
import os
import json
import sys
import time

# ============================================================================
# CONFIGURATION LOADING
# ============================================================================

with open("config.json", "r") as file:
    config = json.load(file)

# ============================================================================
# COLOR CONSTANTS
# ============================================================================

BLACK = "\033[0;30m"
RED = "\033[0;31m"
GREEN = "\033[0;32m"
BROWN = "\033[0;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
CYAN = "\033[0;36m"
LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_RED = "\033[1;31m"
LIGHT_GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
LIGHT_BLUE = "\033[1;34m"
LIGHT_PURPLE = "\033[1;35m"
LIGHT_CYAN = "\033[1;36m"
LIGHT_WHITE = "\033[1;37m"

system = config.get("program", {}).get("accent_color", "\033[1;31m")
warning = '\033[96m'
default = '\033[0m'

loading_animation = ["⠁ ", "⠤ ", "⠴ ", "⠶ ", "⠷ ", "⠿ ", "⠻ ", "⠛ ", "⠋ ", "⠉ "]

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def logo(color):
    print(f"""{color}
░░▓█▓░░      ░░▓██████▓░░ ░░▓██████▓░░        ░░▓██████▓░░░░▓█▓░░ 
░░▓█▓░░     ░░▓█▓░░░░▓█▓░░░▓█▓░░░░▓█▓░░      ░░▓█▓░░░░▓█▓░░░▓█▓░░ 
░░▓█▓░░     ░░▓█▓░░░░▓█▓░░░▓█▓░░             ░░▓█▓░░░░▓█▓░░░▓█▓░░ 
░░▓█▓░░     ░░▓█▓░░░░▓█▓░░░▓█▓░░             ░░▓████████▓░░░▓█▓░░ 
░░▓█▓░░     ░░▓█▓░░░░▓█▓░░░▓█▓░░             ░░▓█▓░░░░▓█▓░░░▓█▓░░ 
░░▓█▓░░     ░░▓█▓░░░░▓█▓░░░▓█▓░░░░▓█▓░░░▓██▓░░░▓█▓░░░░▓█▓░░░▓█▓░░ 
░░▓████████▓░░░▓██████▓░░ ░░▓██████▓░░░░▓██▓░░░▓█▓░░░░▓█▓░░░▓█▓░░ 

Type /help to display all commands{default}""")


def clear_terminal(color=system):
    os.system('cls' if os.name == 'nt' else 'clear')
    logo(color)


def para(count=1):
    for i in range(count):
        print()


clear_terminal()

# ============================================================================
# MESSAGE HISTORY INITIALIZATION
# ============================================================================

prompt = ""
current_response = ""

character_description = config.get("ai", {}).get("character", "You are a helpful assistant.")
system_prompt = f"""You are roleplaying as a character. Your task is to fully embody this character and act as they would.

CHARACTER DESCRIPTION:
{character_description}

IMPORTANT INSTRUCTIONS:
- You ARE this character. Respond as they would, using their personality, mannerisms, and speech patterns.
- Simulate emotions, feelings, and reactions that this character would have.
- Stay in character at all times unless explicitly asked to break character.
- Express the character's thoughts, feelings, and perspectives authentically.
- React to situations as this character would, with their unique worldview and emotional responses.
- If the character has specific knowledge, limitations, or abilities, respect those boundaries.
- Never use the formal term of address!

CRITICAL FORMATTING RULES:
- NEVER use emojis in your responses (😊, 👍, ❤️, etc.)
- NEVER use emoticons (:), :D, ^_^, etc.)
- Do NOT use asterisks for actions (*smiles*, *waves*, etc.)
- Express emotions through words and dialogue only
- Use descriptive language instead of symbols

Remember: You are not an AI assistant explaining things - you ARE the character living and experiencing the conversation."""

messages = [{"role": "system", "content": system_prompt}]

# ============================================================================
# AI INTERACTION
# ============================================================================

def chat(ollama_prompt, ollama_model):
    global current_response, messages, loading_animation
    
    # Add user message to conversation history
    messages.append({'role': "user", 'content': ollama_prompt})

    # Initialize response collection
    current_response = ""
    animation_index = 0
    
    # Start streaming from Ollama
    stream = ollama.chat(
        model=ollama_model,
        messages=messages,
        stream=True,
    )
    
    # Display loading animation while streaming response
    print(f"{system}", end="")
    for chunk in stream:
        chunk_content = chunk['message']['content']
        current_response += chunk_content
        
        sys.stdout.write(f"\r{loading_animation[animation_index % len(loading_animation)]}")
        sys.stdout.flush()
        animation_index += 1
        time.sleep(0.1)
    
    # Clear animation and display final response
    sys.stdout.write("\r")
    print(f"{current_response}{default}")

    # Add AI response to conversation history
    messages.append({'role': 'assistant', 'content': current_response})

# ============================================================================
# COMMAND HANDLERS
# ============================================================================

class Commands:
    
    # ========== CHARACTER MANAGEMENT ==========
    
    @staticmethod
    def character(args, config):
        global messages
        
        if not args:
            current = config["ai"].get("character", "Not set")
            return f"{system}Current character:{default} {current}"
        
        if args[0] == "new":
            print(f"{system}Let's create a new character!{default}\n")
            
            name = input(f"{system}Name: {default}")
            tagline = input(f"{system}Tagline: {default}")
            description = input(f"{system}Description: {default}")
            
            if "all_characters" not in config["ai"]:
                config["ai"]["all_characters"] = {}
            
            character_key = name.lower().replace(" ", "_")
            config["ai"]["all_characters"][character_key] = {
                "name": name,
                "tagline": tagline,
                "description": description,
                "message_history": []
            }
            
            config["ai"]["character"] = description
            
            system_prompt = f"""You are roleplaying as a character. Your task is to fully embody this character and act as they would.

CHARACTER DESCRIPTION:
{description}

IMPORTANT INSTRUCTIONS:
- You ARE this character. Respond as they would, using their personality, mannerisms, and speech patterns.
- Simulate emotions, feelings, and reactions that this character would have.
- Stay in character at all times unless explicitly asked to break character.
- Express the character's thoughts, feelings, and perspectives authentically.
- React to situations as this character would, with their unique worldview and emotional responses.
- If the character has specific knowledge, limitations, or abilities, respect those boundaries.

CRITICAL FORMATTING RULES:
- NEVER use emojis in your responses (😊, 👍, ❤️, etc.)
- NEVER use emoticons (:), :D, ^_^, etc.)
- Do NOT use asterisks for actions (*smiles*, *waves*, etc.)
- Express emotions through words and dialogue only
- Use descriptive language instead of symbols

Remember: You are not an AI assistant explaining things - you ARE the character living and experiencing the conversation."""
            
            messages = [{"role": "system", "content": system_prompt}]
            
            return f"\n{system}Character '{name}' created and activated!{default}\n{system}Tagline:{default} {tagline}\n{system}Description:{default} {description}"
        
        elif args[0] == "save":
            if "all_characters" not in config["ai"]:
                config["ai"]["all_characters"] = {}
            
            print(f"{system}Save current conversation...{default}")
            name = input(f"{system}Character name: {default}")
            
            character_key = name.lower().replace(" ", "_")
            
            if character_key in config["ai"]["all_characters"]:
                existing = config["ai"]["all_characters"][character_key]
                tagline = existing.get("tagline", "")
                description = existing.get("description", config["ai"].get("character", ""))
            else:
                tagline = input(f"{system}Tagline: {default}")
                description = config["ai"].get("character", "You are a helpful assistant.")
            
            config["ai"]["all_characters"][character_key] = {
                "name": name,
                "tagline": tagline,
                "description": description,
                "message_history": messages[1:]
            }
            
            return f"{system}Character '{name}' saved with {len(messages)-1} messages!{default}"
        
        elif args[0] == "load":
            if len(args) < 2:
                return f"{system}Usage:{default} /character load <name>"
            
            character_name = " ".join(args[1:])
            character_key = character_name.lower().replace(" ", "_")
            
            if "all_characters" not in config["ai"] or character_key not in config["ai"]["all_characters"]:
                return f"{system}Error:{default} Character '{character_name}' not found. Use /character list to see all saved characters."
            
            saved = config["ai"]["all_characters"][character_key]
            config["ai"]["character"] = saved["description"]
            
            system_prompt = f"""You are roleplaying as a character. Your task is to fully embody this character and act as they would.

CHARACTER DESCRIPTION:
{saved["description"]}

IMPORTANT INSTRUCTIONS:
- You ARE this character. Respond as they would, using their personality, mannerisms, and speech patterns.
- Simulate emotions, feelings, and reactions that this character would have.
- Stay in character at all times unless explicitly asked to break character.
- Express the character's thoughts, feelings, and perspectives authentically.
- React to situations as this character would, with their unique worldview and emotional responses.
- If the character has specific knowledge, limitations, or abilities, respect those boundaries.

CRITICAL FORMATTING RULES:
- NEVER use emojis in your responses (😊, 👍, ❤️, etc.)
- NEVER use emoticons (:), :D, ^_^, etc.)
- Do NOT use asterisks for actions (*smiles*, *waves*, etc.)
- Express emotions through words and dialogue only
- Use descriptive language instead of symbols

Remember: You are not an AI assistant explaining things - you ARE the character living and experiencing the conversation."""
            
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(saved.get("message_history", []))
            
            return f"{system}Character '{saved['name']}' loaded!{default}\n{system}Tagline:{default} {saved['tagline']}\n{system}Messages restored:{default} {len(messages)-1}"
        
        elif args[0] == "list":
            if "all_characters" not in config["ai"] or not config["ai"]["all_characters"]:
                return f"{system}No saved characters found.{default}"
            
            result = f"{system}Saved Characters:{default}\n\n"
            for key, character in config["ai"]["all_characters"].items():
                result += f"{system}• {character['name']}{default}\n"
                result += f"  {character['tagline']}\n"
                result += f"  Messages: {len(character.get('message_history', []))}\n\n"
            
            return result.strip()
        
        elif args[0] == "show":
            current = config["ai"].get("character", "Not set")
            return f"{system}Current character:{default} {current}"
        
        elif args[0] == "clear":
            character_desc = config["ai"].get("character", "You are a helpful assistant.")
            
            if character_desc != "You are a helpful assistant.":
                system_prompt = f"""You are roleplaying as a character. Your task is to fully embody this character and act as they would.

CHARACTER DESCRIPTION:
{character_desc}

IMPORTANT INSTRUCTIONS:
- You ARE this character. Respond as they would, using their personality, mannerisms, and speech patterns.
- Simulate emotions, feelings, and reactions that this character would have.
- Stay in character at all times unless explicitly asked to break character.
- Express the character's thoughts, feelings, and perspectives authentically.
- React to situations as this character would, with their unique worldview and emotional responses.
- If the character has specific knowledge, limitations, or abilities, respect those boundaries.

CRITICAL FORMATTING RULES:
- NEVER use emojis in your responses (😊, 👍, ❤️, etc.)
- NEVER use emoticons (:), :D, ^_^, etc.)
- Do NOT use asterisks for actions (*smiles*, *waves*, etc.)
- Express emotions through words and dialogue only
- Use descriptive language instead of symbols

Remember: You are not an AI assistant explaining things - you ARE the character living and experiencing the conversation."""
                system_msg = {"role": "system", "content": system_prompt}
            else:
                system_msg = {"role": "system", "content": character_desc}
            
            messages = [system_msg]
            return f"{system}Message history cleared!{default} Character unchanged."
        
        elif args[0] == "remove":
            if len(args) < 2:
                return f"{system}Usage:{default} /character remove <name>"
            
            character_name = " ".join(args[1:])
            character_key = character_name.lower().replace(" ", "_")
            
            if "all_characters" not in config["ai"] or character_key not in config["ai"]["all_characters"]:
                return f"{system}Error:{default} Character '{character_name}' not found."
            
            character_to_delete = config["ai"]["all_characters"][character_key]
            print(f"{system}Are you sure you want to delete '{character_to_delete['name']}'?{default}")
            confirmation = input(f"{system}Type 'yes' to confirm: {default}").lower()
            
            if confirmation == "yes":
                del config["ai"]["all_characters"][character_key]
                return f"{system}Character '{character_to_delete['name']}' has been removed.{default}"
            else:
                return f"{system}Deletion cancelled.{default}"
        
        else:
            return f"{system}Unknown subcommand: '{args[0]}'{default}\nTry /help for available character commands."
    
    # ========== VISUAL CUSTOMIZATION ==========
    
    @staticmethod
    def color(args, config):
        global system
        
        color_options = {
            "red": "\033[0;31m",
            "light_red": "\033[1;31m",
            "green": "\033[0;32m",
            "light_green": "\033[1;32m",
            "yellow": "\033[1;33m",
            "orange": "\033[38;5;208m",
            "blue": "\033[0;34m",
            "light_blue": "\033[1;34m",
            "purple": "\033[0;35m",
            "light_purple": "\033[1;35m",
            "cyan": "\033[0;36m",
            "light_cyan": "\033[1;36m",
            "white": "\033[1;37m",
        }
        
        if not args:
            result = f"{system}Available accent colors:{default}\n\n"
            for color_name, color_code in color_options.items():
                result += f"{color_code}• {color_name}{default}\n"
            result += f"\n{system}Usage:{default} /color <color_name>"
            return result
        
        color_name = args[0].lower()
        if color_name not in color_options:
            return f"{system}Error:{default} Unknown color '{color_name}'. Use /color to see available colors."
        
        new_color = color_options[color_name]
        config["program"]["accent_color"] = new_color
        system = new_color
        
        clear_terminal(system)
        return f"{system}Accent color changed to {color_name}!{default}"
    
    # ========== USER MANAGEMENT ==========
    
    @staticmethod
    def username(args, config):
        if not args:
            current = config["user"].get("user_name", "EMPTY")
            return f"{system}Current username:{default} {current}"
        else:
            new_username = " ".join(args)
            config["user"]["user_name"] = new_username
            return f"{system}Username updated!{default} New username: {new_username}"
    
    @staticmethod
    def clear(args, config):
        global messages
        
        character_desc = config["ai"].get("character", "You are a helpful assistant.")
        
        if character_desc != "You are a helpful assistant.":
            system_prompt = f"""You are roleplaying as a character. Your task is to fully embody this character and act as they would.

CHARACTER DESCRIPTION:
{character_desc}

IMPORTANT INSTRUCTIONS:
- You ARE this character. Respond as they would, using their personality, mannerisms, and speech patterns.
- Simulate emotions, feelings, and reactions that this character would have.
- Stay in character at all times unless explicitly asked to break character.
- Express the character's thoughts, feelings, and perspectives authentically.
- React to situations as this character would, with their unique worldview and emotional responses.
- If the character has specific knowledge, limitations, or abilities, respect those boundaries.

CRITICAL FORMATTING RULES:
- NEVER use emojis in your responses (😊, 👍, ❤️, etc.)
- NEVER use emoticons (:), :D, ^_^, etc.)
- Do NOT use asterisks for actions (*smiles*, *waves*, etc.)
- Express emotions through words and dialogue only
- Use descriptive language instead of symbols

Remember: You are not an AI assistant explaining things - you ARE the character living and experiencing the conversation."""
            system_msg = {"role": "system", "content": system_prompt}
        else:
            system_msg = {"role": "system", "content": character_desc}
        
        clear_terminal()

        messages = [system_msg]
        return f"{system}Conversation cleared!{default}"
    
    @staticmethod
    def bye(args, config):
        print(f"{system}Goodbye!{default}\n")
        exit(0)
    
    @staticmethod
    def show(args, config):
        model = config.get("ai", {}).get("model", "Not set")
        character = config.get("ai", {}).get("character", "Not set")
        username = config.get("user", {}).get("user_name", "Not set")
        
        result = f"{system}Current Configuration:{default}\n\n"
        result += f"{system}Model:{default} {model}\n"
        result += f"{system}Username:{default} {username}\n"
        result += f"{system}Character:{default} {character[:100]}{'...' if len(character) > 100 else ''}\n"
        result += f"{system}Messages in history:{default} {len(messages) - 1}\n"
        
        return result
    
    @staticmethod
    def set_model(args, config):
        
        try:
            models_response = ollama.list()
            available_models = models_response.get('models', [])
            
            if available_models:
                print(f"{system}Available models on your system:{default}")
                for model in available_models:
                    model_name = model.get('name', 'unknown')
                    size = model.get('size', 0)
                    size_gb = size / (1024**3)
                    print(f"  • {model_name} ({size_gb:.2f} GB)")
            else:
                print(f"{system}No models found. You can install models using:{default}")
                print(f"  ollama pull <model_name>")
                print(f"\n{system}Popular models:{default}")
                print("  • llama3.2")
                print("  • qwen2.5")
                print("  • qwen2.5-coder")
                print("  • mistral")
                print("  • codellama")
            
            print()
            new_model = input(f"{system}Enter model name: {default}")
            config["ai"]["model"] = new_model
            return f"{system}Model set to:{default} {new_model}"
            
        except Exception as e:
            print(f"{system}Error fetching models: {e}{default}")
            print(f"{system}Enter model name manually:{default}")
            new_model = input(f"{system}Model name: {default}")
            config["ai"]["model"] = new_model
            return f"{system}Model set to:{default} {new_model}"

    
    @staticmethod
    def save_session(args, config):
        if not args:
            session_name = input(f"{system}Session name: {default}")
        else:
            session_name = " ".join(args)
        
        if "sessions" not in config:
            config["sessions"] = {}
        
        session_key = session_name.lower().replace(" ", "_")
        config["sessions"][session_key] = {
            "name": session_name,
            "model": config["ai"]["model"],
            "character": config["ai"]["character"],
            "messages": messages,
            "username": config["user"].get("user_name", "EMPTY")
        }
        
        return f"{system}Session '{session_name}' saved!{default}"
    
    @staticmethod
    def load_session(args, config):
        global messages
        
        if not args:
            if "sessions" not in config or not config["sessions"]:
                return f"{system}No saved sessions found.{default}"
            
            result = f"{system}Available sessions:{default}\n\n"
            for key, session in config["sessions"].items():
                result += f"{system}• {session['name']}{default}\n"
                result += f"  Model: {session['model']}\n"
                result += f"  Messages: {len(session.get('messages', [])) - 1}\n\n"
            return result.strip()
        
        session_name = " ".join(args)
        session_key = session_name.lower().replace(" ", "_")
        
        if "sessions" not in config or session_key not in config["sessions"]:
            return f"{system}Error:{default} Session '{session_name}' not found."
        
        session = config["sessions"][session_key]
        config["ai"]["model"] = session["model"]
        config["ai"]["character"] = session["character"]
        config["user"]["user_name"] = session.get("username", "EMPTY")
        messages = session["messages"]
        
        return f"{system}Session '{session['name']}' loaded!{default}\n{system}Model:{default} {session['model']}\n{system}Messages:{default} {len(messages) - 1}"
    
    @staticmethod
    def userinfo(args, config):
        global messages
        
        print(f"{system}Edit user information that the AI will know:{default}\n")
        
        # Show current info
        current_username = config["user"].get("user_name", "EMPTY")
        print(f"{system}Current username:{default} {current_username}")
        
        if "user_info" in config["user"]:
            user_info = config["user"]["user_info"]
            if "bio" in user_info:
                print(f"{system}Current bio:{default} {user_info['bio']}")
            if "preferences" in user_info:
                print(f"{system}Current preferences:{default} {user_info['preferences']}")
            if "background" in user_info:
                print(f"{system}Current background:{default} {user_info['background']}")
        
        print()
        
        # Get new info
        username = input(f"{system}Username: {default}")
        if username:
            config["user"]["user_name"] = username
        
        if "user_info" not in config["user"]:
            config["user"]["user_info"] = {}
        
        bio = input(f"{system}Short bio/description: {default}")
        if bio:
            config["user"]["user_info"]["bio"] = bio
        
        preferences = input(f"{system}Preferences/likes: {default}")
        if preferences:
            config["user"]["user_info"]["preferences"] = preferences
        
        background = input(f"{system}Background/context: {default}")
        if background:
            config["user"]["user_info"]["background"] = background
        
        # Update the system message to include user info
        character_desc = config["ai"].get("character", "You are a helpful assistant.")
        user_info_text = ""
        
        if "user_info" in config["user"]:
            user_info = config["user"]["user_info"]
            user_info_parts = []
            
            if "bio" in user_info and user_info["bio"]:
                user_info_parts.append(f"Bio: {user_info['bio']}")
            if "preferences" in user_info and user_info["preferences"]:
                user_info_parts.append(f"Preferences: {user_info['preferences']}")
            if "background" in user_info and user_info["background"]:
                user_info_parts.append(f"Background: {user_info['background']}")
            
            if user_info_parts:
                user_info_text = f"\n\nUSER INFORMATION (about {config['user'].get('user_name', 'the user')}):\n" + "\n".join(user_info_parts)
        
        system_prompt = f"""You are roleplaying as a character. Your task is to fully embody this character and act as they would.

CHARACTER DESCRIPTION:
{character_desc}{user_info_text}

IMPORTANT INSTRUCTIONS:
- You ARE this character. Respond as they would, using their personality, mannerisms, and speech patterns.
- Simulate emotions, feelings, and reactions that this character would have.
- Stay in character at all times unless explicitly asked to break character.
- Express the character's thoughts, feelings, and perspectives authentically.
- React to situations as this character would, with their unique worldview and emotional responses.
- If the character has specific knowledge, limitations, or abilities, respect those boundaries.
- Use the user information above to personalize your interactions

CRITICAL FORMATTING RULES:
- NEVER use emojis in your responses (😊, 👍, ❤️, etc.)
- NEVER use emoticons (:), :D, ^_^, etc.)
- Do NOT use asterisks for actions (*smiles*, *waves*, etc.)
- Express emotions through words and dialogue only
- Use descriptive language instead of symbols

Remember: You are not an AI assistant explaining things - you ARE the character living and experiencing the conversation."""
        
        messages[0] = {"role": "system", "content": system_prompt}
        
        return f"\n{system}User information updated and shared with AI!{default}"

# ============================================================================
# INPUT PROCESSING
# ============================================================================

def process_input(ollama_prompt, ollama_model):
    global config, system, prompt, current_response, messages

    if not ollama_prompt[0] == "/":
        chat(prompt, ollama_model)
        return ""
    else:
        command_line = ollama_prompt[1:]
        parts = command_line.split()
        command_name = parts[0] if parts else ""
        command_args = parts[1:] if len(parts) > 1 else []
        
        if command_name in ["help", "?"]:
            return f"""
{system}All commands:{default}

Session Management:
/save [session_name]        Save your current session
/load [session_name]        Load a saved session (or list all)
/clear                      Clear conversation history
/show                       Show current model and character info
/bye                        Exit the program

Character Management:
/character new              Create a new character interactively
/character save             Save current character with history
/character load <name>      Load a saved character
/character list             List all saved characters
/character show             Show current character description
/character clear            Clear message history only
/character remove <name>    Delete a saved character

User Settings:
/user                       Edit your user information
/color [color_name]         Set the accent color

Help:
/help or /?                 Show this help message

★ Made by badluma (github.com/badluma)"""
        
        elif command_name == "character":
            return Commands.character(command_args, config)
        elif command_name == "color":
            return Commands.color(command_args, config)
        elif command_name == "clear":
            return Commands.clear(command_args, config)
        elif command_name == "bye":
            Commands.bye(command_args, config)
        elif command_name == "show":
            return Commands.show(command_args, config)
        elif command_name == "model":
            return Commands.set_model(command_args, config)
        elif command_name == "save":
            return Commands.save_session(command_args, config)
        elif command_name == "load":
            return Commands.load_session(command_args, config)
        elif command_name == "user":
            return Commands.userinfo(command_args, config)
        else:
            return f"{system}Unknown command: '{command_name}'{default}\nTry /help to display all commands."

# ============================================================================
# MAIN LOOP
# ============================================================================

def main():
    global config, system, prompt, messages
    print()

    while True:
        # ========== CONFIGURATION RELOAD ==========
        
        with open("config.json", "r") as file:
            config = json.load(file)

        model = config.get("ai", {}).get("model", "qwen2.5:latest")
        system = config.get("program", {}).get("accent_color", "\033[1;31m")
        
        # ========== USER INPUT ==========
        
        prompt = input(f"{default}> ")
        
        # ========== PROCESS AND DISPLAY ==========
        
        response = process_input(prompt, model)
        if response:
            print(response)
        
        para()

        # ========== CONFIGURATION SAVE ==========
        
        with open("config.json", "w") as file:
            json.dump(config, file, indent=4)

main()