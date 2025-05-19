from bot.command_layer.commands.command import BaseCommand
from messages.state_messages import vote_started_message, vote_registered_message, you_voted_now_message
from game.core.game_coordinator import GameCoordinator

from bot.services.messenger_service import MessengerService

class EndGameCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "завершити гру"

    async def execute(self, update, context, game):
        user_id = update.effective_user.id

        if not game.end_vote_active:
            game.end_vote_active = True
            game.end_game_votes = {user_id}

            await MessengerService.send_all_except(
                bot=context.bot,
                players=game.players,
                excluded_id=user_id,
                text=vote_started_message(game.players[user_id].name)
            )

        elif user_id in game.end_game_votes:
            await MessengerService.send(
                context=context,
                chat_id=update.effective_chat.id,
                text=you_voted_now_message
            )
        else:
            game.end_game_votes.add(user_id)
            await MessengerService.send(
                context=context,
                chat_id=update.effective_chat.id,
                text=vote_registered_message
            )

        if len(game.end_game_votes) > len(game.players) // 2:
            await GameCoordinator.end_game(game, context)
