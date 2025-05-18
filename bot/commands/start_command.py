from bot.commands.command import BaseCommand
from bot.services.player_service import PlayerService
from messages.state_messages import in_game_now_message
from bot.services.keyboard_messenger import KeyboardMessenger
from bot.services.state_service import StateService
from game.gamelogic.game_engine import GameEngine

class StartGameCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "почати гру"

    async def execute(self, update, context, game):
        user_id = update.effective_user.id

        if user_id in game.players:
            await KeyboardMessenger.reply(update, context, in_game_now_message)
            return

        success, current_count = await PlayerService.register(update, context, game)
        if success and current_count == game.settings.max_players:
            await GameEngine(game, context).start_game()