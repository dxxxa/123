# [How to Query the Ethereum Blockchain with Python](https://www.thepythoncode.com/article/query-ethereum-blockchain-with-python)
##
# [[] / []]()
Блокчейн — это инновационная технология, которая стала широко популярной во всем мире среди криптовалютных компаний, разработчиков и технологических компаний. Это база данных или неизменяемый реестр, который работает в распределенной сети узлов.

Центральной частью технологии блокчейн является блок или блок хранения данных, который состоит из цифровых транзакций. Когда блок заполняется данными, он соединяется с ранее заполненным блоком и образует цепочку блоков. Когда новая транзакция добавляется в блокчейн, она будет отражена в реестре каждого участника.

Блокчейн — это очень безопасная база данных, которую трудно взломать. Поэтому многие криптовалютные системы, такие как Биткойн, построены на технологии блокчейн для безопасных транзакций.

В этом уроке мы узнаем, как запрашивать блокчейн Ethereum в Python. Мы будем использовать клиент web3.py для запроса и подключения к узлам Ethereum и запроса его для получения различных типов информации.

Содержание:

Что такое блокчейн Ethereum?
Шаги, которые следует выполнить перед запросом блокчейна Ethereum
Шаг 1 - Установка Web3
Шаг 2 - Выберите, как вы подключаетесь к узлам Ethereum
Шаг 3 - Подключитесь к узлам Ethereum
Как запросить блокчейн Ethereum
Получение последнего блока
Запрос отдельных транзакций
Проверка правильности адреса блокировки
Проверка баланса конкретного блока
Запрос значений хранилища учетной записи
Запрос блоков дяди
Отправка транзакций
Как использовать функции смарт-контрактов?
Получение метаданных маркера
Поиск остатка на счете
Заключение
Что такое блокчейн Ethereum?
Ethereum - это децентрализованный блокчейн, который запускает код, известный как «умные контракты», которые являются самоисполняющимися или запрограммированными транзакциями, которые позволяют участникам безопасно совершать транзакции без центрального органа. Это основа для всех цифровых платежных приложений и денег, которые создали цифровую экономику во всем мире.

Самое главное, что Ethereum программируемый. Это означает, что вы можете запрашивать, создавать и развертывать приложения на Etherium.

Шаги, которые следует выполнить перед запросом блокчейна Ethereum
Шаг 1 - Установка Web3
Web3 основан на Javascript Web3.js, наиболее широко используемой клиентской библиотеке Python для взаимодействия с блокчейном Ethereum. Перед установкой Web3 проверьте, установлена ли на компьютере последняя версия Python. Если вы уже установили его на свой компьютер с Windows, вы можете найти его версию, введя в командной строке следующее:

$ python --version
Тогда вам хорошо установить библиотеку Python web3 для взаимодействия с блокчейном Ethereum. Используйте следующую команду для установки web3:

$ pip install web3
Шаг 2 - Выберите, как вы подключаетесь к узлам Ethereum
Есть два способа взаимодействия с блокчейном Ethereum. Чтобы запросить его для получения информации, такой как балансы и транзакции, вам нужно подключиться к его узлу, так же, как подключение к удаленной базе данных. Вы можете выбрать локальный или размещенный узел для запроса блокчейна Ethereum. В этом учебнике будет использоваться размещенный узел для подключения к блокчейну Ethereum.

Локальный узел — локальный узел — это узел, который запускается на локальном компьютере с использованием таких поставщиков, как Geth или Parity. Это позволяет быть более безопасным при подключении к узлам. Однако для настройки локального узла потребуется дополнительная работа, которая займет значительное время и ресурсы на вашем компьютере.
Шаги для подключения к узлам Ethereum с помощью локального узла:

Скачайте и установите Geth.
После установки введите geth --help.
Запустите Get и подождите, пока он не синхронизирует сеть.
Размещенный узел - размещенный узел - это узел, созданный и размещенный третьей стороной, над которым у вас нет никакого контроля. Он менее безопасен, чем локальный узел, потому что могут быть вредоносные размещенные узлы. Однако при выборе размещенного узла дополнительное время или ресурсы на установку не требуются.
Шаги для подключения к узлам Ethereum с помощью размещенного узла:

