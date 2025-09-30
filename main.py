import ollama
import os

# ANSI Colors
CYAN = '\033[96m'
ORANGE = '\033[93m'
RESET = '\033[0m'

loading_animation =  ["–", "/", "|", "\\"]

# Essential Functions
def clear_terminal():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')
clear_terminal()

def logo(color=CYAN):
    print(f"""{color}
 _            _                 ___  _____ 
| |          | |               / _ \\|_   _|
| | ___   ___| |__   __ _ _ __/ /_\\ \\ | |  
| |/ _ \\ / __| '_ \\ / _` | '__|  _  | | |  
| | (_) | (__| | | | (_| | |  | | | |_| |_ 
|_|\\___/ \\___|_| |_|\\__,_|_|  \\_| |_/\\___/ 
                                           
{RESET}""")

# Variables
logo()
current_response = ""
messages = [
    {
        "role": "system",
        "content": input(f"{CYAN}Please describe Qwen's personality: \n{RESET}")
    }
]


def color(color):
    print(color, end="")

def para(count=1):
    for i in range(count):
        print()

# Functions

def _chat_ollama(ollama_prompt, ollama_model):
    global current_response, messages
    
    messages.append({
        'role': "user",
        'content': ollama_prompt,
    })

    response = ollama.chat(
        model=ollama_model,
        messages=messages,
    )

    current_response = response['message']['content']

    messages.append({
        'role': 'assistant',
        'content': current_response,
    })

clear_terminal()
logo()
while True:
    color(RESET)
    _chat_ollama(input("> "), "qwen2.5-coder:7b")
    para()
    color(CYAN)
    print(current_response)
    para()
