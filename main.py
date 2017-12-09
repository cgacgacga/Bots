from cmath import phase
from email import message


import config
import telebot
import json

token = config.token
bot = telebot.TeleBot(config.token)
tag = ''
phrase = ''

@bot.message_handler(commands=['start', 'find'])
def main(message): # Название функции не играет никакой роли, в принципе
    sent = bot.send_message(message.chat.id, 'Привет!Введи слово и я выдам тебе цитату.')
    bot.register_next_step_handler(sent, fileSearch)

@bot.message_handler(commands=['adminbot'])
def adminbot(message):
    sent = bot.send_message(message.chat.id, "Вы перешли в версию для администрирования.\n"
                                             "Выберите действие:\n"
                                             "1 - Добавить новую цитату\n"
                                             "2 - Удалить последнюю\n"
                                             "3 - Выйти из меню администрирования")
    bot.register_next_step_handler(sent, admin)

@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, "Это команда тест")

def check (message):
    if message.text == '/start':
        main(message)
    elif message.text == '/adminbot':
        adminbot(message)
    elif message.text == '/find':
        main(message)
    else:
        return 0
    return 1


def addPhrase(message):
    with open('DB.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    id = str(len(data) + 1)

    element = {
        "ID": id,
        # "Tag": tag,
        # "Phrase": phrase
        "Тэг": tag,
        "Цитата": phrase
    }

    try:
        data.append(element)
        with open('DB.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except:
        bot.send_message(message.chat.id, "ooops")
    sent = bot.send_message(message.chat.id, "№ {i}\nТэги: {t}\nЦитата: {p}\nЗаписаны в базу данных".format(i = id, t = tag, p = phrase))
    bot.register_next_step_handler(sent, admin)
    bot.send_message(message.chat.id, "Выберите одну из команд\n"
                                      "1 - Добавить новую цитату\n"
                                      "2 - Удалить последнюю\n"
                                      "3 - Выйти из меню администрирования")


def deleteLastPhrase(message):
    with open('DB.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    try:
        data.pop()
        with open('DB.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
    except:
        bot.send_message(message.chat.id, "ooops")

    id = len(data) - 1
    sent = bot.send_message(message.chat.id,
                            "Теперь последняя цитата:\n№{i}\nТэг: {t}\nЦитата: {p}".format(i=id, t=data[id]["Цитата"], p=data[id]["Цитата"]))
    bot.register_next_step_handler(sent, admin)

    bot.send_message(message.chat.id, "Выберите одну из команд\n"
                                      "1 - Добавить новую цитату\n"
                                      "2 - Удалить последнюю\n"
                                      "3 - Выйти из меню администрирования")

def find(message):
    # Открываем файл базы данных для чтения
    # Пробегать циклом по базе данных и искать цитату по введенному слову (message.text)
    # Вывести цитату
    # Проверить message.text , если ввели /adminbot , вызвать admin
    # Рекурсивно вызвать find(message)
    bot.send_message(message.chat.id, "Выполняется поиск...")

def fileSearch(message):
    if (check(message) == 1):
        return

    with open('DB.json', encoding='utf-8') as data_file:
        data = json.loads(data_file.read())

    for i in range(0, len(data)):
        element = data[i]["Тэг"]
        for element in data[i]["Тэг"]:
            if message.text == element:
                sent = bot.reply_to(message, data[i]["Цитата"])
                bot.register_next_step_handler(sent, fileSearch)
                return
    else:
        str = bot.send_message(message.chat.id, 'Цитаты по такому слову не найдено, попробуй что-нибудь еще')
        bot.register_next_step_handler(str, fileSearch)


def inputTag(message):
    if (check(message) == 1):
        return
    global tag
    tag = message.text.split(', ')
    sent = bot.send_message(message.chat.id, "Теперь введите цитату без ковычек")
    bot.register_next_step_handler(sent, inputPhrase)


def inputPhrase(message):
    if (check(message) == 1):
        return
    global phrase
    phrase = message.text
    addPhrase(message)

def admin(message):
    if (check(message) == 1):
        return
    if message.text == '1':
        sent = bot.send_message(message.chat.id, "Введите тэги.\nФормат: \"первый, второй, третий\".\nПодряд с маленькой буквы разделяя запятой")
        bot.register_next_step_handler(sent, inputTag)
        # keyboard = types.InlineKeyboardMarkup()
        # url_button = types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
        # keyboard.add(url_button)
        # bot.send_message(message.chat.id, "Привет! Нажми на кнопку и перейди в поисковик.", reply_markup=keyboard)
    elif message.text == '2':
        deleteLastPhrase(message)
    elif message.text == '3':
        main(message)
    else:
        sent = bot.send_message(message.chat.id, "Такой функции не существует")
        bot.register_next_step_handler(sent, admin)


if __name__ == '__main__':
     bot.polling(none_stop=True)
