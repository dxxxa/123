from telethon import TelegramClient, events
import asyncio

api_id = 28297361
api_hash = "e0eed1ec03e7de3c444d73f3aef9ce68"

my_channel_id = -1001803361079
channels = [-1001805734430,
            -1001881156407]  # sfgddygff

client = TelegramClient('myGrab', api_id, api_hash)
print("GRAB - Started")


@client.on(events.NewMessage(chats=channels))
async def my_event_handler(event):
    if event.message and not event.grouped_id:
        await client.send_message(my_channel_id, event.message)
        print(event.message)


@client.on(events.Album(chats=channels))
async def handler(event):
    await client.send_message(
        my_channel_id,
        file=event.messages,
        message=event.original_update.message.message,
    )


client.start()
client.run_until_disconnected()
