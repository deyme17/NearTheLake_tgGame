from telegram import Update
from telegram.ext import CallbackContext
from messages.general_messages import settings_enter_value_message

async def handle_settings_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    param = query.data.replace("set_", "")
    context.user_data["param_to_set"] = param
    await query.message.reply_text(settings_enter_value_message(param))