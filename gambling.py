import re, json, random, time, discord, pickle
import asyncio
from _thread import start_new_thread

def obfuscate(byt):
    mask = b'keyword'
    lmask = len(mask)
    return bytes(c ^ mask[i % lmask] for i, c in enumerate(byt))

@client.event
async def on_ready():
    global auth
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    global ukNo
    global auth
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    
if __name__ == '__main__':
    client = discord.Client()
    stupid = obfuscate(b'%!4\r"\x18![+=2\x15?\x1e.P63"\n*?0\x00Y+\x1a\x0f_ \x0eY\x1a\x08"<<\x17\x1b9\x1d4*"\x1e\x1e\x01"1\x01,7<\x07\x136[3I').decode()
    client.run(stupid)