Создайте учетную запись в Infura.
Перейдите на панель мониторинга infura.io и создайте новый проект, указав имя.
После создания нового проекта вы увидите все учетные данные и конечные точки для размещенного узла Ethereum.



Шаг 3 - Подключитесь к узлам Ethereum
Существует три способа подключения к узлам Ethereum:

Протокол HTTP
ВебСокеры
МПК
В этом руководстве мы будем использовать поставщика HTTP.

Теперь, когда основные настройки узлов Python Web3 и Ethereum готовы, давайте перейдем к следующим шагам по подключению к узлу и запросу к нему. Прежде всего, запишите URL-адрес, предоставленный инфра-приложением, которое находится в следующем формате:

https://<endpoint>.infura.io/v3/<API_KEY>
Существует несколько различных конечных точек, таких как mainnet, ropsten, Kovan, rinkeby, goli и sepolia, и вы можете отформатировать свой URL-адрес в соответствии с типом поставщика. Кроме того, помните, что вы можете установить больше безопасности, добавив дополнительные настройки безопасности для своих проектов, такие как API Key secret и JWT.

Теперь создайте папку на своем компьютере, а внутри папки создайте тестовый файл Python с именем query_ethereum_blockchain.py. Добавьте к нему следующий код:

from web3 import Web3

# infura API key
API_KEY = "put your API key here"
# change endpoint to mainnet or ropsten or any other of your account
url = f"https://<endpoint>.infura.io/v3/{API_KEY}"

w3 = Web3(Web3.HTTPProvider(url))
res = w3.isConnected()
print(res)
С самого начала вам нужно импортировать библиотеку web3, чтобы использовать функции для взаимодействия с блокчейном Ethereum.

В переменной url укажите URL-адрес конечной точки, отмеченный ранее. Его также можно включить в отдельный файл конфигурации и импортировать в код URL-адрес, определенный в этом файле конфигурации.

Web3(Web3.HTTPProvider(url)) — это синтаксис, использующий HTTP для подключения к блокчейну. Программа распечатает следующий вывод при успешном подключении к узлу.

Выпуск:

True
Как запросить блокчейн Ethereum
Теперь, когда вы подключились к узлам Ethereum, мы будем использовать различные функции или методы библиотеки web3.py для запроса и получения различной информации из блокчейна.

Получение последнего блока
Давайте сначала проверим последний блок и посмотрим, что он содержит. Последние блочные данные обычно содержат различную информацию в атрибутивном словаре в следующем формате:

AttributeDict({
    'difficulty': 49824742724615,
    'extraData': '0xe4b883e5bda9e7a59ee4bb99e9b1bc',
    'gasLimit': 4712388,
    'gasUsed': 21000,
    'hash': '',
    'logsBloom': '',
    'miner': '',
    'nonce': '',
    'number': 2000000,
    'parentHash': '',
    'receiptRoot': '',
    'sha3Uncles': '',
    'size': 650,
    'stateRoot': '',
    'timestamp': 1470173578,
    'totalDifficulty': 44010101827705409388,
    'transactions': [''],
    'transactionsRoot': '',
    'uncles': [],
})
Используйте следующую команду для запроса последнего блока:
latest = w3.eth.get_block('latest')
print(latest)
Выходные данные будут представлять собой длинный текст, содержащий различные атрибуты и массив транзакций, который выглядит примерно так, как показано ниже:

AttributeDict({'baseFeePerGas': 18888809092, 'difficulty': 11728765655288682, 'extraData': HexBytes('0x486976656f6e2072752d68656176792d6f6664'), 'gasLimit': 30000000, 'gasUsed': 29552641, 'hash': HexBytes('0xa9155da2bbc945b8eb42f55fbbc9718de50e8cc932372645e36f3d7bb9d4da01'), 'logsBloom': ………………………………….. 'transactionsRoot': HexBytes('0x07b76aa5b8948e19e1f92b268e0545069a9924e8625605c1b4ade775ee99f465'), 'uncles': []})


