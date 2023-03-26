import logging

import telegram.ext

from config import bot_token, bot_name
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
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


def build_menu(menu_list):
    keybord = []
    for rows in range(len(menu_list)):
        keybord.append([])
        for cols in menu_list[rows]:
            keybord[rows].append(KeyboardButton(cols))
    return keybord


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправлят сообщение по команде /start"""
    user = update.effective_user
    await update.message.reply_html(
        f"Привет {user.mention_html()}! \
Я {bot_name}. Напиши мне что-нибудь, и я пришлю это назад!",
    )

    button_list = [["col1", "col2"], ["row2"]]
    reply_markup = ReplyKeyboardMarkup(build_menu(button_list))
    await update.message.reply_text(text="Добавлено меню возможностей)", reply_markup=reply_markup)


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет помощь по команде /help"""
    await update.message.reply_text(
        "Я пока не умею помогать... Я только твоё эхо."
    )


async def echo(update: Update,
               context: ContextTypes.DEFAULT_TYPE) -> None:
    """Эхо пользователя"""
    await update.message.reply_text(
        update.message.text
    )


async def unknown(update: Update,
                  context: ContextTypes.DEFAULT_TYPE):
    '''Неизвестные комманды'''
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Прости, я не понимаю, что ты хочешь(."
    )


def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(bot_token).build()
    extbot = telegram.ext.ExtBot(token=bot_token)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_handler(MessageHandler(filters.TEXT, echo))

    application.run_polling()


if __name__ == "__main__":
    main()
