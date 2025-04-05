import random
import telebot
from telebot import types
from telebot.types import Message

bot = telebot.TeleBot("7296473058:AAHMXwh5EDKoBm9Y9qvIvlDfM5E83_556RQ")

Jokes = [
    "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25.",
    "Как называют программиста, который не боится работы? Ленивый.",
    "Сколько программистов нужно, чтобы вкрутить лампочку? Ни одного, это hardware проблема.",
    "Почему 1 + 1 = 10? Потому что это двоичная система!",
    "Заходит как-то нейросеть в бар... а там все единицы и нули.",
]


@bot.message_handler(commands=["about"])
def about(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(
        message.from_user.id,
        "Создатьель бота: Соловьев Алексардр \nСтудент группы: ИСТ-233902у",
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["help"])
def help(message):

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bot.send_message(
        message.from_user.id,
        "Комманды бота\n/about: Выводит информацию о авторе бота\n/help: выводит справку по командам для работы с ботом\n/joke: Выводит случайную шутку\n/math: выводит случайный пример уравнения с ответом",
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["joke"])
def send_joke(message: Message):
    joke = random.choice(Jokes)
    bot.reply_to(message, joke)


@bot.message_handler(commands=["math"])
def math(message: Message):

    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operation = random.choice(["+", "-", "*", "/"])

    if operation == "+":
        result = a + b
    elif operation == "-":
        result = a - b
    elif operation == "*":
        result = a * b
    elif operation == "/":
        result = a // b

    bot.reply_to(
        message,
        f"{a} {operation} {b} = ?\n\n<tg-spoiler>{result}</tg-spoiler>",
        parse_mode="HTML",
    )


@bot.message_handler(content_types=["text"])
def get_text_messages(message):

    if message.text == "привет":
        bot.send_message(
            message.from_user.id,
            "Привет-привет! Как дела?",
            parse_mode="Markdown",
        )

    elif message.text == "как дела?":
        bot.send_message(
            message.from_user.id,
            "У меня все отлично! А у тебя?",
            parse_mode="Markdown",
        )

    elif message.text == "ты кто?":
        bot.send_message(
            message.from_user.id,
            "Я бот для шуток и математики! Напиши /help для списка команд.",
            parse_mode="Markdown",
        )
    else:
        bot.send_message(
            message.from_user.id,
            "Я не понимаю. Напиши /help для списка команд.",
            parse_mode="Markdown",
        )


bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть
