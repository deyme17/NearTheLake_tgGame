from bot.commands.command import BaseCommand
from bot.commands.rule_command import ShowRulesCommand
from bot.commands.leave_lobby_command import LeaveLobbyCommand
from bot.command_managers.command_manager import BaseCommandManager
from messages.state_messages import waiting_for_player_message

class WaitingLobbyCommandManager(BaseCommandManager):
    def __init__(self):
        super().__init__([
            ShowRulesCommand(),
            LeaveLobbyCommand()
        ])

    async def handle(self, update, context, game):
        user_id = update.effective_user.id

        if user_id not in game.players:
            await update.message.reply_text(waiting_for_player_message)
            return

        await super().handle(update, context, game)