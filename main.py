import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Takes in the open_ai response object
def clean_response(open_ai_response):
    cleaned_response = open_ai_response
    if '\n\n' in cleaned_response:
        cleaned_response = cleaned_response.split('\n\n')[1]
    return cleaned_response


def generate_response(open_ai_prompt):
    open_ai_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=open_ai_prompt,
        max_tokens=60,
        temperature=0.8,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
    # total_token_usage = open_ai_response['usage']['total_tokens']
    return open_ai_response['choices'][0]['text']


def call_horror_generator(noun):
    return generate_response(
        "Topic: Breakfast\nTwo-Sentence Horror Story: He always stops crying when I pour the milk on "
        "his cereal. I just have to remember not to let him see his face on the carton.\n    \nTopic: "
        f"{noun}\nTwo-Sentence Horror Story:""")


while True:
    prompt = input("Enter a noun to create a horror story. Or press enter to exit: ")
    leading_question = 'Here is a list of example nouns [Mcdonalds, Tom, Cat]. Please only respond in Yes or No, ' \
                       'is the following word a noun: '
    if prompt == "":
        break
    print("Loading...")
    noun_confirmation = clean_response(generate_response(leading_question + prompt))
    if noun_confirmation == 'Yes':
        response = call_horror_generator(prompt)
    else:
        response = 'Error, you have not entered a noun. Please try again.\n'
    print(response)
