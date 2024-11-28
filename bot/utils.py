from telegram import InlineKeyboardMarkup, InlineKeyboardButton

async def prompt_action(context, chat_id):
    """Надсилає кнопки для вибору дій гравцю."""
    keyboard = [
        [InlineKeyboardButton("1: Скидання", callback_data="1")],
        [InlineKeyboardButton("2: Очищення", callback_data="2")],
        [InlineKeyboardButton("3: Штраф", callback_data="3")],
        [InlineKeyboardButton("4: Премія", callback_data="4")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=chat_id, text="Виберіть вашу дію:", reply_markup=reply_markup)
