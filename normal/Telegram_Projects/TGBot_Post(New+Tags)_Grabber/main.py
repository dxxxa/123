# https://zelenka.guru/threads/1851054/

from telethon import TelegramClient, events, errors
import asyncio
import re
# ----
api_id = 28297361
api_hash = "e0eed1ec03e7de3c444d73f3aef9ce68"
# ----
my_channel = 'opopoq'  # куда
channels = 'sfgddygff', 'gvghhq'  # откуда
# -----
KEYS = {
    "байден": 'Омерикос',
    "Евросоюз": 'Гейропа',
    "Россию": "СССР",
    "ссылка:": "",
    r"@\S+": "Максим",
    r"https://\S+": "",
    r"http://\S+": "",
    "пила жесть": "[уже не пила](https://t.me/max_reynders)"
}
# ----
# Bad_Keys - список стоп слов, если в посте будет слово из списка, пост не попадет к вам в канал, просто будет пропущен.
Bad_Keys = ['биткоин', 'биток', 'ставки', 'казино']
# ----
tags = '\n\n├ +\n├ +\n└ +'  # '\n\n[новостной канал](https://t.me/max_reynders) | @max_reynders'
# добавление текста к посту, если не надо оставить ковычки пустыми ""
# ----
with TelegramClient('myApp13', api_id, api_hash) as client:
    print("～Activated～")

    @client.on(events.NewMessage(chats=channels))
    async def Messages(event):
        if not [element for element in Bad_Keys
                if event.raw_text.lower().__contains__(element)]:
            text = event.raw_text
            for i in KEYS:
                text = re.sub(i, KEYS[i], text)
            if not event.grouped_id\
                    and not event.message.forward:
                try:
                    await client.send_message(
                        entity=my_channel,
                        file=event.message.media,
                        message=text + tags,
                        parse_mode='md',
                        link_preview=False)
                except errors.FloodWaitError as e:
                    print(f'[!] Ошибка флуда ждем: {e.seconds} секунд')
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    print('[!] Ошибка', e)
            elif event.message.text and not event.message.media\
                and not event.message.forward\
                    and not event.grouped_id:
                try:
                    await client.send_message(
                        entity=my_channel,
                        message=text + tags,
                        parse_mode='md',
                        link_preview=False)
                except errors.FloodWaitError as e:
                    print(f'[!] Ошибка флуда ждем: {e.seconds} секунд')
                    await asyncio.sleep(e.seconds)
                except Exception as e:
                    print('[!] Ошибка', e)
            elif event.message.forward:
                try:
                    await event.message.forward_to(my_channel)
                except errors.FloodWaitError as e:
                    print(f'[!] Ошибка флуда ждем: {e.seconds} секунд')
                except Exception as e:
                    print('[!] Ошибка', e)

    @client.on(events.Album(chats=channels))
    async def Album(event):
        text = event.original_update.message.message
        print(text)
        if not [element for element in Bad_Keys
                if text.lower().__contains__(element)]:
            for i in KEYS:
                text = re.sub(i, KEYS[i], text)
            try:
                await client.send_message(
                    entity=my_channel,
                    file=event.messages,
                    message=text + tags,
                    parse_mode='md',
                    link_preview=False)
            except errors.FloodWaitError as e:
                print(f'[!] Ошибка флуда ждем: {e.seconds} секунд')
                await asyncio.sleep(e.seconds)
            except Exception as e:
                print('[!] Ошибка', e)

    client.run_until_disconnected()
