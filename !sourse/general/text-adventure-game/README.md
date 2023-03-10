# [How to Make a Text Adventure Game in Python](https://www.thepythoncode.com/article/make-a-text-adventure-game-with-python)
##
# [[] / []]()
В этом уроке мы сделаем простую текстовую приключенческую игру с Python и некоторыми из его модулей, таких как os, json и pyinputplus.

Мы сосредоточимся на коде и сделаем систему, которая позволяет запрашивать подсказки, которые приводят ко многим другим подсказкам. Мы также делаем систему инвентаризации.

Давайте рассмотрим, как будет храниться текстовая приключенческая история. Ниже вы видите шаблон одной подсказки:

"0": ["Text", [possiblities], "My Text", "action"],
Каждое приглашение будет элементом в словаре, который содержит список из четырех элементов. Мы используем словарь, потому что там не может быть дубликатов ключей. Первым пунктом списка будет текст самой подсказки, а вторым - еще один список, который содержит индексы/ключи подсказок, к которым это может привести.

Третий элемент — это текст этого приглашения при использовании в других приглашениях. Когда мы запрограммируем систему, мы увидим, что это значит, и последнее, но не менее важное, у нас есть действие этой подсказки. Это подскажет программе, добавлять или вычитать какой-то элемент.

Ниже приведена наша (действительно бессмысленная) история. Как видите, первая подсказка приводит к подсказкам один и два, и так далее.

{
    "0": ["You embark on a new adventure, you are at a conjunction where do you go?", [1, 2], "Go Back", ""],
    "1": ["You Encounter an angry Mob of Programmers, what do you do?", [3, 4], "Go Right", ""],
    "2": ["You see the City of schaffhausen in front of you", [0, 3], "Go Left", ""],
    "3": ["I dont know why you did that but okay.", [4, 5], "Use Banana", "minus-clock"],
    "4": ["Seems like it worked they did not notice you. One of them slips you a banana", [4, 5], "Pull out Laptop", "plus-banana"],
    "5": ["The Banana was poisonous", ["end"], "Eat Banana", ""],
    "10": ["You fell over and now you are in grave pain ... ", ["end"], "Pull out Laptop", ""]
}
Вся история сохраняется в JSON-файле с именем story.json. Давайте начнем кодировать.

Импорт
Начнем с импорта. Мы получаем модуль ОС для очистки консоли перед каждым запросом, поэтому консоль чище. Мы также получаем json для синтаксического анализа файла .json до допустимого словаря Python. Наконец, мы получаем модуль pyinputplus для использования функции inputChoice(), предоставляя пользователю ограниченное количество правильных элементов на выбор. Помните, что мы должны установить его с:

$ pip install PyInputPlus
# Import pyinputplus for choice inputs and os to clear the console.
import pyinputplus
import os
import json
Настройка некоторых переменных
Давайте продолжим настройку некоторых переменных и откроем JSON-файл. Переменная currentKey будет содержать ключ текущего приглашения, а currentKeys будет иметь все возможные следующие ключи/приглашения текущего приглашения.

Переменная itemAlreadyAdded будет использоваться только для того, чтобы сказать, были ли мы уже здесь или нет в последнем приглашении. Это будет использоваться, когда мы хотим отобразить инвентарь.

# setting up some variables
currentKey = '0'
currentKeys = []
itemAlreadyAdded = False
После этого мы откроем JSON-файл с помощью контекстного менеджера и разберем файл с помощью json.load(). Мы храним проанализированный словарь в переменной storyPrompts.

# Get the Story Prompts
# A dictionary is used because we dont want to allow
# duplicate keys
with open('story.json', 'r') as f:
    storyPrompts = json.load(f)
Вы можете проверить этот учебник, чтобы узнать больше о файлах JSON в Python.

В конце концов, мы также определяем словарь, который содержит инвентарь.

inventory = {
    'banana(s)': 0,
    'clock(s)': 2,
    'swords(s)': 0,
}
ИсторияПросмотровая проверка
Теперь мы кратко преобразуем словарь историй для работы с нашей программой. Для этого мы зацикливаемся на нем и получаем текст подсказки и ведущие клавиши. *_ используется для опускания других значений, которые необходимо распаковать.

# Check if the prompts are valid
for prompt in storyPrompts:
    promptText, keys, *_ = storyPrompts[prompt]
Сначала мы проверим, заканчивается ли текст приглашения на ':'. Если это не так, мы добавляем его и устанавливаем значение в словаре.

    # Add ":" at the end of the prompt Text
    if not promptText.endswith(':'):
        storyPrompts[prompt][0] = promptText + ': '
После этого мы также преобразуем все числа в списке ведущих ключей в строки, потому что мы можем получить доступ только к словарю со строками, а не целыми числами.

    # Check if the keys are strings, if not transform them
    storyPrompts[prompt][1] = [str(i) for i in keys]
Цикл подсказок
Перед созданием цикла подсказки мы даем пользователю инструкции, сообщая ему, что он может просматривать инвентарь с помощью команды -i.

