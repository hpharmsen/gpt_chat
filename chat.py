""" The main chat program to chat with the model"""
import sys

from gpt import GPT
from repl import Repl

if __name__ == "__main__":
    gpt = GPT()
    if len(sys.argv) > 1:
        gpt.load(sys.argv[1])
    repl = Repl(gpt)
    repl.show_token_count = True
    repl.run()
