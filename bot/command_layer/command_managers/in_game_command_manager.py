from bot.command_layer.commands.command import BaseCommand
from bot.command_layer.commands.rule_command import ShowRulesCommand
from bot.command_layer.commands.end_command import EndGameCommand
from bot.command_layer.command_managers.command_manager import BaseCommandManager
from bot.services.meeting_service import MeetingService
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
            await MeetingService.forward_player_message(update, context, game)
            return

        for command in self.commands:
            if command.matches(text):
                await command.execute(update, context, game)
                return

        await update.message.reply_text(no_communication_message)