from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3
import random
from dotenv import load_dotenv
import os
from datetime import datetime
import logging

# Загрузка переменных окружения
load_dotenv()

# Telegram ID пользователей, которые могут пользоваться ботом
ALLOWED_USERS = [7666108269, 1278614067]  # Укажите свои ID

# Инициализация логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Список загадок
riddles = [
    {"question": "Что всегда идет, но никогда не останавливается?", "answer": "время"},
    {"question": "Чем больше из него берёшь, тем больше оно становится. Что это?", "answer": "яма"},
    {"question": "Оно может ломаться, даже если ты его не трогаешь. Что это?", "answer": "обещание"},
    {"question": "Что принадлежит тебе, но другие используют его чаще, чем ты?", "answer": "имя"},
    {"question": "Что становится больше, если его перевернуть вверх ногами?", "answer": "число 6"},
    {"question": "Чем больше его моешь, тем грязнее оно становится. Что это?", "answer": "вода"},
    {"question": "Что можно услышать, но нельзя увидеть и потрогать, хотя оно невидимо?", "answer": "эхо"},
    {"question": "Что всегда перед тобой, но ты никогда не можешь его догнать?", "answer": "будущее"},
    {"question": "Что не имеет веса, но его нельзя удержать долго?", "answer": "дыхание"},
    {"question": "Меня можно сломать, даже не касаясь. Что я?", "answer": "тишина"}
]

# Список челленджей
challenges = [
    "💌 Напишите письмо любимому человеку и отправьте его почтой.",
    "🎵 Создайте плейлист из песен, которые ассоциируются с вашими отношениями.",
    "📸 Найдите старую фотографию вас двоих и расскажите, что было в тот день.",
    "🎯 Придумайте общую цель на неделю и попробуйте выполнить её вместе.",
    "💡 Изучите новый навык или факт, а потом расскажите об этом друг другу.",
    "🍴 Приготовьте одно и то же блюдо и обсудите, у кого получилось вкуснее.",
    "📖 Прочитайте одну и ту же главу книги и поделитесь мыслями.",
    "🎥 Посмотрите фильм вместе и обсудите его сразу после просмотра.",
    "🎁 Сделайте неожиданную доставку любимого блюда для партнёра.",
    "📞 Проведите вечерний видеозвонок и поговорите обо всём, что пришло в голову.",
    "🎨 Нарисуйте что-нибудь друг для друга и обменяйтесь рисунками.",
    "🍹 Попробуйте приготовить один и тот же коктейль и сравните вкусы.",
    "🌟 Обсудите, как вы представляете своё будущее через 5 лет.",
    "📝 Напишите 10 вещей, которые вы любите в своём партнёре, и поделитесь ими.",
    "🕵️‍♂️ Загадайте друг другу загадку, которую партнер должен отгадать.",
    "🎶 Спойте или запишите голосовое сообщение с любимой песней для партнёра.",
    "🤔 Напишите 3 неожиданных факта о себе – пусть партнер попробует угадать, что правда.",
    "🎭 Изобразите любимую сцену из фильма по видеозвонку и пусть партнер угадает.",
    "📚 Поменяйтесь любимыми книгами и обсудите, понравилась ли вам история.",
    "🌍 Запланируйте виртуальное путешествие – выберите страну и изучите её культуру."
]

# Хранение текущей загадки для пользователей
current_riddles = {}

# Функция проверки пользователя
def is_allowed(user_id):
    return user_id in ALLOWED_USERS

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat (
            id INTEGER PRIMARY KEY,
            user TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gratitude (
            id INTEGER PRIMARY KEY,
            user TEXT,
            message TEXT,
            timestamp TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS list_items (
            id INTEGER PRIMARY KEY,
            item TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY,
            goal TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dates (
            id INTEGER PRIMARY KEY,
            date TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("❌ Вы не авторизованы для использования этого бота.")
        return

    await update.message.reply_text(
        "👋 Привет! Это ваш семейный бот. Вот доступные команды:\n\n"
        "✨ /gratitude - Добавить благодарность\n"
        "📖 /viewgratitudes - Просмотреть благодарности\n"
        "🛒 /additem - Добавить элемент в список покупок\n"
        "🛍️ /viewitems - Посмотреть список покупок\n"
        "❌ /removeitem - Удалить элемент из списка покупок\n"
        "🎯 /addgoal - Добавить совместную цель\n"
        "🏆 /goals - Посмотреть список целей\n"
        "📅 /setdate - Добавить памятную дату\n"
        "🗓️ /dates - Просмотреть памятные даты\n"
        "🧩 /riddle - Получить загадку\n"
        "🎉 /challenge - Получить челлендж\n"
        "💬 Общий чат работает автоматически: просто отправьте сообщение."
    )

# Общий чат: обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    message = update.message.text
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if not is_allowed(user_id):
        await update.message.reply_text("❌ Вы не авторизованы для использования этого бота.")
        return

    # Сохранение сообщения в базе данных
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat (user, message, timestamp) VALUES (?, ?, ?)", (user_name, message, timestamp))
    conn.commit()
    conn.close()

    # Отправка сообщения всем пользователям
    for user in ALLOWED_USERS:
        if user != user_id:
            try:
                await context.bot.send_message(chat_id=user, text=f"💬 {user_name}: {message}")
            except Exception as e:
                logging.error(f"Ошибка отправки сообщения пользователю {user}: {e}")

# Команда /riddle
async def riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    riddle = random.choice(riddles)
    current_riddles[user_id] = riddle
    await update.message.reply_text(f"🧩 Загадка: {riddle['question']}\nНапишите ваш ответ!")

# Проверка ответа на загадку
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in current_riddles:
        riddle = current_riddles[user_id]
        user_answer = update.message.text.strip().lower()
        if user_answer == riddle['answer']:
            await update.message.reply_text("🎉 Правильно!")
            del current_riddles[user_id]
        else:
            await update.message.reply_text("❌ Неправильно. Попробуйте ещё раз.")
    else:
        await update.message.reply_text("❓ У вас ещё нет загадки. Используйте /riddle, чтобы получить новую.")

# Команда /challenge
async def challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    challenge = random.choice(challenges)
    await update.message.reply_text(f"🎉 Ваш челлендж: {challenge}")

# Основная функция запуска бота
def main():
    init_db()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("Токен бота не найден. Убедитесь, что он указан в файле .env")

    app = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("riddle", riddle))
    app.add_handler(CommandHandler("challenge", challenge))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    logging.info("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
