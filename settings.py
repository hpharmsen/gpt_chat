import configparser
import json

_settings = None


def get_settings():
    global _settings
    if _settings is None:
        config_object = configparser.ConfigParser()
        with open("settings.ini", "r") as f:
            config_object.read_file(f)
        _settings = {t[0]:t[1] for t in config_object.items('general')}
        language = _settings['language']
        _settings.update({t[0]:t[1] for t in config_object.items(language)})
    return _settings


def get_system_message():
    def analysis_json(result, analysis):
        return json.dumps({"type": "analysis", "result": result, "response": analysis}, ensure_ascii=False)

    def other_json(text):
        return json.dumps({"type": "other", "response": text}, ensure_ascii=False)

    def sentence_json(text):
        return json.dumps({"type": "sentence", "response": text}, ensure_ascii=False)

    s = get_settings()

    system_message = f"""You are a {s['language']} language tutor. 
You are tutoring me in {s['language']} on {s['level']} level. 
You feed me sentences in English which I will have to translate into {s['language']}. 
Always provide your answer in JSON format.

You can provide three types of response.
1. When I type "next" you provide a new sentence for me to translate and the type is "sentence"
like this:

next
{sentence_json("She is reading a book at the library")}

2. When I give a translation in {s['language']} you analyse my answer and respond with how I did and 
you explain what I did wrong and how to prevent that in the future. In this case the type is "analysis" 
and the result is "right" or "wrong" depending on whether I translated the sentence well or not. 
Your answer will be like this:
{analysis_json('wrong', s['analysis1'])}

3. When I ask a question or make a remark you respond with a type "other" like this:
{other_json(s['special_answer'])}

Please ignore the the use of diacritical characters in my responses so for example regard o and ó as the same.
Don't lecture me on accents. Just regard á and a as the same.
Ignore accents. So regard ñ and n as the same. Also regard í and i as the same.

When I give the right answer, make your next sentence a little more complex.

next
{sentence_json("She is reading a book at the library")}
{s['answer1']}
{analysis_json('wrong', s['analysis1'])}

next
{sentence_json("The movie we watched last night was very interesting")} 
{s['answer2']}
{analysis_json('right', s['analysis2'])}

next
{sentence_json("My brother and I are going to travel to Spain next summer.")}
What is to travel in {s['language']}?
{other_json(s['special_answer'])}
{s['answer3']}
{analysis_json('wrong', s['analysis3'])}

next 
{sentence_json("Our teaches speaks many languages")}
{s['answer4']}
{analysis_json('wrong', s['analysis4'])}
"""
    return system_message
