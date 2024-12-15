from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.handlers import (
    start,
    help_command,
    rule_command,
    player_message,
    handle_action_callback,
    handle_end_meeting_vote,
)
from bot.controller import end_game
from bot.utils import prompt_action
from config.secrets import TOKEN
from game.game import Game

def main():
    # Ініціалізуємо додаток
    application = ApplicationBuilder().token(TOKEN).post_init(lambda app: app.job_queue.start()).build()

    # Ініціалізуємо гру і додаємо її до bot_data
    game = Game()
    application.bot_data["game"] = game

    # Реєстрація обробників
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("rule", rule_command))
    application.add_handler(CommandHandler("end_game", end_game))

    application.add_handler(CommandHandler("action", prompt_action))
    application.add_handler(CallbackQueryHandler(handle_action_callback, pattern=r"^\d$"))


    # Наради
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, player_message))
    application.add_handler(CallbackQueryHandler(handle_end_meeting_vote, pattern="end_meeting_vote"))
    

    # Запуск polling
    application.run_polling()

if __name__ == "__main__":
    main()
