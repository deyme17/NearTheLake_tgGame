from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters
from bot.handlers import start, help_command, rule_command
from bot.controller import start_game, end_game
from config.secrets import TOKEN


def main():
    application = ApplicationBuilder().token(TOKEN).build()

    # Реєстрація обробників
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={},
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("rule", rule_command))
    application.add_handler(CommandHandler("start_game", start_game))
    application.add_handler(CommandHandler("end_game", end_game))

    application.run_polling()


if __name__ == "__main__":
    main()
