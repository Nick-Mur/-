import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import bot_token


# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def echo(update, context):
    await update.message.reply_text(
        update.message.text if update.message.text[0] != '/' else 'неизвестная команда')


async def start(update, context):
    """Отправляет сообщение когда получена команда /start"""
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я {}. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def help_command(update, context):
    """Отправляет сообщение когда получена команда /help"""
    await update.message.reply_text("Я пока не умею помогать... Я только ваше эхо.")


def main():
    application = Application.builder().token(bot_token).build()
    text_handler = MessageHandler(filters.TEXT, echo)
    bot_name = application.bot.get_me()
    print(bot_name)


    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(text_handler)


    application.run_polling()


if __name__ == '__main__':
    main()
