from bot.commands.command import BaseCommand
from bot.controllers.game_controller import GameController

class EndGameCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "завершити гру"

    async def execute(self, update, context, game):
        await GameController.end_game(update, context, update)

