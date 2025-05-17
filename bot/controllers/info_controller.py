from telegram import Update
from telegram.ext import CallbackContext
from messages.help_message import help_message
from messages.rule_message import rule_message, game_water_matrix_message, game_water_matrix_not_found_message
from config.constants import game_matrix_path

class InfoController:
    @staticmethod
    async def help(update: Update, context: CallbackContext):
        await update.message.reply_text(help_message())

    @staticmethod
    async def rules(update: Update, context: CallbackContext):
        await update.message.reply_text(rule_message())
        try:
            with open(game_matrix_path, "rb") as photo:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=photo,
                    caption=game_water_matrix_message
                )
        except FileNotFoundError:
            await update.message.reply_text(game_water_matrix_not_found_message)