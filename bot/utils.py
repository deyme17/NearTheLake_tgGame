from telegram import InlineKeyboardMarkup, InlineKeyboardButton


async def prompt_action(context, user_id):
    """Відправляє гравцям кнопки для вибору дій."""
    game = context.application.bot_data["game"]

    # Якщо нарада активна, повідомляємо, що хід неможливий
    if game.meeting_active:
        await context.bot.send_message(
            chat_id=user_id,
            text="⏳ Зараз триває нарада. Хід буде доступний після завершення наради."
        )
        return

    keyboard = [
        [InlineKeyboardButton("1: Скидання", callback_data="1")],
        [InlineKeyboardButton("2: Очищення", callback_data="2")],
        [InlineKeyboardButton("3: Штраф", callback_data="3")],
        [InlineKeyboardButton("4: Премія", callback_data="4")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=user_id,
        text="Виберіть вашу дію:",
        reply_markup=reply_markup
    )
