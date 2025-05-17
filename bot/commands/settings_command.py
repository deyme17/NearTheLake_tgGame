from commands.command import BaseCommand
from messages.settings_message import settings_not_available_message

class SettingsCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "налаштування"

    async def execute(self, update, context, game):
        if game.state != "waiting":
            await update.message.reply_text(settings_not_available_message)
        else:
            await update.message.reply_text("⚙️ Тут будуть параметри гри (ще в розробці).")
