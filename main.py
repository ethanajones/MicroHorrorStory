import os
import textwrap
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


total_token_usage = 0


def generate_response(open_ai_prompt, temp=1):
    global total_token_usage
    open_ai_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=open_ai_prompt,
        max_tokens=60,
        temperature=temp,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
    total_token_usage += open_ai_response['usage']['total_tokens']
    return open_ai_response['choices'][0]['text']


def call_horror_generator(noun):
    return generate_response(
        "Topic: Breakfast\nTwo-Sentence Horror Story: He always stops crying when I pour the milk on "
        "his cereal. I just have to remember not to let him see his face on the carton.\n    \nTopic: "
        f"{noun}\nTwo-Sentence Horror Story:""")


while True:
    prompt = input("Enter an animal to create a horror story. Or press enter to exit:  ")
    leading_question = f'Please only respond with Yes or No, ' \
                       'is the following word an animal: '
    if prompt == "":
        print(f"You used {total_token_usage} tokens during this session.")
        break
    print("Checking animal...")
    animal_confirmation = clean_response(generate_response(leading_question + prompt, 0))
    if animal_confirmation == 'Yes':
        print(prompt, "Accepted. \nGenerating story...")
        response = call_horror_generator(prompt)
    else:
        response = 'Error, you have not entered an animal. Please try again.\n'
    print(response)
