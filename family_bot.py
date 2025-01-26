from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import sqlite3
import random
from dotenv import load_dotenv
import os
from datetime import datetime

# Загрузка переменных окружения из файла .env
load_dotenv()

# Укажите Telegram ID пользователей, которые могут пользоваться ботом
ALLOWED_USERS = [7666108269, 1278614067]  # Укажите ваши ID

# Список загадок с ответами
riddles = [
    {"question": "Что можно приготовить, но нельзя съесть?", "answer": "уроки"},
    {"question": "Кто говорит на всех языках?", "answer": "эхо"},
    {"question": "Что поднимается, но никогда не опускается?", "answer": "возраст"},
    {"question": "Что становится мокрым во время сушки?", "answer": "полотенце"},
    {"question": "Что нельзя съесть на завтрак?", "answer": "Обед и ужин"},
    {"question": "У чего нет начала, конца и середины?", "answer": "Кольцо"},
    {"question": "Что всегда растет, но никогда не уменьшается?", "answer": "Возраст"},
    {"question": "Висит груша — нельзя скушать. Что это?", "answer": "Лампочка"},
    {"question": "Какая птица самая умная?", "answer": "Сова"}
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

# Хранение текущей загадки для пользователей
current_riddles = {}

def is_allowed(user_id):
    """Проверяет, является ли пользователь авторизованным."""
    return user_id in ALLOWED_USERS

def init_db():
    """Создает таблицы в базе данных, если они не существуют."""
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS gratitude (id INTEGER PRIMARY KEY, user TEXT, message TEXT, timestamp TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS dates (id INTEGER PRIMARY KEY, date TEXT, description TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS list_items (id INTEGER PRIMARY KEY, item TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS goals (id INTEGER PRIMARY KEY, goal TEXT)")
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
    )

# Команда /riddle
async def riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет случайную загадку."""
    user_id = update.effective_user.id
    riddle = random.choice(riddles)
    current_riddles[user_id] = riddle  # Сохраняем загадку для пользователя
    await update.message.reply_text(f"🧩 Загадка: {riddle['question']}\nНапишите ваш ответ!")

# Проверка ответа на загадку
async def handle_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in current_riddles:
        riddle = current_riddles[user_id]
        user_answer = update.message.text.strip().lower()
        if user_answer == riddle['answer']:
            await update.message.reply_text("🎉 Правильно! Отличная работа!")
            del current_riddles[user_id]  # Удаляем загадку после правильного ответа
        else:
            await update.message.reply_text("❌ Неправильно. Попробуйте ещё раз.")
    else:
        await update.message.reply_text("❓ У вас ещё нет загадки. Используйте /riddle, чтобы получить новую.")

# Команда /challenge
async def challenge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет случайный челлендж."""
    challenge = random.choice(challenges)
    await update.message.reply_text(f"🎉 Ваш челлендж: {challenge}")

# Команда /gratitude
async def gratitude(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сохраняет благодарность в базу данных."""
    user = update.effective_user.first_name
    message = ' '.join(context.args)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not message:
        await update.message.reply_text("❌ Пожалуйста, укажите за что вы благодарны.")
        return
    
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gratitude (user, message, timestamp) VALUES (?, ?, ?)", (user, message, timestamp))
    conn.commit()
    conn.close()
    
    await update.message.reply_text("✨ Благодарность добавлена!")

# Команда /viewgratitudes
async def view_gratitudes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отображает список благодарностей."""
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user, message, timestamp FROM gratitude")
    gratitudes = cursor.fetchall()
    conn.close()
    
    if gratitudes:
        gratitude_texts = [f"📅 {g[2]} - {g[0]}: {g[1]}" for g in gratitudes]
        await update.message.reply_text("\n".join(gratitude_texts))
    else:
        await update.message.reply_text("Список благодарностей пока пуст.")

# Команда /additem
async def additem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет элемент в список покупок."""
    item = ' '.join(context.args)
    if not item:
        await update.message.reply_text("❌ Укажите, что вы хотите добавить в список.")
        return

    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO list_items (item) VALUES (?)", (item,))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"🛒 '{item}' добавлено в список покупок!")

# Команда /viewitems
async def viewitems(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отображает список покупок."""
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT item FROM list_items")
    items = cursor.fetchall()
    conn.close()

    if items:
        item_list = [f"🛒 {item[0]}" for item in items]
        await update.message.reply_text("\n".join(item_list))
    else:
        await update.message.reply_text("Список покупок пока пуст.")

# Команда /removeitem
async def removeitem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Удаляет элемент из списка покупок."""
    item = ' '.join(context.args)
    if not item:
        await update.message.reply_text("❌ Укажите, что вы хотите удалить из списка.")
        return

    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM list_items WHERE item = ?", (item,))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"🛒 '{item}' удалено из списка покупок!")

# Команда /setdate
async def setdate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Добавляет памятную дату в базу данных."""
    date = context.args[0]
    description = ' '.join(context.args[1:])
    
    if not date or not description:
        await update.message.reply_text("❌ Пожалуйста, укажите дату и описание.")
        return
    
    conn = sqlite3.connect("family_bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dates (date, description) VALUES (?, ?)", (date, description))
    conn.commit()
    conn.close()
    
    await update.message.reply_text("📅 Памятная дата добавлена!")

# Основная функция
def main():
    init_db()
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("Токен не найден!")

    app = Application.builder().token(BOT_TOKEN).build()

    # Регистрация всех команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("riddle", riddle))
    app.add_handler(CommandHandler("challenge", challenge))
    app.add_handler(CommandHandler("gratitude", gratitude))
    app.add_handler(CommandHandler("viewgratitudes", view_gratitudes))
    app.add_handler(CommandHandler("additem", additem))
    app.add_handler(CommandHandler("viewitems", viewitems))
    app.add_handler(CommandHandler("removeitem", removeitem))
    app.add_handler(CommandHandler("setdate", setdate))  # Новая команда
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_answer))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
