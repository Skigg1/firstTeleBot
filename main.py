import random
import telebot
from telebot import types
from telebot.types import Message
import time
from config import BOT_TOKEN  # Импорт токена из config.py

bot = telebot.TeleBot(BOT_TOKEN)

Jokes = [
    "Почему программисты путают Хэллоуин и Рождество? Потому что Oct 31 == Dec 25.",
    "Как называют программиста, который не боится работы? Ленивый.",
    "Сколько программистов нужно, чтобы вкрутить лампочку? Ни одного, это hardware проблема.",
    "Почему 1 + 1 = 10? Потому что это двоичная система!",
    "Заходит как-то нейросеть в бар... а там все единицы и нули.",
]


# Обработчики команд должны быть объявлены ДО запуска бота
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message, "Привет! Я бот для шуток и математики. Напиши /help для списка команд."
    )


@bot.message_handler(commands=["about"])
def about(message):
    markup = types.InlineKeyboardMarkup()
    btn_contact = types.InlineKeyboardButton(
        "Связаться", url="https://github.com/Skigg1"
    )
    btn_portfolio = types.InlineKeyboardButton(
        "Портфолио", url="https://github.com/Skigg1"
    )
    markup.add(btn_contact, btn_portfolio)
    bot.send_message(
        message.chat.id,
        "Создатель бота: Соловьев Александр\nСтудент группы: ИСТ-233902у",
        reply_markup=markup,
    )


@bot.message_handler(commands=["help"])
def help(message):
    markup = types.InlineKeyboardMarkup()
    btn_about = types.InlineKeyboardButton("About", callback_data="help_about")
    btn_joke = types.InlineKeyboardButton("Joke", callback_data="help_joke")
    btn_math = types.InlineKeyboardButton("Math", callback_data="help_math")
    markup.add(btn_about, btn_joke, btn_math)
    bot.send_message(
        message.chat.id,
        "Выберите команду для получения подробной информации:",
        reply_markup=markup,
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("help_"))
def help_callback(call):
    command = call.data[5:]
    if command == "about":
        text = "Команда /about\nПоказывает информацию о создателе бота с контактами"
    elif command == "joke":
        text = "Команда /joke\nПоказывает случайную шутку про программистов\nМожно запросить новую шутку кнопкой"
    elif command == "math":
        text = "Команда /math\nГенерирует математическую задачу с вариантами ответов"
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text)


@bot.message_handler(commands=["joke"])
def send_joke(message: Message):
    joke = random.choice(Jokes)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_another = types.KeyboardButton("Ещё шутку")
    markup.add(btn_another)
    bot.reply_to(message, joke, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Ещё шутку")
def another_joke(message):
    send_joke(message)


@bot.message_handler(commands=["math"])
def math(message: Message):
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operation = random.choice(["+", "-", "*", "/"])

    if operation == "+":
        correct = a + b
    elif operation == "-":
        correct = a - b
    elif operation == "*":
        correct = a * b
    else:
        correct = round(a / b, 2) if a % b != 0 else a // b

    answers = [correct]
    while len(answers) < 4:
        wrong = correct + random.choice([-2, -1, 1, 2])
        if wrong != correct and wrong > 0 and wrong not in answers:
            answers.append(wrong)

    random.shuffle(answers)
    markup = types.InlineKeyboardMarkup()
    for answer in answers:
        markup.add(
            types.InlineKeyboardButton(
                str(answer), callback_data=f"math_answer_{answer}_{correct}"
            )
        )
    bot.send_message(
        message.chat.id, f"Решите: {a} {operation} {b} = ?", reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("math_answer_"))
def math_callback(call):
    _, _, answer, correct = call.data.split("_")
    answer = float(answer) if "." in answer else int(answer)
    correct = float(correct) if "." in correct else int(correct)
    response = (
        "Верно! Отличная работа!"
        if answer == correct
        else f"Неверно. Правильный ответ: {correct}"
    )
    bot.answer_callback_query(call.id, response)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None,
    )


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    text = message.text.lower()
    if text == "привет":
        bot.send_message(message.chat.id, "Привет-привет! Как дела?")
    elif text == "как дела?":
        bot.send_message(message.chat.id, "У меня все отлично! А у тебя?")
    elif text == "ты кто?":
        bot.send_message(
            message.chat.id,
            "Я бот для шуток и математики! Напиши /help для списка команд.",
        )
    else:
        bot.send_message(
            message.chat.id, "Я не понимаю. Напиши /help для списка команд."
        )


def start_bot():
    try:
        bot.delete_webhook()
        time.sleep(1)
        print("Бот запускается...")
        bot.infinity_polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"Ошибка: {e}")
        time.sleep(5)
        start_bot()


if __name__ == "__main__":
    start_bot()
