from commands.command import BaseCommand
from bot.controllers.info_controller import InfoController

class ShowRulesCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "правила гри"

    async def execute(self, update, context, game):
        await InfoController.rules(update, context)
