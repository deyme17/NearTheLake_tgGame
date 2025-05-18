from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from bot.commands.command import BaseCommand
from messages.general_messages import settings_menu_title, settings_unavailable_message, param_ua

class SettingsCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "налаштування"

    def get_settings_keyboard(self):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(f"👥 {param_ua['MAX_PLAYERS']}", callback_data="set_MAX_PLAYERS")],
            [InlineKeyboardButton(f"📅 {param_ua['GAME_DURATION_MONTHS']}", callback_data="set_GAME_DURATION_MONTHS")],
            [InlineKeyboardButton(f"🗓 {param_ua['MEETING_INTERVAL']}", callback_data="set_MEETING_INTERVAL")],
            [InlineKeyboardButton(f"✅ {param_ua['BONUS_SCORE']}", callback_data="set_BONUS_SCORE")],
            [InlineKeyboardButton(f"❌ {param_ua['PENALTY_SCORE']}", callback_data="set_PENALTY_SCORE")]
        ])

    async def execute(self, update, context, game):
        if game.state != "waiting":
            await update.message.reply_text(settings_unavailable_message)
        else:
            await update.message.reply_text(settings_menu_title, reply_markup=self.get_settings_keyboard())