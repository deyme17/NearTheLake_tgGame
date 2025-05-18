from bot.commands.command import BaseCommand
from bot.commands.rule_command import ShowRulesCommand
from bot.commands.leave_lobby_command import LeaveLobbyCommand
from messages.state_messages import joined_message, waiting_for_player_message


class WaitingLobbyCommandManager:
    def __init__(self):
        self.commands: list[BaseCommand] = [
            ShowRulesCommand(),
            LeaveLobbyCommand()
        ]

    async def handle(self, update, context, game):
        text = update.message.text.strip().lower()

        for command in self.commands:
            if command.matches(text):
                await command.execute(update, context, game)
                return

        user_id = update.effective_user.id
        player = game.players.get(user_id)

        if not player:
            await update.message.reply_text(waiting_for_player_message)
