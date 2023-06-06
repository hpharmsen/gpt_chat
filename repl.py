""" Class to handle the interactivity to the model and setting model system parameters """
from display import color_print, ERROR_COLOR, SYSTEM_COLOR, print_message
from gpt import GPT


class Repl:
    def __init__(self, gpt: GPT):
        self.gpt = gpt
        self.show_token_count = False

    def handle_command(self, command: str):
        # Commands can be things like
        # :load filename
        # :save [filename]
        # :quite
        # :max_tokens=1000
        # :temperature=0.8
        if command.count('='):
            command, param = command.split('=', 1)
        elif command.count(' '):
            command, param = command.split(' ', 1)
        else:
            param = None

        match command:
            case ':quit' | ':exit':
                return False

            case ':load':
                filename = param
                if not filename:
                    color_print(f"Pass a filename\n", color=ERROR_COLOR)
                    return True
                self.gpt.load(filename)
                return True

            case ':input':
                filename = param
                if not filename:
                    color_print(f"Pass a filename\n", color=ERROR_COLOR)
                    return True
                self.gpt.file_input(filename)
                return True

            case ':save':
                filename = param or self.gpt.name
                self.gpt.save(filename)
                color_print(f"Saved to {(self.gpt.save_dir / filename).with_suffix('.txt')}\n", color=SYSTEM_COLOR)
                return True

            case ':reset':
                self.gpt.reset()
                color_print(f"Conversation reset\n", color=SYSTEM_COLOR)
                return True

            case ':bye':
                self.gpt.save()
                self.gpt.chat(command)
                return False

            case ':maxmessages':
                self.gpt.message_memory = int(param)

            case c if c in [':'+attr for attr in dir(self.gpt)]:
                attr = c[1:]
                if not param:
                    color_print(f"Invalid command: {command}\n", color=ERROR_COLOR)
                    return True
                try:
                    value = eval(param)
                except SyntaxError:
                    value = param  # Treat param as a string
                setattr(self.gpt, attr, value)
                color_print(f"{attr} set to {value}\n", color=SYSTEM_COLOR)
                return True

            case ':help' | '?':
                color = SYSTEM_COLOR
                color_print(":reset - resets the conversation", color=color)
                color_print(":load name - loads the saved conversation with the specified name", color=color)
                color_print(":save name - saves the conversation under the specified name", color=color)
                color_print(":input filename - loads an input from the specified file", color=color)
                color_print(":model gpt-4 - Sets the AI model", color=color)
                color_print(":max_tokens 800 - The maximum number of tokens to generate in the completion", color=color)
                color_print(":temperature 0.9 - What sampling temperature to use, between 0 and 2", color=color)
                color_print(":n 1 - Specifies the number answers given", color=color)
                color_print(':stop ["\\n", " Human:", " AI:"] - Up to 4 sequences where the API will stop ' +
                            'generating further tokens', color=color)
                color_print(":bye - quits but saves the conversation first", color=color)
                color_print(":quit - quits the program", color=color)
                color_print(":exit - quits the program", color=color)
                return True

            case _:
                color_print(f"Unknown command: {command}\n", color=ERROR_COLOR)
                return True

    def run(self, first_prompt=''):
        while True:
            if first_prompt:  # If we have a first prompt, use it instead of asking the user first
                prompt = first_prompt
                first_prompt = None
            else:
                prompt = self.get_prompt()
            if prompt[0] == ':':
                if not self.handle_command(prompt):
                    break
            else:
                response = self.gpt.chat(prompt)
                print_message(response)
                if self.show_token_count:
                    print(f"[{response['completion']['usage']['total_tokens']}]")

    def get_prompt(self):
        """ Default implementation, can be overridden """
        prompt = ''
        while not prompt:
            prompt = input("You: ")
        return prompt
