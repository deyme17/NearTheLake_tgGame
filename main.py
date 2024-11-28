from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from bot.handlers import (
    start,
    help_command,
    rule_command,
    start_meeting,
    player_message,
    end_meeting,
    handle_action_callback,
)
from bot.controller import start_game, end_game
from bot.utils import prompt_action
from config.secrets import TOKEN
from game.game import Game  # Імпортуємо клас Game


def main():
    # Ініціалізуємо додаток
    application = ApplicationBuilder().token(TOKEN).build()

    # Ініціалізуємо гру і додаємо її до bot_data
    game = Game()
    application.bot_data["game"] = game

    # Реєстрація обробників
    application.add_handler(CommandHandler("start", start))  # Початок роботи бота
    application.add_handler(CommandHandler("help", help_command))  # Допомога
    application.add_handler(CommandHandler("rule", rule_command))  # Правила гри
    application.add_handler(CommandHandler("start_game", start_game))  # Запуск гри
    application.add_handler(CommandHandler("end_game", end_game))  # Завершення гри

    application.add_handler(CommandHandler("action", prompt_action))  # Команда для вибору дії
    application.add_handler(CallbackQueryHandler(handle_action_callback))  # Обробка кнопок

    # Наради
    application.add_handler(CommandHandler("start_meeting", start_meeting))
    application.add_handler(CommandHandler("end_meeting", end_meeting))
    application.add_handler(CallbackQueryHandler(handle_action_callback))  # Обробка вибору кнопок
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, player_message))  # Повідомлення під час нарад

    # Вибір дій гравців через кнопки
    application.add_handler(CommandHandler("action", prompt_action))  # Вибір дії через кнопки

    # Запускаємо бота
    application.run_polling()


if __name__ == "__main__":
    main()
