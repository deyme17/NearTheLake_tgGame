from bot.commands.command import BaseCommand
from bot.commands.rule_command import ShowRulesCommand
from bot.commands.end_command import EndGameCommand
from bot.services.discussion_service import MessageRelayService

class InGameStateCommandManager:
    def __init__(self):
        self.commands: list[BaseCommand] = [
            ShowRulesCommand(),
            EndGameCommand()
        ]

    async def handle(self, update, context, game):
        text = update.message.text.strip().lower()
        user_id = update.effective_user.id

        if game.meeting_active:
            await MessageRelayService.forward_player_message(update, context, game)
            return

        for command in self.commands:
            if command.matches(text):
                await command.execute(update, context, game)
                return

        from messages.events_messages import no_communication_message
        await update.message.reply_text(no_communication_message)
