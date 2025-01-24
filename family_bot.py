from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, filters
from datetime import datetime
import sqlite3
import random

ALLOWED_USERS = [7666108269, 1278614067]

def is_allowed(user_id):
    return user_id in ALLOWED_USERS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("Извините, вы не авторизованы для использования этого бота.")
        return

    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! 👋\n"
        "Я Family, ваш личный бот. Вот что я могу:\n"
        "/todo - Список задач\n"
        "/memory - Сохранение воспоминаний\n"
        "/challenge - Генерация челленджей\n"
        "/addgoal - Добавить совместную цель\n"
        "/goals - Посмотреть список целей\n"
        "/setdate - Добавить важную дату\n"
        "/dates - Просмотреть памятные даты\n"
        "/help - Посмотреть команды\n"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("Извините, вы не авторизованы для использования этого бота.")
        return

    await update.message.reply_text(
        "Вот доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/todo - Добавить задачу или посмотреть список\n"
        "/memory - Добавить или просмотреть воспоминания\n"
        "/challenge - Генерация челленджей\n"
        "/addgoal - Добавить совместную цель\n"
        "/goals - Посмотреть список целей\n"
        "/setdate - Добавить важную дату\n"
        "/dates - Просмотреть памятные даты\n"
    )

async def challenge_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    challenges = [
        "Напишите друг другу длинное сообщение о том, за что вы благодарны в отношениях.",
        "Поделитесь своей любимой фотографией из вашего общего прошлого.",
        "Запишите короткое голосовое сообщение с признанием в любви и отправьте его партнёру.",
        "Сделайте небольшой сюрприз: закажите доставку еды или чего-то приятного для партнёра.",
        "Устройте онлайн-вечер: выберите фильм или сериал и посмотрите его вместе, созвонившись в видео-чате.",
        "Поделитесь своей мечтой или целью, о которой ещё не рассказывали.",
        "Напишите друг другу 5 вещей, которые вы любите в партнёре.",
        "Сделайте плейлист из песен, которые ассоциируются с вашими отношениями, и поделитесь им.",
        "В течение дня отправьте партнёру 3 случайных сообщения с приятными словами.",
        "Обсудите, куда вы хотите отправиться в ваш следующий совместный отпуск, и начните планировать поездку.",
        "Напишите друг другу письмо от руки, сфотографируйте его и отправьте партнёру.",
        "Создайте вместе список фильмов или сериалов, которые хотите посмотреть, и начните с первого пункта.",
        "Составьте список целей на год, которые вы хотите достичь вместе."
    ]
    challenge = random.choice(challenges)
    await update.message.reply_text(f"Ваш челлендж: {challenge}")

async def add_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("Извините, вы не авторизованы для использования этого бота.")
        return

    if not context.args:
        await update.message.reply_text("Пожалуйста, добавьте цель после команды, например: /addgoal Съездить в Париж")
        return

    goal = " ".join(context.args)
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY, goal TEXT)")
    cursor.execute("INSERT INTO goals (goal) VALUES (?)", (goal,))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Цель \"{goal}\" добавлена в список!")

async def goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("Извините, вы не авторизованы для использования этого бота.")
        return

    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY, goal TEXT)")
    cursor.execute("SELECT goal FROM goals")
    goals = cursor.fetchall()
    conn.close()

    if goals:
        goals_list = "\n".join([f"- {goal[0]}" for goal in goals])
        await update.message.reply_text(f"Ваши цели:\n{goals_list}")
    else:
        await update.message.reply_text("Список целей пуст.")

async def set_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("Извините, вы не авторизованы для использования этого бота.")
        return

    if len(context.args) < 2:
        await update.message.reply_text("Пожалуйста, используйте формат: /setdate Дата Описание (например: /setdate 2025-01-01 Годовщина)")
        return

    date = context.args[0]
    description = " ".join(context.args[1:])
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS dates (id INTEGER PRIMARY KEY, date TEXT, description TEXT)")
    cursor.execute("INSERT INTO dates (date, description) VALUES (?, ?)", (date, description))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"Дата \"{description}\" на {date} добавлена!")

async def dates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_allowed(user_id):
        await update.message.reply_text("Извините, вы не авторизованы для использования этого бота.")
        return

    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS dates (id INTEGER PRIMARY KEY, date TEXT, description TEXT)")
    cursor.execute("SELECT date, description FROM dates ORDER BY date")
    dates = cursor.fetchall()
    conn.close()

    if dates:
        dates_list = "\n".join([f"{date[0]} - {date[1]}" for date in dates])
        await update.message.reply_text(f"Ваши памятные даты:\n{dates_list}")
    else:
        await update.message.reply_text("Список памятных дат пуст.")

def main():
    app = Application.builder().token("7916153118:AAGFNBgZ6u9IFeooVqpW_NgAACxIfNJyz1Y").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("challenge", challenge_command))
    app.add_handler(CommandHandler("addgoal", add_goal))
    app.add_handler(CommandHandler("goals", goals))
    app.add_handler(CommandHandler("setdate", set_date))
    app.add_handler(CommandHandler("dates", dates))
    app.run_polling()

if __name__ == "__main__":
    main()
