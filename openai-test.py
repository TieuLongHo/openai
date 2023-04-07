import os
import openai
from termcolor import colored
import argparse
openai.api_key = os.getenv('OPENAI_API_KEY')

history = [
    {"role": "system", "content": "You are a helpful assistant."}
]


def generate_chat_response(user_input):
    history.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history
    )
    history.append(
        {"role": "system", "content": response.choices[0].message.content})
    return response


def generate_image_response(user_input):
    response = openai.Image.create(
        prompt=user_input,
        n=3,
        size="1024x1024"
    )

    return response


def chat(debug):
    while True:
        try:
            user_input = input('you: ')
            if user_input.lower() in ['quit', 'exit']:
                break
            response = generate_chat_response(user_input)
            print("gpt:", colored(
                response['choices'][0]['message']['content'], 'white', "on_dark_grey"))
            if debug:
                print_usage(response)
        except Exception as e:
            print(e)


def image(debug):

    while True:
        try:
            user_input = input('you: ')
            if user_input.lower() in ['quit', 'exit']:
                break
            response = generate_image_response(user_input)

            for i, image in enumerate(response['data']):
                text = f'image {i+1}'
                print(f"\x1b]8;;{image['url']}\a{text}\x1b]8;;\a")
                print(image['url'])
            if debug:
                print_usage(response)
        except Exception as e:
            print(e)


def print_usage(response):
    print(response)


def main(debug=False):
    if debug:
        print('debug mode')
    input_type = input('chat or image? ')
    if input_type == 'chat':
        chat(debug)
    elif input_type == 'image':
        image(debug)
    else:
        print('invalid input type')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    main(args.debug)
