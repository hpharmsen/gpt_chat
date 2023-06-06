""" The main program for the spanish tutor """
import json
import sys

from display import SYSTEM_COLOR, color_print
from gpt import GPT
from repl import Repl
from settings import get_settings, get_system_message

STATUS_NEXT_QUESTION = 1
STATUS_ANSWER = 2


class Tutor(GPT):
    def __init__(self):
        super().__init__()
        self.system = get_system_message()
        self.hard_concepts = []
        self.message_memory = 4
        self.last_question = ''
        self.status = STATUS_NEXT_QUESTION

    def chat(self, prompt, add_to_messages=True):
        # Modify prompt here...
        # Check if there's a concept that went wrong last time. If so, include it in the prompt.

        result = super().chat(prompt, add_to_messages=add_to_messages)

        # Modify result here...
        reply = json.loads(result['content'])

        # this is the python switch statement:
        match reply['type']:
            case 'sentence':
                self.status = STATUS_ANSWER
                self.last_question = reply['response']
            case 'other':
                self.status = STATUS_ANSWER
            case 'analysis':
                if reply['result'] == 'wrong':
                    hard_concept = {'question': self.last_question, 'answer': prompt, 'analysis': reply['response']}
                    self.hard_concepts.append(hard_concept)
                self.status = STATUS_NEXT_QUESTION
        modified_result = result.copy()
        modified_result['content'] = reply['response']
        return modified_result

    def get_prompt(self):
        if self.status == STATUS_NEXT_QUESTION:
            # Auto advance to the next prompt
            if len(self.hard_concepts) > 2:
                hard_concept = self.hard_concepts.pop(0)
                prompt = f"""You previously asked "{hard_concept['question']}" and I answered "{hard_concept['answer']}"
                Your analysis was: "{hard_concept['analysis']}"

                Generate a new sentence that includes one or more of the concepts I got wrong"""
            else:
                prompt = "Generate a new sentence"
        else:
            # Ask the user for a prompt
            s = get_settings()
            prompt = ''
            while not prompt:
                prompt = input(f"{s['language']}: ")
        return prompt


if __name__ == "__main__":
    s = get_settings()
    color_print(f"Hello, I am your {s['language']} tutor on {s['level']} level. I will help you learn {s['language']}.\n" +
                f"I will give you sentences in English and you will have to translate them into {s['language']}.\n" +
                "Here's your first sentence:\n", color=SYSTEM_COLOR)
    gpt = Tutor()
    gpt.model = s['model']

    # Load session if passed as a command line argument
    if len(sys.argv) > 1:
        gpt.load(sys.argv[1])

    # Start the interactive prompt
    repl = Repl(gpt)
    repl.get_prompt = gpt.get_prompt # partial(gpt.get_prompt, repl=repl)
    repl.run()
