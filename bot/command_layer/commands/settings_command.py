from bot.command_layer.commands.command import BaseCommand
from messages.general_messages import settings_menu_title, settings_unavailable_message
from bot.ui_components.keyboard import get_settings_keyboard

class SettingsCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "налаштування"

    async def execute(self, update, context, game):
        chat_id = update.effective_chat.id

        if game.state != "waiting":
            await context.bot.send_message(
                chat_id=chat_id,
                text=settings_unavailable_message
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text=settings_menu_title,
                reply_markup=get_settings_keyboard(game)
            )