from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.handlers.command_handlers import start, help_command, rule_command, end_game_command, start_game_command
from bot.handlers.action_handlers import handle_action_callback
from bot.handlers.meeting_handlers import handle_end_meeting_vote
from bot.handlers.message_handlers import handle_player_message
from bot.ui_components.promt_action import prompt_action
from bot.handlers.settings_handlers import handle_settings_callback

from config.secrets import TOKEN
from game.core.models.game import Game

def create_app():
    application = ApplicationBuilder() \
        .token(TOKEN) \
        .post_init(lambda app: app.job_queue.start()) \
        .build()

    application.bot_data["game"] = Game()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("rule", rule_command))
    application.add_handler(CommandHandler("start_game", start_game_command))
    application.add_handler(CommandHandler("end_game", end_game_command))
    application.add_handler(CommandHandler("action", prompt_action))
    application.add_handler(CallbackQueryHandler(handle_action_callback, pattern=r"^\d$"))
    application.add_handler(CallbackQueryHandler(handle_settings_callback, pattern="^set_"))
    application.add_handler(CallbackQueryHandler(handle_end_meeting_vote, pattern="end_meeting_vote"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_player_message))

    return application
