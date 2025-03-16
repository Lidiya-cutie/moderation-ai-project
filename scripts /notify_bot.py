import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

BOT_TOKEN = "YOUR_BOT_TOKEN"
USER_ID = 1631375063

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

def send_notification(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": USER_ID, "text": message}
        response = requests.post(url, json=data)

        if response.status_code == 200:
            logger.info("Уведомление отправлено успешно.")
        else:
            logger.error(f"Ошибка при отправке уведомления: {response.text}")
    except Exception as e:
        logger.error(f"Исключение при отправке уведомления: {e}")


async def start(update: Update, context):
    user_id = update.effective_user.id  
    first_name = update.effective_user.first_name 

    await update.message.reply_text(
        f"Привет, {first_name}! Ваш Telegram User ID: {user_id}\n"
        "Бот готов уведомлять о завершении задач."
    )
    logger.info(f"Команда /start от пользователя: ID={user_id}, Имя={first_name}")


# Функция для обработки команды /notify (тест уведомления)
async def notify_task_complete(update: Update, context):
    await update.message.reply_text("Отправляю уведомление...")
    send_notification("Задача завершена! Вы можете проверить результаты.")
    await update.message.reply_text("Уведомление отправлено!")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("notify", notify_task_complete))  # Тестовая команда

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Если скрипт вызван с аргументами, отправить уведомление
        send_notification(" ".join(sys.argv[1:]))
    else:
        # Иначе запускаем Telegram-бот
        print("Бот запущен!")
        app.run_polling()
