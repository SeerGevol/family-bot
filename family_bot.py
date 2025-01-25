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
        [InlineKeyboardButton("📅 Памятные даты", callback_data="dates")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 Привет, *{user.first_name}*!\n"
        "Я _Family Bot_ — ваш личный помощник. Вот что я могу для вас сделать:\n\n"
        "📌 *Основные команды:*\n"
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
        "💡 Используйте команды для взаимодействия с ботом!",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выводит список доступных команд."""
    await update.message.reply_text(
        "📋 *Список доступных команд:*\n"
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
        "💡 Используйте команды для взаимодействия с ботом!",
        parse_mode="Markdown"
    )

# Заглушки для всех команд
async def gratitude(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет благодарность."""
    await update.message.reply_text("Спасибо за вашу благодарность!")

async def view_gratitudes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Список благодарностей пока пуст.")

async def additem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добавлено в список покупок.")

async def viewitems(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ваш список покупок пуст.")

async def removeitem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Элемент удалён из списка покупок.")

async def addgoal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Цель добавлена.")

async def goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ваши цели.")

async def setdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Дата добавлена.")

async def dates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ваши памятные даты.")

async def addphoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Фото добавлено в альбом.")

async def viewalbum(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ваш фотоальбом.")

async def morning(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Доброе утро!")

async def evening(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Добрый вечер!")

async def mood(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ваше настроение сохранено.")

async def riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Загадка дня!")

async def challenge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    challenges = ["Челлендж 1", "Челлендж 2"]
    challenge = random.choice(challenges)
    await update.message.reply_text(f"Ваш челлендж: {challenge}")

# Основная функция
def main():
    init_db()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("Токен не найден!")

    app = Application.builder().token(BOT_TOKEN).build()

    # Регистрация всех команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("gratitude", gratitude))
    app.add_handler(CommandHandler("viewgratitudes", view_gratitudes))
    app.add_handler(CommandHandler("additem", additem))
    app.add_handler(CommandHandler("viewitems", viewitems))
    app.add_handler(CommandHandler("removeitem", removeitem))
    app.add_handler(CommandHandler("addgoal", addgoal))
    app.add_handler(CommandHandler("goals", goals))
    app.add_handler(CommandHandler("setdate", setdate))
    app.add_handler(CommandHandler("dates", dates))
    app.add_handler(CommandHandler("addphoto", addphoto))
    app.add_handler(CommandHandler("viewalbum", viewalbum))
    app.add_handler(CommandHandler("morning", morning))
    app.add_handler(CommandHandler("evening", evening))
    app.add_handler(CommandHandler("mood", mood))
    app.add_handler(CommandHandler("riddle", riddle))
    app.add_handler(CommandHandler("challenge", challenge_command))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
