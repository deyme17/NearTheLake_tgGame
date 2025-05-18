from bot.ui_components.keyboard import get_keyboard_for_state

class KeyboardMessenger:
    @staticmethod
    async def reply(update, context, text: str, state: str = None):
        state = state or context.user_data.get("state", "idle")
        await update.message.reply_text(text, reply_markup=get_keyboard_for_state(state))

    @staticmethod
    async def send(bot, chat_id: int, text: str, state: str = "idle"):
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=get_keyboard_for_state(state))