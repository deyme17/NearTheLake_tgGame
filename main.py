from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters
from bot.handlers import start, enter_name, help_command, rule_command
from config.secrets import TOKEN

def main():
    application = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            0: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_name)],
        },
        fallbacks=[],
    )

    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('rule', rule_command))
    application.add_handler(conv_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
