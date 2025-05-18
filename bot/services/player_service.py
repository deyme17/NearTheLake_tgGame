from messages.state_messages import (
    game_not_configure_message, game_started_negative_messege,
    joined_message, player_connected_message, game_full_message
)
from game.gamelogic.game_engine import GameEngine
from bot.services.state_service import StateService
from bot.services.keyboard_messenger import KeyboardMessenger 
from bot.services.message_broadcast_service import MessageBroadcastService

class PlayerService:
    @staticmethod
    async def register(update, context, game):
        if not game:
            await update.message.reply_text(game_not_configure_message)
            return False, None

        if game.state != "waiting":
            await update.message.reply_text(game_started_negative_messege)
            return False, None

        user_id = update.effective_user.id
        user_name = update.effective_user.first_name

        success, current_count = game.add_player(user_id, user_name)
        if not success:
            await update.message.reply_text(game_full_message)
            return False, None

        StateService.set_state(context, user_id, "waiting_lobby")

        await KeyboardMessenger.send(
            bot=context.bot,
            chat_id=user_id,
            text=joined_message(user_name, current_count, game),
            state="waiting_lobby"
        )

        await MessageBroadcastService.send_all_except(
            bot=context.bot,
            players=game.players,
            excluded_id=user_id,
            text=player_connected_message(user_name, current_count, game)
        )

        return True, current_count
