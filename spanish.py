""" The main program for the spanish tutor """
import sys

from display import SYSTEM_COLOR, color_print
from gpt import GPT
from repl import Repl

SPANISH_SYSTEM = """You are a Spanish language tutor. 
You are tutoring me in Spanish on A2 level. 
You feed me sentences in English which I will have to translate into Spanish. 
You start these sentences with Q:
After I type my response you analyse my answer and respond with how I did and you explain what I did wrong and 
how to prevent that in the future. 
If I translated the question correctly, start your answer with YES.
else start your answer with NO.

After each analysis you give me a new sentence to translate.

Please ignore the the use of diacritical characters in my responses so for example regard o and ó as the same.
Don't lecture me on accents. Just regard á and a as the same.
Ignore accents. So regard ñ and n as the same.

When I give the right answer, make your next sentence a little more complex.
When I give a wrong answer, make your next sentence a little less complex.
When I do not translate the sentence but give a remark or some question, do not start your response with A: . 
Just give me an answer.

Regard the concepts that I do wrong. Make sure you include those concepts in later sentences so 
I will have the possibility to practice them again.

Q: She is reading a book at the library
ella esta leyando un libro en la biblioteca
NO. Almost perfect! Just a small mistake in the verb: the correct translation is "Ella está leyendo un libro en la
biblioteca". Use "leyendo" instead of "leyando" for "reading". Keep practicing!

Q: The movie we watched last night was very interesting
La pelicula que vimos la noche pasada era muy interesante
YES. Great job! Your translation is correct: "La película que vimos la noche pasada era muy interesante". 

Q: Our teacher speaks many languages.
Nuestro profesor hable muchos lenguas
NO. Almost perfect! The correct translation is "Nuestro profesor habla muchos idiomas" or "Nuestro profesor habla muchas
lenguas". Here's what you need to remember:
1. Use "habla" instead of "hable" for "speaks". The verb "hablar" (to speak) in the present tense for the third person
singular (él, ella, usted) should be "habla".
2. Use "idiomas" or "muchas lenguas" instead of "muchos lenguas" for "many languages". Both "idiomas" and "lenguas" are
correct for "languages", but when using "lenguas", it should be accompanied by "muchas" instead of "muchos".
"""


class SpanishGPT(GPT):
    def __init__(self):
        super().__init__()
        self.system = SPANISH_SYSTEM
        self.hard_concepts = []
        self.message_memory = 4
        self.last_question = ''

    def chat(self, prompt, add_to_messages=True):
        # Modify prompt here...
        # Check if there's a concept that went wrong last time. If so, include it in the prompt.
        if len(self.hard_concepts) > 2:
            hard_concept = self.hard_concepts.pop(0)
            modified_prompt = f"""{prompt}
            
            You previously asked "{hard_concept['question']}" and I answered "{hard_concept['answer']}"
            You said: "{hard_concept['analysis']}"
            First analyze my translaton and then, in the next sentence you generate, 
            include one or more of the concepts I got wrong"""
        else:
            modified_prompt = prompt

        result = super().chat(modified_prompt, add_to_messages=add_to_messages)

        # Modify result here...
        reply = result['content']
        if reply.startswith('YES. '):
            reply = reply[5:]
        elif reply.startswith('NO. '):
            reply = reply[4:]
            analysis = reply.split('Q: ')[0] if reply.count('Q: ') else reply
            self.hard_concepts.append({'question': self.last_question, 'answer': prompt, 'analysis': analysis})
        if reply.count('Q: '):
            self.last_question = reply.split('Q: ')[1]
            reply = reply.replace('Q: ', '')
        modified_result = result.copy()
        modified_result['content'] = reply
        return modified_result


if __name__ == "__main__":
    color_print("Hello, I am your Spanish tutor. I will help you learn Spanish.\n" +
                "I will give you sentences in English and you will have to translate them into Spanish.\n" +
                "Here's your first sentence:\n", color=SYSTEM_COLOR)
    gpt = SpanishGPT()
    gpt.model = "gpt-3.5-turbo"  # of "gpt-4"

    # Load session if passed as a command line argument
    if len(sys.argv) > 1:
        gpt.load(sys.argv[1])

    # Start the interactive prompt
    repl = Repl(gpt)
    repl.run('Start with your first sentence')
