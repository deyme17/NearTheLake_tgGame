from bot.command_layer.commands.command import BaseCommand
from bot.command_layer.commands.rule_command import ShowRulesCommand
from bot.command_layer.commands.start_command import StartGameCommand
from bot.command_layer.commands.settings_command import SettingsCommand
from bot.command_layer.command_managers.command_manager import BaseCommandManager
from messages.error_messages import unknown_parameter_message
from messages.general_messages import settings_updated_message, settings_invalid_value

class IdleStateCommandManager(BaseCommandManager):
    def __init__(self):
        super().__init__([
            ShowRulesCommand(),
            StartGameCommand(),
            SettingsCommand()
        ])

    async def handle(self, update, context, game):
        if "param_to_set" in context.user_data:
            param = context.user_data.pop("param_to_set")
            new_val = update.message.text.strip()

            if not new_val.isdigit():
                await update.message.reply_text(settings_invalid_value)
                return

            val = int(new_val)
            success = game.settings.update(param, val)
            if success:
                await update.message.reply_text(settings_updated_message(param, val))
            else:
                await update.message.reply_text(unknown_parameter_message)
            return

        await super().handle(update, context, game)