from bot.commands.command import BaseCommand
from bot.services.player_service import PlayerService
from messages.state_messages import in_game_now_message
from bot.services.ui_refresh_service import UIRefreshService
from bot.services.state_service import StateService

class StartGameCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "почати гру"

    async def execute(self, update, context, game):
        user_id = update.effective_user.id

        if user_id in game.players:
            await UIRefreshService.reply(update, context, in_game_now_message)
            return

        success, count = await PlayerService.register(update, context, game)
        if success:
            StateService.set_state(context, user_id, "waiting_lobby")