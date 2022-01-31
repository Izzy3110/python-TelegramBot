import asyncio
import os

import socks
import json
import re
from telethon import TelegramClient, events

api_id = os.environ["API_ID"]
api_hash = os.environ["API_HASH"]

# Here you define the target channel that you want to listen to:
user_input_channel = 'https://t.me/wyl22dev'

subjectFilter = ['physics', 'mathematics', 'maths', 'math']
levelFilter = ['sec', 'secondary', 'junior college', 'jc']
proxy = (socks.SOCKS5, "127.0.0.1", "3128")


async def main(api_id="11616477", api_hash="770f84399a0379b2c25080dd1b9dd175"):
    async with TelegramClient('name', api_id, api_hash, proxy=proxy) as client:
        
        @client.on(events.NewMessage(chats=user_input_channel))
        async def newMessageListener(event):
            newMessage = event.message.message
            print(newMessage)
            subject_filtered = re.findall(r"(?=(" + '|'.join(subjectFilter) + r"))", newMessage, re.IGNORECASE)
            if len(subject_filtered) != 0:
                print("sub found")
                print(subject_filtered)
                level_filtered = re.findall(r"(?=(" + '|'.join(levelFilter) + r"))", newMessage, re.IGNORECASE)
                if len(level_filtered) != 0:
                    print("level")
                with open("users.json") as users_f:
                    users = json.loads(users_f.read())
                    for user in users:
                        print("id: "+str(user["id"]))
                    await client.forward_messages(entity="@wyl2022_bot", messages=event.message)

        @client.on(events.NewMessage(pattern='(?i).*Hello'))
        async def handler(event):
            await event.reply('Hey!')

        await client.run_until_disconnected()


asyncio.run(main())
