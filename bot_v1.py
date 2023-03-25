import logging

import telegram.ext

from config import bot_token, bot_name
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued"""
    user = update.effective_user
    await update.message.reply_html(
        f"Привет {user.mention_html()}! \
Я {bot_name}. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued"""
    await update.message.reply_text(
        "Я пока не умею помогать... Я только ваше эхо."
    )


async def echo(update: Update,
               context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message"""
    await update.message.reply_text(
        update.message.text if update.message.text[0] != '/' else 'неизвестная команда'
    )


def main() -> None:
    """Start the bot"""

    application = Application.builder().token(bot_token).build()
    # extbot = telegram.ext.ExtBot(token=bot_token)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(MessageHandler(filters.TEXT, echo))

    application.run_polling()


if __name__ == "__main__":
    main()