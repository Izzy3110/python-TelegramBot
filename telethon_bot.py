import asyncio
from telethon import TelegramClient, events

import configparser
import json
import re
from telethon.errors import SessionPasswordNeededError
from telethon import TelegramClient, events, sync
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)

api_id = "11616477"
api_hash = "770f84399a0379b2c25080dd1b9dd175"

# Here you define the target channel that you want to listen to:
user_input_channel = 'https://t.me/wyl22dev'
subjectFilter = ['physics', 'mathematics', 'maths', 'math']
levelFilter = ['sec', 'secondary', 'junior college', 'jc']


async def main(api_id="11616477", api_hash="770f84399a0379b2c25080dd1b9dd175"):
    async with TelegramClient('name', api_id, api_hash) as client:
        me = await client.get_me()
        print(me.stringify())

        async for message in client.iter_messages('me'):
            print(message.id, message.text)

        await client.send_message('me', 'Hello, myself!')

        # print(await client.download_profile_photo('me'))

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
                        await client.forward_messages(entity=user["id"], messages=event.message)

        @client.on(events.NewMessage(pattern='(?i).*Hello'))
        async def handler(event):
            await event.reply('Hey!')

        await client.run_until_disconnected()


asyncio.run(main())
