from bot.command_layer.commands.command import BaseCommand
from messages.state_messages import vote_started_message, vote_registered_message, you_voted_now_message
from game.core.game_coordinator import GameCoordinator

class EndGameCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "завершити гру"

    async def execute(self, update, context, game):
        user_id = update.effective_user.id

        if not game.end_vote_active:
            game.end_vote_active = True
            game.end_game_votes = {user_id}

            for player in game.players.values():
                if player.player_id != user_id:
                    await context.bot.send_message(
                        chat_id=player.player_id,
                        text=vote_started_message(game.players[user_id].name)
                    )
                    
        elif user_id in game.end_game_votes:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=you_voted_now_message
            )
        else:
            game.end_game_votes.add(user_id)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=vote_registered_message
            )

        if len(game.end_game_votes) > len(game.players) // 2:
            await GameCoordinator.end_game(game, context)