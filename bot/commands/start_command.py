from commands.command import BaseCommand
from bot.controllers.game_controller import GameController
from messages.game_state_messages import game_started_messege

class StartGameCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "почати гру"

    async def execute(self, update, context, game):
        if game.state == "waiting":
            await GameController.start_game(update, context)
            context.user_data["state"] = "in_game"
        else:
            await update.message.reply_text(game_started_messege)
