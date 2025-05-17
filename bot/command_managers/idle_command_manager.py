from bot.commands.command import BaseCommand
from bot.commands.rule_command import ShowRulesCommand
from bot.commands.start_command import StartGameCommand
from bot.commands.settings_command import SettingsCommand
from messages.error_messages import command_not_recognize_message

class IdleStateCommandManager:
    def __init__(self):
        self.commands: list[BaseCommand] = [
            ShowRulesCommand(),
            StartGameCommand(),
            SettingsCommand()
        ]

    async def handle(self, update, context, game):
        text = update.message.text.strip().lower()
        for command in self.commands:
            if command.matches(text):
                await command.execute(update, context, game)
                return

        await update.message.reply_text(command_not_recognize_message)
