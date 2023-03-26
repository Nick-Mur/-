import logging
#import telegram.ext

from config import bot_token, bot_name
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
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

CHOOSING, TYPING_REPLY = range(2)


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
    button_list = [["Help", "Game"], ["Cancel"]]

    await update.message.reply_html(
        f"Привет {user.mention_html()}! \
Я {bot_name}. Напиши мне что-нибудь, и я пришлю это назад!",
        reply_markup=ReplyKeyboardMarkup(
            build_menu(button_list),
            one_time_keyboard=True,
            input_field_placeholder='What are we do?'
        )
    )
    return 0


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет помощь по команде /help"""
    await update.message.reply_text(
        "Я пока не умею помогать... Я только твоё эхо."
    )


async def unknown(update: Update,
                  context: ContextTypes.DEFAULT_TYPE):
    """Неизвестные комманды"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Прости, я не понимаю, что ты хочешь(."
    )


async def cancel(update: Update,
                 context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Пока-пока! Надеюсь, ещё увидимся!", reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


async def game_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Запрос информации о выбранном предопределенном выборе."""
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Ты выбрал {text.lower()}? Я работаю над этим)!")


def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(bot_token).build()
    # extbot = telegram.ext.ExtBot(token=bot_token)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^(Help)$"), help_command
                ),
                MessageHandler(
                    filters.Regex("^(Game)$"), game_choice
                ),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel),
                   MessageHandler(filters.Regex("^(Cancel)$"), cancel)]
    )

    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling()


if __name__ == "__main__":
    main()
