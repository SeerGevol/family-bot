from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import sqlite3
import random
from dotenv import load_dotenv
import os
from datetime import datetime
import logging

# Загрузка переменных окружения
load_dotenv()

# Укажите Telegram ID пользователей
ALLOWED_USERS = [7666108269, 1278614067]  # Добавьте свои ID

# Инициализация логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Список загадок
riddles = [
    {"question": "Что можно приготовить, но нельзя съесть?", "answer": "уроки"},
    {"question": "Кто говорит на всех языках?", "answer": "эхо"},
    {"question": "Что поднимается, но никогда не опускается?", "answer": "возраст"},
    {"question": "Что становится мокрым во время сушки?", "answer": "полотенце"},
    {"question": "Что нельзя съесть на завтрак?", "answer": "обед и ужин"},
    {"question": "У чего нет начала, конца и середины?", "answer": "кольцо"},
    {"question": "Что всегда растет, но никогда не уменьшается?", "answer": "возраст"},
    {"question": "Висит груша — нельзя скушать. Что это?", "answer": "лампочка"},
    {"question": "Какая птица самая умная?", "answer": "сова"}
]

# Список челленджей
challenges = [
    "💌 Напишите благодарственное письмо другу или партнеру.",
    "🎵 Составьте плейлист ваших любимых песен.",
    "📸 Найдите и поделитесь вашим любимым снимком.",
    "🎯 Поставьте цель на неделю и поделитесь результатами.",
    "💡 Изучите новый навык или интересный факт.",
    "🍴 Приготовьте новое блюдо и поделитесь впечатлениями.",
    "📖 Прочитайте главу новой книги и обсудите с кем-то.",
    "🎥 Посмотрите фильм, который вы давно откладывали.",
    "📸 Поделитесь своей любимой фотографией из вашего общего прошлого.",
    "🎁 Сделайте небольшой сюрприз: закажите доставку еды для партнёра.",
    "🍴 Устройте онлайн-ужин, приготовив один и тот же рецепт.",
    "🎵 Создайте плейлист из песен, которые ассоциируются с вашими отношениями.",
    "🌟 Обсудите, как вы видите себя через 5 лет вместе.",
    "🎯 Создайте виртуальную доску мечтаний с совместными целями.",
    "📖 Прочитайте одну и ту же книгу и обсудите её.",
    "📝 Напишите список из 10 вещей, которые вам нравятся в партнёре.",
    "🎥 Посмотрите вместе фильм, связавшись по видеозвонку.",
    "📞 Устройте звонок и обсудите свои мечты и планы.",
    "🎨 Нарисуйте что-нибудь вместе и обменяйтесь результатами.",
    "🍹 Приготовьте коктейль или кофе по одному рецепту и выпейте вместе.",
    "📚 Обсудите ваши любимые фильмы, книги или сериалы.",
    "💡 Обсудите, что бы вы хотели изменить в своём будущем."
]

# Текущие загадки пользователей
current_riddles = {}

# Функция проверки пользователя
def is_allowed(user_id):
    return user_id in ALLOWED_USERS

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS gratitude (id INTEGER PRIMARY KEY, user TEXT, message TEXT, timestamp TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS dates (id INTEGER PRIMARY KEY, date TEXT, description TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS list_items (id INTEGER PRIMARY KEY, item TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY, goal TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS chat (id INTEGER PRIMARY KEY, user TEXT, message TEXT, timestamp TEXT)")
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

    # Проверка авторизации
    if not is_allowed(user_id):
        await update.message.reply_text("❌ Вы не авторизованы для использования этого бота.")
        return

    # Сохранение сообщения в базу данных
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat (user, message, timestamp) VALUES (?, ?, ?)", (user_name, message, timestamp))
    conn.commit()
    conn.close()

    # Отправка сообщения всем пользователям
    for user in ALLOWED_USERS:
        if user != user_id:  # Исключить отправителя
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

# Основная функция
def main():
    init_db()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("Токен не найден!")

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
