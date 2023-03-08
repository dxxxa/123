import time

from pyrogram import Client


API_ID = 28297361
API_HASH = "e0eed1ec03e7de3c444d73f3aef9ce68"
PHONE_NUMBER = '+79693053554'  # номер зарегистрованный в телеге

app = Client("cyberpunk", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)  # cyberpunk - файл сессии



links = open('Channels.txt')

with app:
    for line in links.readlines():
        app.join_chat(line.strip())
        time.sleep(5)
app.run()
