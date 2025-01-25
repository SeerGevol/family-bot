from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import sqlite3
import random
from dotenv import load_dotenv
import os
from datetime import datetime

# Загрузка переменных окружения из файла .env
load_dotenv()

# Укажите Telegram ID пользователей, которые могут пользоваться ботом
ALLOWED_USERS = [7666108269, 1278614067]

def is_allowed(user_id):
    """Проверяет, является ли пользователь авторизованным."""
    return user_id in ALLOWED_USERS

# Инициализация базы данных
def init_db():
    """Создает таблицы в базе данных, если они не существуют."""
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS gratitude (id INTEGER PRIMARY KEY, user TEXT, message TEXT, timestamp TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS dates (id INTEGER PRIMARY KEY, date TEXT, description TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS emotions (id INTEGER PRIMARY KEY, user TEXT, mood TEXT, timestamp TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS list_items (id INTEGER PRIMARY KEY, item TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY, goal TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS photos (id INTEGER PRIMARY KEY, user TEXT, file_id TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("❌ Извините, вы не авторизованы для использования этого бота.")
        return

    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("✨ Добавить благодарность", callback_data="gratitude")],
        [InlineKeyboardButton("📸 Просмотреть фотоальбом", callback_data="view_album")],
        [InlineKeyboardButton("🎯 Получить челлендж", callback_data="challenge")],
        [InlineKeyboardButton("🧩 Получить загадку", callback_data="riddle")],
        [InlineKeyboardButton("📅 Памятные даты", callback_data="dates")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 Привет, *{user.first_name}*!\n"
        "Я _Family Bot_ — ваш личный помощник. Вот что я могу для вас сделать:\n\n"
        "✨ /gratitude - Добавить благодарность\n"
        "📖 /viewgratitudes - Просмотреть благодарности\n"
        "🛒 /additem - Добавить элемент в список покупок\n"
        "🛍️ /viewitems - Посмотреть список покупок\n"
        "❌ /removeitem - Удалить элемент из списка покупок\n"
        "🎯 /addgoal - Добавить совместную цель\n"
        "🏆 /goals - Посмотреть список целей\n"
        "📅 /setdate - Добавить памятную дату\n"
        "🗓️ /dates - Просмотреть памятные даты\n"
        "📸 /addphoto - Сохранить фото в альбом\n"
        "🎥 /viewalbum - Просмотреть весь альбом\n"
        "🕒 /morning - Утреннее сообщение\n"
        "🌙 /evening - Вечернее сообщение\n"
        "😊 /mood - Поделиться настроением\n"
        "🧩 /riddle - Получить загадку\n"
        "🎉 /challenge - Получить челлендж\n\n"
        "💡 Используйте команды для взаимодействия со мной!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Команда /morning
async def morning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Доброе утро моя любовь! ☀️ Пусть твой день начнется с улыбки!")

# Команда /evening
async def evening(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Сладких снов! 🌙 Время расслабиться и отдохнуть, завтра новый день.")

# Команда /mood
async def mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Пожалуйста, укажите ваше настроение. Пример: /mood Счастливый.")
        return

    mood_text = " ".join(context.args)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emotions (user, mood, timestamp) VALUES (?, ?, ?)",
                   (update.effective_user.username, mood_text, timestamp))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"😊 Ваше настроение сохранено: {mood_text}")

# Команда /setdate
async def setdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("❗ Пожалуйста, укажите дату и описание. Пример: /setdate 2023-01-01 Новый год")
        return

    date = context.args[0]
    description = " ".join(context.args[1:])
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dates (date, description) VALUES (?, ?)", (date, description))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"📅 Дата сохранена: {date} - {description}")

# Команда /addphoto
async def addphoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("❗ Пожалуйста, отправьте фото вместе с командой.")
        return

    photo_file = update.message.photo[-1].file_id
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO photos (user, file_id, timestamp) VALUES (?, ?, ?)",
                   (update.effective_user.username, photo_file, timestamp))
    conn.commit()
    conn.close()

    await update.message.reply_text("📸 Фото успешно добавлено в альбом!")

# Команда /viewalbum
async def viewalbum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM photos")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        await update.message.reply_text("🎥 Ваш фотоальбом пока пуст.")
        return

    for row in rows:
        await update.message.bot.send_photo(chat_id=update.effective_chat.id, photo=row[0])

# Обработчик /riddle
async def riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    riddles =[ 
        {"question": "Что всегда растет, но никогда не уменьшается?", "answer": "Возраст"},
        {"question": "Что можно разбить, не касаясь?", "answer": "Обещание"},
        {"question": "Какое место на Земле ближе всего к небу?", "answer": "Гора"},
        {"question": "Что нельзя съесть на завтрак?", "answer": "Обед и ужин"},
        {"question": "У чего нет начала, конца и середины?", "answer": "Кольцо"},
        {"question": "Что всегда растет, но никогда не уменьшается?", "answer": "Возраст"},
        {"question": "Висит груша — нельзя скушать. Что это?", "answer": "Лампочка"},
        {"question": "Какая птица самая умная?", "answer": "Сова"}
    ]
    selected_riddle = random.choice(riddles)
    context.user_data['riddle'] = selected_riddle
    await update.message.reply_text(f"🧩 Загадка: {selected_riddle['question']}")

# Команда /challenge
async def challenge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    challenges = [
        "💌 Напишите благодарственное письмо другу.",
        "📸 Сделайте фотографию на прогулке.",
        "🍴 Приготовьте новое блюдо.",
        "📚 Прочитайте одну главу книги.",
        "🏃 Пройдите 10 000 шагов.",
        "🎵 Составьте плейлист ваших любимых песен.",
        "📸 Найдите и поделитесь вашим любимым снимком.",
        "🎯 Поставьте цель на неделю и поделитесь результатами.",
        "💡 Изучите новый навык или интересный факт.",
        "🍴 Приготовьте новое блюдо и поделитесь впечатлениями.",
        "📖 Прочитайте главу новой книги и обсудите с кем-то.",
        "🎥 Посмотрите фильм, который вы давно откладывали."
    ]
    challenge = random.choice(challenges)
    await update.message.reply_text(f"🎉 Ваш челлендж: {challenge}")

# Основная функция
def main():
    init_db()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("Токен не найден!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("morning", morning))
    app.add_handler(CommandHandler("evening", evening))
    app.add_handler(CommandHandler("mood", mood))
    app.add_handler(CommandHandler("setdate", setdate))
    app.add_handler(CommandHandler("addphoto", addphoto))
    app.add_handler(CommandHandler("viewalbum", viewalbum))
    app.add_handler(CommandHandler("riddle", riddle))
    app.add_handler(CommandHandler("challenge", challenge_command))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
