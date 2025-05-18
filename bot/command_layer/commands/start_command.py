from bot.command_layer.commands.command import BaseCommand
from messages.state_messages import in_game_now_message
from bot.services.messenger_service import MessengerService
from bot.services.session_service import SessionService
from game.core.game_coordinator import GameCoordinator

class StartGameCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "почати гру"

    async def execute(self, update, context, game):
        user_id = update.effective_user.id

        if user_id in game.players:
            await MessengerService.reply(update, context, in_game_now_message)
            return

        success, current_count = await SessionService.register_player(update, context, game)
        if success and current_count == game.settings.max_players:
            await GameCoordinator.start_game(game, context)