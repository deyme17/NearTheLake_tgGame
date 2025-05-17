from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from config.constants import ACTION_NAMES
from messages.action_messages import choose_action_message
from messages.events_messages import meeting_continues_message

async def prompt_action(context, user_id):
    """Sends buttons to players to select actions."""
    game = context.application.bot_data["game"]

    if game.meeting_active:
        await context.bot.send_message(
            chat_id=user_id,
            text=meeting_continues_message
        )
        return

    keyboard = [
        [InlineKeyboardButton(f"{key}: {name}", callback_data=key)]
        for key, name in ACTION_NAMES.items()
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=user_id,
        text=choose_action_message,
        reply_markup=reply_markup
    )