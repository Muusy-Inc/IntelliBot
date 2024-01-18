import websocket
import ssl
import requests
from json import loads, dumps
from PIL import Image
from io import BytesIO
import re
import random
from commands import process_imgur_link, fetch_joke, process_commands
from utils import is_bot_mentioned

nick = 'intelliBOT'  # Change this to your bot name!!!
channel_to_join = 'programming'  # Use lowercase 'programming'
password = '<your password>'
joke_api_url = 'https://v2.jokeapi.dev/joke/Any?blacklistFlags=political,sexist'  # JokeAPI URL

ws = websocket.create_connection("wss://hack.chat/chat-ws", sslopt={"cert_reqs": ssl.CERT_NONE})  # 1: connect
ws.send(dumps({'cmd': 'join', 'channel': channel_to_join, 'nick': nick, 'trip': 'datura', 'pass': password}))  # 2: join
print(f'The {nick} bot is now running...')

while True:
    result = loads(ws.recv())  # 3: receive data
    print(str(result))
    cmd = result['cmd']

    if cmd == 'chat':  # If someone sent a message...
        if result['nick'] == nick:
            continue

        msg = result['text']

        # Check if intelliBOT is mentioned
        if is_bot_mentioned(msg, nick):
            response_msg = "Need help? Here are some commands:\n" + process_commands()
            ws.send(dumps({'cmd': 'chat', 'text': response_msg}))
            continue

        # Check for Imgur links
        if 'imgur.com' in msg:
            process_imgur_link(ws, msg)

        # Check for !joke command
        if msg.lower() == '!joke':
            joke = fetch_joke()
            ws.send(dumps({'cmd': 'chat', 'text': joke}))

        # Process other commands
        process_commands(ws, msg, nick, channel_to_join)

    elif cmd == 'onlineSet':
        print(f'Users online: {result["nicks"]}\nPowered by {nick}!')

    elif cmd == 'info':
        if result['nick'] == nick and result['channel'] == channel_to_join:
            ws.send(dumps({'cmd': 'op', 'channel': channel_to_join, 'nick': nick}))  # Attempt to become a mod
            introduction_msg = "Hello fellow humanoids."
            ws.send(dumps({'cmd': 'chat', 'text': introduction_msg}))
