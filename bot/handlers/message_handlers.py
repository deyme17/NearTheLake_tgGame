from telegram import Update
from telegram.ext import CallbackContext
from bot.services.discussion_service import MessageRelayService
from config.helpers import get_game

async def handle_player_message(update: Update, context: CallbackContext):
    game = get_game(context)
    await MessageRelayService.forward_player_message(update, context, game)