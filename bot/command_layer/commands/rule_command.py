from bot.command_layer.commands.command import BaseCommand
from messages.rules_messages import get_rule_message

class ShowRulesCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "правила гри"

    async def execute(self, update, context, game):
        await update.message.reply_text(get_rule_message())