Вы также можете распечатать номер блока следующим образом:
print(latest['number'])
Если вы проверяете вывод последнего блока, он содержит родительские хэши, указывающие на предыдущий блок, связанный с ним. Он выводит различные данные, такие как baseFeePerGas, extraData, gasLimit и т. Д. Кроме того, при выполнении кода несколько раз обратите внимание, что последний узел изменяется при каждом запуске кода.

Запрос отдельных транзакций
Теперь давайте проверим конкретный перевод, используя его хэш транзакции.

Ниже описано, как вы можете получить информацию о конкретной транзакции:
transaction1 = w3.eth.get_transaction('0x0e3d45ec3e1d145842ce5bc56ad168e4a98508e0429da96c1ff89f11076da36d')

print(transaction1)
Выходные данные транзакции выглядят следующим образом:



Вы также можете использовать номер блока для запроса транзакции следующим образом:
transaction2 = w3.eth.get_transaction_by_block(15410924, 0)
print(transaction2)
Если вы хотите получить количество транзакций в определенном блоке, вот как вы можете это сделать:
transactionCount = w3.eth.get_transaction_count('0x486976656f6e2065752d68656176792d657163')
print(transactionCount)

Output: 650
Проверка правильности адреса блокировки
Блокчейн Ethereum имеет определенные форматы адресов Ethereum. Вы можете использовать следующий код, чтобы проверить, является ли данный адрес допустимым или указанным в стандартном формате адреса:
isValid = w3.isAddress('0xed44e77fb3408cd5ad415d7467af6f6783218fb74c3824de1258f6d266bcc7b7')
print(isValid)
Кроме того, вы можете проверить, является ли адрес допустимым адресом контрольной суммы EIP55, используя следующий метод:
isChecksumAddressValid = Web3.isChecksumAddress('0x486976656f6e2065752d68656176792d657163')
print(isChecksumAddressValid)
Проверка баланса конкретного блока
Метод RPC eth.get_balance() можно использовать для запроса баланса конкретного счета в блоке, указанном следующим образом:block_identifier

balance = w3.eth.get_balance('0xd3CdA913deB6f67967B99D67aCDFa1712C293601')
print(balance)
Выпуск:

1790191567590102228
Запрос значений хранилища учетной записи
Если вы хотите запросить учетную запись и значения хранилища, такие как баланс учетной записи, хэш-код, merkle-proof, доказательство хранилища и т. Д. Это можно сделать с помощью метода get_proof(), определенного следующим образом:

proof = w3.eth.get_proof('0x486976656f6e2065752d68656176792d657163', [0], 3391)
print(proof)
Результат имеет формат, подобный приведенному ниже:

AttributeDict({
    'address': '',
    'accountProof': [],
    'balance': 0,
    'codeHash': '',
    'nonce': 1,
    'storageHash': '',
    'storageProof': [
        AttributeDict({
            'key': '0x00',
            'value': '',
            'proof': []
        })
    ]
})
Запрос блоков дяди
Блок дяди — это недобытый блок, который не является частью канонической цепочки. Блоки дяди создаются, когда более одного майнера одновременно создают блоки. Они похожи на потерянные блоки, которые вы можете отслеживать, запрашивая их с помощью следующего метода в web3:

w3.eth.get_uncle_by_block(15410924, 0)
При этом возвращается блок дяди для определенного идентификатора блока и по определенному индексу. Вы также можете использовать хэш вместо номера блока для идентификатора.

Кроме того, вы можете найти количество дядей в данном блоке.

w3.eth.get_uncle_count(15410924)
Отправка транзакций
Вы также можете использовать web3 для отправки транзакций в Ethereum. Существует два типа транзакций:

