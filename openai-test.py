import argparse
import os

from termcolor import colored

import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

history = [{'role': 'system', 'content': 'You are a helpful assistant.'}]


def generate_chat_response(user_input):
    history.append({'role': 'user', 'content': user_input})
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo', messages=history
    )
    history.append(
        {'role': 'system', 'content': response.choices[0].message.content}
    )
    return response


def generate_image_response(user_input):
    response = openai.Image.create(prompt=user_input, n=3, size='1024x1024')

    return response


def chat(debug=False):
    while True:
        try:
            user_input = input('you: ')
            if user_input.lower() in ['quit', 'exit']:
                break
            response = generate_chat_response(user_input)
            print(
                colored('GPT:', 'black', 'on_white'),
                colored(
                    response['choices'][0]['message']['content'],
                    'light_red',
                ),
            )
            if debug:
                print_usage(response)
        except Exception as e:
            print(e)


def image(debug=False):

    while True:
        try:
            user_input = input('Image prompt: ')
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
    parser.add_argument(
        '--debug', help='Activate debug mode', action='store_true'
    )
    parser.add_argument(
        '--chat', help='Activate chat mode', action='store_true'
    )
    parser.add_argument(
        '--image', help='Activate image mode', action='store_true'
    )
    args = parser.parse_args()
    if args.chat & args.image:
        print('To many arguments')
        exit()
    elif args.chat:
        chat(args.debug)
        exit()
    elif args.image:
        image(args.debug)
        exit()
    main(args.debug)
