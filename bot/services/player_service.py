from config.settings import MAX_PLAYERS
from messages.state_messages import (
    game_not_configure_message, game_started_negative_messege,
    joined_message, player_connected_message, game_full_message
)
from game.gamelogic.game_engine import GameEngine


class PlayerService:
    @staticmethod
    async def register(update, context, game):
        """
        Returns: success: bool, current_count: int or None
        """
        if not game:
            await update.message.reply_text(game_not_configure_message)
            return False, None

        if game.state != "waiting":
            await update.message.reply_text(game_started_negative_messege)
            return False, None

        user_id = update.effective_user.id
        user_name = update.effective_user.first_name

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
                await GameEngine(game, context).start_game()

            return True, current_count

        else:
            await update.message.reply_text(game_full_message)
            return False, None