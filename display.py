""" Just some color coded output to the terminal """
import rich

ASSISTANT_COLOR = '#99ccff'
SYSTEM_COLOR = '#ffa500'
USER_COLOR = '#ffffff'
ERROR_COLOR = '#ff0000'


def color_print(message, color, end='\n'):
    rich.get_console().print(message, style=color, end=end)


def print_message(message):
    colors = {'assistant': ASSISTANT_COLOR, 'system': SYSTEM_COLOR, 'user': USER_COLOR}
    color = colors[message['role']]
    end = '\n' if message['role'] == 'user' else '\n\n'
    color_print(message['content'], color=color, end=end)
