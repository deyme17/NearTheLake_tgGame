from telegram import Update
from telegram.ext import CallbackContext
from config.helpers import get_game

from bot.handlers.command_dispatcher import CommandDispatcher
dispatcher = CommandDispatcher()

async def handle_player_message(update: Update, context: CallbackContext):
    game = get_game(context)
    await dispatcher.dispatch(update, context, game)