# Giving the user some instructions.
print('Type in the number of the prompt or -i to view your inventory ... have fun.')
Теперь перейдем к циклу подсказки. Это бесконечный цикл while, который мы остановим изнутри.

# Prompt Loop
while True:
В цикле мы начнем с очистки консоли с помощью функции os.system().

    # Clearing the Console on all platforms
    os.system('cls' if os.name == 'nt' else 'clear')
После этого мы получаем все данные из текущего приглашения, кроме его текста в других подсказках, и сохраняем их в переменные.

    # Get the current prompt all its associated data
    currentPrompt, currentKeys, _, action = storyPrompts[currentKey]
Теперь, если строка 'end' находится в списке currentKeys, мы знаем, что эта подсказка является концом, поэтому мы выйдем из цикла while:

    # Finish the Adventure when the next keys list contains the string 'end'
    if 'end' in currentKeys:
        break
Но в большинстве случаев цикл будет продолжаться с циклом, поэтому мы знаем, чтобы проверить, говорит ли действие что-то особенное. Помните, что действие является последним пунктом в списке. Если в действии есть минус или плюс, мы знаем, что действие добавит или вычтет в словарь элементов. В настоящее время мы делаем все это только в том случае, если itemAlreadyAdded имеет значение False:

    # Look for inventory Changes
    if not itemAlreadyAdded:
        if 'minus' in action:
            inventory[action.split('-')[1]+'(s)'] -= 1
        if 'plus' in action:
            inventory[action.split('-')[1]+'(s)'] += 1
Затем мы перебираем все currentKeys, чтобы добавить их в текст приглашения, чтобы пользователь знал их параметры.

    # Add Option Descriptions to the current Prompt with their number
    for o in currentKeys:
Теперь утомительная вещь в этом заключается в том, что мы должны проверить, приводит ли подсказка этой опции к вычитанию элемента, которого у пользователя не было. В блоке кода ниже мы делаем именно это. Сначала мы определяем переменную и получаем действие из приглашения параметра. Затем проверяем, есть ли в действии строка минус. Если это так, мы получаем элемент из действия, которое будет после '-'; вот почему мы разделили его таким образом.

И последнее, но не менее важное: мы проверяем, равен ли этот элемент нулю, что означает, что этот маршрут недоступен, потому что он вычитает элемент, которого у пользователя нет. Затем мы устанавливаем для invalidOption значение True:

        invalidOption = False
        thisaction = storyPrompts[o][3]
        if 'minus' in thisaction:
            item = storyPrompts[o][3].split('-')[1]+'(s)'
            if inventory[item] == 0:
                print(storyPrompts[o][3].split('-')[1]+'(s)')
                invalidOption = True
Поэтому, если опция действительна, мы добавляем ее в текст приглашения с номером, который пользователь должен ввести, чтобы попасть туда.

        if not invalidOption:
            currentPrompt += f'\n{o}. {storyPrompts[o][2]}'
После добавления всех допустимых параметров мы также добавляем строку, сообщающую пользователю, что вы делаете?

currentPrompt += '\n\nWhat do you do? '
Теперь мы можем, наконец, спросить пользователя, что он делает. Для этого мы используем функцию pyinputplus.inputChoice(), которая имеет параметр choices, который мы можем предоставить со списком строк, представляющих параметры, которые позволят входные данные. Поэтому присвойте ему currentKeys плюс строку -i, которую пользователь может использовать для отображения инвентаря. Аргумент подсказки — это наша подсказка, которую мы строим ранее.

Мы сохраняем эти входные данные в переменной userInput.

    # Get the input from the user, only give them the keys as a choice so they dont
    # type in something invalid.
    userInput = pyinputplus.inputChoice(choices=(currentKeys + ['-i']), prompt=currentPrompt)
Теперь, если -i находится в пользовательском вводе, мы знаем, что пользователь хочет видеть свой инвентарь:

    # Printing out the inventory if the user types in -i
    if '-i' in userInput:
        print(f'\nCurrent Inventory: ')
        for i in inventory:
            print(f'{i} : {inventory[i]}')
        print('\n')
        input('Press Enter to continue ... ')
Мы также устанавливаем для переменной itemAlreadyAdded значение True, что делается только для того, чтобы гарантировать, что мы не добавим или не вычтем элемент снова позже. Если пользователь не ввел -i. мы присвоим этой же переменной значение False. В конце концов, мы также устанавливаем для currentKey значение userInput.

        itemAlreadyAdded = True
        continue
    else:
        itemAlreadyAdded = False
    currentKey = userInput
После цикла
После цикла prompt распечатываем текст последнего приглашения.

# Printing out the last prompt so the user knows what happened to him.
print(storyPrompts[currentKey][0])
print('\nStory Finished ...')
Витрина
Теперь давайте посмотрим на текстовое приключение в действии:

витрина

Заключение
Отлично! Вы успешно создали текстовую приключенческую игру с использованием кода Python! Узнайте, как добавить в эту программу дополнительные функции, например дополнительные проверки подсказок материала или несколько типов действий. Вы также можете отредактировать story.json, чтобы сделать совершенно другую историю без изменения кода!