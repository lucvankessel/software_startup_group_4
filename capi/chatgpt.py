from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
  
my_api_key = os.getenv("OPENAI_KEY")

def get_chatgpt_result(selected_text):
    client = OpenAI(
        api_key=my_api_key,
    )

    messages = [ 
        {
          "role": "system",
          "content": """
            You are a political analysis tool designed to output what political leaning a text has and return that as a JSON object.
            Do this based on how the Dutch perceive these political sides to be.
            Do not only look at the subject but also how the author writes about the subject.
            this return is one object you return like: 
            {
                "result": {political leaning}, 
                "number": {number} 
                "reason": "{reason why you decided to give the given text this value}",
                "keywords": [{keywords}]
            }
            The field "number" should represent the political leaning as a integer. -100 is the most left leaning, 100 is the most right leaning, 0 is center.
            "keywords": field is an array of keywords of the text that is given.
            """
        },
        {
          "role": "user",
          "content": selected_text
        }
    ]
    
    chat = client.chat.completions.create( 
            model="gpt-3.5-turbo-1106", 
            messages=messages, 
            response_format={"type": "json_object"},
        )

    return chat.choices[0].message.content

def translate_chatgpt(text):
    client = OpenAI(
        api_key=my_api_key,
    )

    messages = [
        {
            "role": "system",
            "content": """"
                You are a translation tool designed to translate any given text to english.
                The output of the given text is to be returned as JSON.
                The json should be returned as following:
                {
                    "result": {result}
                }
                where the {result} should be the translation result.
            """
        },
        {
            "role": "user",
            "content": text
        }
    ]

    chat = client.chat.completions.create( 
            model="gpt-3.5-turbo-1106", 
            messages=messages, 
            response_format={"type": "json_object"},
        )
    
    return chat.choices[0].message.content
