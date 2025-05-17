from telegram import Update
from telegram.ext import CallbackContext

from game.gamelogic.game_engine import GameEngine
from messages.state_messages import game_started_or_not_configure_messege, game_not_created_messege
from config.helpers import get_game

class GameController:
    @staticmethod
    async def start_game(update: Update, context: CallbackContext):
        game = get_game(context)
        if not game or game.state != "waiting":
            await update.message.reply_text(game_started_or_not_configure_messege)
            return
        await GameEngine(game, context).start_game()

    @staticmethod
    async def end_game(update, context, update_for_flow=None):
        game = get_game(context)
        if not game:
            await update.message.reply_text(game_not_created_messege)
            return
        await GameEngine(game, context).end_game(update_for_flow or update)
