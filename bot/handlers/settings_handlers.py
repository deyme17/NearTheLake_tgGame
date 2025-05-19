from telegram import Update
from telegram.ext import CallbackContext
from messages.general_messages import settings_enter_value_message
from messages.error_messages import unknown_parameter_message
from config.settings import SETTINGS_PARAMS

async def handle_settings_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    param = query.data.replace("set_", "")
    if param not in [key for key, _ in SETTINGS_PARAMS]:
        await query.message.reply_text(unknown_parameter_message)
        return

    context.user_data["param_to_set"] = param
    await query.message.reply_text(settings_enter_value_message(param))