from bot.commands.command import BaseCommand
from bot.commands.rule_command import ShowRulesCommand
from bot.commands.start_command import StartGameCommand
from bot.commands.settings_command import SettingsCommand
from messages.error_messages import command_not_recognize_message, uknown_parameter_message
from messages.general_messages import settings_updated_message, settings_invalid_value

class IdleStateCommandManager:
    def __init__(self):
        self.commands: list[BaseCommand] = [
            ShowRulesCommand(),
            StartGameCommand(),
            SettingsCommand()
        ]

    async def handle(self, update, context, game):
        if "param_to_set" in context.user_data:
            param = context.user_data.pop("param_to_set")
            new_val = update.message.text.strip()

            try:
                val = int(new_val)
                success = game.settings.update(param, val)
                if success:
                    await update.message.reply_text(settings_updated_message(param, val))
                else:
                    await update.message.reply_text(uknown_parameter_message)
            except ValueError:
                await update.message.reply_text(settings_invalid_value)
            return

        text = update.message.text.strip().lower()
        for command in self.commands:
            if command.matches(text):
                await command.execute(update, context, game)
                return

        await update.message.reply_text(command_not_recognize_message)
