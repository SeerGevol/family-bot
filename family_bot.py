from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import sqlite3
import random
import os
from datetime import datetime

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

# Челленджи
async def challenge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет случайный челлендж."""
    challenges = [
        "💌 Напишите друг другу длинное сообщение о том, за что вы благодарны в отношениях.",
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
    challenge = random.choice(challenges)
    await update.message.reply_text(f"🎉 Ваш челлендж: {challenge}")

# Основная функция
def main():
    """Запускает приложение Telegram бота."""
    init_db()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("Токен не найден! Убедитесь, что BOT_TOKEN указан в переменных окружения.")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("challenge", challenge_command))
    app.run_polling()

if __name__ == "__main__":
    main()
