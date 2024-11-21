from telegram import Update
from telegram.ext import CallbackContext

async def start_game(update: Update, context: CallbackContext):
    """Команда для запуску гри."""
    game = context.application.bot_data.get("game")
    if not game:
        await update.message.reply_text("Гра ще не створена.")
        return

    if game.start_game():
        await update.message.reply_text("🎮 Гра розпочалася!")
        await notify_players(context)
    else:
        await update.message.reply_text("🙁 Недостатньо гравців для початку гри.")


async def notify_players(context: CallbackContext):
    """Розсилає всім гравцям стан гри."""
    game = context.application_data.get("game")
    if not game:
        return

    for user_id in game.players.keys():
        await context.bot.send_message(chat_id=user_id, text="Наступний хід розпочався!")


async def end_game(update: Update, context: CallbackContext):
    """Завершує гру та виводить підсумкові результати."""
    game = context.application_data.get("game")
    if not game:
        await update.message.reply_text("Гра ще не створена.")
        return

    if game.check_game_end():
        results = game.get_winner()
        await update.message.reply_text("🏁 Гра завершена!")
        await update.message.reply_text(results)
    else:
        await update.message.reply_text("🕒 Гра ще не завершена!")
