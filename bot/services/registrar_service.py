from config.settings import MAX_PLAYERS
from game.gamelogic.game_flow_manager import GameFlowManager
from messages.state_messages import (game_started_negative_messege, joined_message, 
                                     player_connected_message, game_full_message
)

class PlayerRegistrar:
    @staticmethod
    async def handle_start(update, context, game):
        """Returns: is_added, is_started: bool, bool"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name

        if game.state != "waiting":
            await update.message.reply_text(game_started_negative_messege)
            return False, False

        success, current_count = game.add_player(user_id, user_name)
        if success:
            await update.message.reply_text(joined_message(user_name, current_count))

            for player in game.players.values():
                if player.player_id != user_id:
                    await context.bot.send_message(
                        chat_id=player.player_id,
                        text=player_connected_message(user_name, current_count)
                    )

            if current_count == MAX_PLAYERS:
                await GameFlowManager.start_game(game, context)
                return True, True

            return True, False

        else:
            await update.message.reply_text(game_full_message)
            return False, False