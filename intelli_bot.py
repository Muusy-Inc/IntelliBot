import websocket
import ssl
from json import loads, dumps
from commands.fun_commands import process_fun_command
from commands.meme_commands import process_meme_command
from utils.image_processing import process_imgur_link
from utils.joke_fetcher import fetch_joke

# Configuration
nick = 'IntelliBot'
channel_to_join = 'programming'
password = '<your password>'
joke_api_url = 'https://v2.jokeapi.dev/joke/Any?blacklistFlags=political,sexist'

ws = websocket.create_connection("wss://hack.chat/chat-ws", sslopt={"cert_reqs": ssl.CERT_NONE})
ws.send(dumps({'cmd': 'join', 'channel': channel_to_join, 'nick': nick, 'trip': 'datura', 'pass': password}))
print(f'The {nick} bot is now running...')

while True:
    try:
        result = loads(ws.recv())
        cmd = result['cmd']

        if cmd == 'chat':
            msg = result['text']
            
            # Process different commands based on cmd value
            if "No Homo" in msg and "then homo" in msg.lower():
                random_number = random.randint(1, 100)
                response_msg = f"{random_number} homo"
                ws.send(dumps({'cmd': 'chat', 'text': response_msg}))

            # Check for Imgur links
            if 'imgur.com' in msg:
                process_imgur_link(msg)

            # Check for !joke command
            if msg.lower() == '!joke':
                joke = fetch_joke()
                ws.send(dumps({'cmd': 'chat', 'text': joke}))

            # Process fun commands
            process_fun_command(msg)

            # Process meme commands
            process_meme_command(msg)

        elif cmd == 'onlineSet':
            print(f'Users online: {result["nicks"]}\nPowered by {nick}!')

        elif cmd == 'info':
            if result['nick'] == nick and result['channel'] == channel_to_join:
                ws.send(dumps({'cmd': 'op', 'channel': channel_to_join, 'nick': nick}))
                introduction_msg = "Hello fellow humanoids. Type !help for commands."
                ws.send(dumps({'cmd': 'chat', 'text': introduction_msg}))

    except Exception as e:
        print(f"Error: {e}")
