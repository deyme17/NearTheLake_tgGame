from bot.commands.command import BaseCommand
from bot.commands.rule_command import ShowRulesCommand
from bot.commands.end_command import EndGameCommand
from bot.services.discussion_service import MessageRelayService
from bot.command_managers.command_manager import BaseCommandManager
from messages.events_messages import no_communication_message 

class InGameStateCommandManager(BaseCommandManager):
    def __init__(self):
        super().__init__([
            ShowRulesCommand(),
            EndGameCommand()
        ])

    async def handle(self, update, context, game):
        user_id = update.effective_user.id
        text = update.message.text.strip().lower()

        if game.meeting_active:
            await MessageRelayService.forward_player_message(update, context, game)
            return

        for command in self.commands:
            if command.matches(text):
                await command.execute(update, context, game)
                return

        await update.message.reply_text(no_communication_message)