""" The main chat program to chat with the model"""
import sys

from commands import CommandHandler
from gpt import GPT
from repl import Repl

if __name__ == "__main__":
    gpt = GPT()
    if len(sys.argv) > 1:
        gpt.load(sys.argv[1])

    # Add a command handler that handles special commands like model parameters and system settings
    command_handler = CommandHandler(gpt)

    # Start the interactive prompt
    repl = Repl(gpt, command_handler.handle_command)
    repl.show_token_count = True
    repl.run()
