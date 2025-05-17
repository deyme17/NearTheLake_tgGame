from bot.commands.command import BaseCommand
from messages.general_messages import settings_not_available_message
from bot.services.ui_refresh_service import UIRefreshService

class SettingsCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "налаштування"

    async def execute(self, update, context, game):
        if game.state != "waiting":
            await UIRefreshService.reply(update, context, settings_not_available_message)
        else:
            await UIRefreshService.reply(update, context, "⚙️ Тут будуть параметри гри (ще в розробці).")