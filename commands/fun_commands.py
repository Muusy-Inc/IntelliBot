import random

# Define fun commands
def process_fun_command(msg):
    if "roll" in msg.lower():
        roll_result = random.randint(1, 6)
        ws.send(dumps({'cmd': 'chat', 'text': f"Rolls a die: {roll_result}"}))
