import logging
from data.config import bot_token, bot_name
from telegram import (
    Update,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
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

CHOOSING, CHOOSING_GAME, MONOPOLY = range(3)


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
    button_list = [["Talk", "Games"],
                   ["Help"],
                   ["Exit"]]

    await update.message.reply_html(
        f"Привет {user.mention_html()}! \
Я {bot_name}. Я только учусь, поэтому не будь со мной жесток!",
        reply_markup=ReplyKeyboardMarkup(
            build_menu(button_list),
            one_time_keyboard=True,
            input_field_placeholder='What are we do?'
        )
    )
    return CHOOSING


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет помощь по команде /help"""
    await update.message.reply_text(
        "Я пока ничего не умею, но в скором времени..."
    )


async def unknown(update: Update,
                  context: ContextTypes.DEFAULT_TYPE):
    """Неизвестные комманды"""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Прости, я не понимаю, что ты хочешь(."
    )


async def exit_from_bot(update: Update,
                        context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    button_list = [['Start']]
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Пока-пока! Надеюсь, ещё увидимся!"
        " Для повторного обращения ко мне напишите /start",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


async def game_choice(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> int:
    """Запрос информации о выбранном предопределенном выборе."""
    text = update.message.text
    context.user_data["choice"] = text
    button_list = [["Monopoly"],
                   ["Exit"]]
    await update.message.reply_text(
        f"Ты хочешь окунуться в {text.lower()}? Я не очень хорош в играх)!",
        reply_markup=ReplyKeyboardMarkup(
            build_menu(button_list),
            one_time_keyboard=True,
            input_field_placeholder='What are we do?'
        )
    )
    return CHOOSING_GAME


async def info_monopoly(update: Update,
                      context: ContextTypes.DEFAULT_TYPE) -> int:
    button_list = [["Начать монополию"],
                   ["Exit"]]
    await update.message.reply_text(
        "Монополия пока доступна только для 2-ух человек. "
        "Чтобы в неё сыграть, оба игрока должны иметь чат со мной. "
        "Дальше один должен создать лобби, ввести ID 2-ого игрока "
        "и ждать подтверждения на игру. Каждый игрок может "
        "принудительно окончить игру.\nВы готовы начать?",
        reply_markup=ReplyKeyboardMarkup(
            build_menu(button_list),
            one_time_keyboard=True,
            input_field_placeholder="Let's go?"
        )
    )
    return MONOPOLY


async def play_monopoly(update: Update,
                      context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Ожидание релиза')


async def talk_with_ai(update: Update,
                      context: ContextTypes.DEFAULT_TYPE):
    """Тут
    будет
    подключение у давинчи
    чата GPT"""
    await update.message.reply_html(
        f"{update.effective_user.mention_html()}, "
        f"извини, но я пока не умею говорить(",
    )


def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(bot_token).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start" or "^(Start)$", start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex("^(Talk)$"), talk_with_ai
                ),
                MessageHandler(
                    filters.Regex("^(Games)$"), game_choice
                ),
                MessageHandler(
                    filters.Regex("^(Help)$"), help_command
                ),
            ],
            CHOOSING_GAME: [
                MessageHandler(
                    filters.Regex("^(Monopoly)$"), info_monopoly
                ),
            ],
            MONOPOLY: [
                MessageHandler(
                    filters.Regex("^(Начать монополию)$"), play_monopoly
                ),
            ]
        },
        fallbacks=[CommandHandler("exit", exit_from_bot),
                   MessageHandler(filters.Regex("^(Exit)$"), exit_from_bot)],
        allow_reentry=True
    )

    application.add_handler(conv_handler)

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))

    application.run_polling()


if __name__ == "__main__":
    main()
