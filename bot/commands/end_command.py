from commands.command import BaseCommand
from bot.controllers.game_controller import GameController
from messages.game_state_messages import no_game_messege

class EndGameCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "завершити гру"

    async def execute(self, update, context, game):
        if game.state != "in_progress":
            await update.message.reply_text(no_game_messege)
        else:
            await GameController.end_game(update, context)
            context.user_data["state"] = "idle"