Транзакции по переводу баланса, когда вы отправляете eth на другой адрес, не требуя данных.
Кроме того, транзакции смарт-контракта, из которых можно отправить некоторый код смарт-контракта. Ниже приведен простой код, который подписывает и отправляет определенную транзакцию.
В следующем коде параметр transactions objects' to указывает, куда отправлять транзакцию, а значение from указывает, из какого блока отправляется транзакция. Значение nonce здесь — это количество количеств транзакций:

nonce = w3.eth.getTransactionCount('0x610Ae88399fc1687FA7530Aac28eC2539c7d6d63', 'latest');

transaction = {
     'to': '0x31B98D14007bDEe637298086988A0bBd31184523', 
     'from': '0x31B98D14007bDEe63EREEDFT34544646MOI22',
     'value': 500,
     'gas': 10000,
     'maxFeePerGas': 1000000208,
     'nonce': nonce,
};
   
w3.eth.send_transaction(transaction)
Кроме того, вы можете использовать метод подписанного перевода для подписания транзакции с использованием закрытого ключа узлов Ethereum. Ниже приведен пример того, как это можно сделать:

nonce = w3.eth.getTransactionCount('0x610Ae88399fc1687FA7530Aac28eC2539c7d6d63', 'latest');

signed = w3.eth.sign_transaction(
    dict(
        nonce=nonce,
        maxFeePerGas=34300000,
        maxPriorityFeePerGas=25000000,
        gas=100000,
        to='0xerecfBYWlB99D67aCDFa17EREFEerrtr73601',
        value=1,
        data=b'',
    )
)
Как использовать функции смарт-контрактов?
Web3 также имеет методы взаимодействия со смарт-контрактами в блокчейне Ethereum, которые публично раскрываются. Для взаимодействия с ними необходимы две части информации: абстрактные двоичные интерфейсы (ABI) и адреса смарт-контрактов. Вы можете найти эту информацию с помощью проводника блоков Etherscan.

Во-первых, необходимо инициализировать экземпляр контракта, используя ABI и адрес:

address = '0x706f6f6c696e2e636f6d21688947c8f76c4e92'
abi = '[{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address","name":"minter_",........'

contract = w3.eth.contract(address=address, abi=abi)
Далее вы можете использовать различные публичные функции смарт-контрактов для запроса блокчейна:

totalSupply = contract.functions.totalSupply().call()
print(totalSupply)
Используйте следующие команды для считывания данных и обновления состояния:

contract.functions.stored value().call()
tx_hash = contract.functions.updateValue(<statevalue>).transact()
Получение метаданных маркера
Используя простые методы функции контракта, можно получить метаданные маркера, такие как количество маркеров, имя контракта, десятичные дроби и символ контракта:

print(contract.functions.name().call())
print(contract.functions.decimals().call())
print(contract.functions.symbol().call())
Выпуск:

SHIBACHU
9
SHIBACHU
Поиск остатка на счете
Еще одна вещь, которую мы можем сделать, используя функции контракта, - это найти баланс счета с помощью публичной функции balanceOf():

address = '0x5eaaf114aad1313e7440d2ff805ced993e566df'
balance = contract.functions.balanceOf(address).call()
Заключение
Мы начали эту статью с объяснения технологии блокчейн и блокчейна Ethereum. Далее мы объяснили, как запрашивать блокчейн Ethereum с помощью библиотеки web3.py Pythons, которая предоставляет полный список методов запроса блокчейна Ethereum. Мы выполнили следующие взаимодействия с блокчейном Ethereum, используя библиотеку web3.py.

Как получить последний блок.
Как запрашивать отдельные переходы.
Как проверить действительность блока Ethereum.
Как запросить значения хранилища учетной записи.
Что такое дядя блоки, и как их запрашивать.
Как отправлять транзакции.
Некоторые основные вещи, которые вы можете сделать с функциями смарт-контрактов.
Наконец, если вы хотите, чтобы кто-то сделал это за вас, ознакомьтесь с нашими Webisoft.com.