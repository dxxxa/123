# [How to Make Facebook Messenger bot in Python](https://www.thepythoncode.com/article/make-bot-fbchat-python)
To run this:
- `pip install -r requirements.txt`
- 
    ```
    python messenger_bot.py
    ```
##
# [[] / []]()
Возможность автоматизировать вещи и сделать полезных ботов в мессенджере Facebook кажется интересной и крутой, вэтом уроке мы увидим, как мы можем подключаться в мессенджере Facebook на Python и делать различные классные вещи!

Мы будем использовать библиотеку fbchat, она работает путем эмуляции браузера. Это означает выполнение тех же самых запросов GET / POST и обман Facebook, заставляя его думать, что он обычно получает доступ к веб-сайту. Поэтому этот API не является официальным и не требует какого-либо ключа API, вместо этого он требует учетных данных вашей учетной записи Facebook.

Связанные с: Как сделать Telegram-бота на Python.

Во-первых, вам нужно будет установить библиотеку fbchat:

pip3 install fbchat
Теперь, чтобы начать, сделайте пустой файл python или откройте интерактивную оболочку или записную книжку jupyter и следуйте за ним, давайте импортируем fbchat:

from fbchat import Client
from fbchat.models import Message
Давайте сначала войдем в систему:

# facebook user credentials
username = "username.or.email"
password = "password"
# login
client = Client(username, password)
Примечание: Вам нужно ввести правильные учетные данные facebook, иначе не будет иметь смысла следовать этому руководству.

У нас теперь есть клиентский объект, в нем много полезных методов, попробуйте dir() его.

Например, давайте узнаем пользователей, с которыми вы недавно разговаривали:

# get 20 users you most recently talked to
users = client.fetchThreadList()
print(users)
Это приведет к списку потоков, поток может быть пользователем или группой.

Давайте найдем нашего лучшего друга, давайте получим всю информацию, которую мы можем получить об этих пользователях:

# get the detailed informations about these users
detailed_users = [ list(client.fetchThreadInfo(user.uid).values())[0] for user in users ]
К счастью для нас, объект потока имеет атрибут message_count, который подсчитывает количество сообщений между вами и этим потоком, мы можем сортировать по этому атрибуту:

# sort by number of messages
sorted_detailed_users = sorted(detailed_users, key=lambda u: u.message_count, reverse=True)
Теперь у нас есть список из 20 пользователей, отсортированных по message_count, давайте легко получим лучшего друга по:

# print the best friend!
best_friend = sorted_detailed_users[0]
print("Best friend:", best_friend.name, "with a message count of", best_friend.message_count)
Давайте поздравим этого друга, отправив сообщение:

# message the best friend!
client.send(Message(text=f"Congratulations {best_friend.name}, you are my best friend with {best_friend.message_count} messages!"),
            thread_id=best_friend.uid)
Позвольте мне взглянуть на сообщения:

Сообщение, отправленное PythonПотрясающе, не так ли?

Если вы хотите получить всех пользователей, с которыми вы общались в мессенджере, вы можете:

# get all users you talked to in messenger in your account
all_users = client.fetchAllUsers()
print("You talked with a total of", len(all_users), "users!")
Наконец, когда вы закончите, убедитесь, что вы вышли из системы:

# let's logout
client.logout()
Как вы можете видеть, есть бесконечные возможности, которые вы можете сделать с этой библиотекой, вы можете делать автоматические ответные сообщения, чат-бот, эхобот и многие другие крутые функции. Пожалуйста, ознакомьтесь с их официальной документацией.

У нас также есть учебник по созданию Telegram-бота, проверьте его!