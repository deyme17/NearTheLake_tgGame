from bot.commands.command import BaseCommand
from messages.state_messages import left_game_message, not_member_message
from bot.services.state_service import StateService
from bot.services.ui_refresh_service import UIRefreshService

class LeaveLobbyCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "вийти з лобі"

    async def execute(self, update, context, game):
        user_id = update.effective_user.id

        if user_id in game.players:
            player = game.players.pop(user_id)
            StateService.set_state(context, user_id, "idle")

            await UIRefreshService.update_keyboard(
                bot=context.bot,
                chat_id=user_id,
                text=left_game_message(player.name),
                state="idle"
            )
        else:
            await update.message.reply_text(not_member_message)
