from telegram import Update
from telegram.ext import CallbackContext
from bot.utils import prompt_action



async def start_game(update: Update, context: CallbackContext):
    """Початок гри, коли всі гравці зібрані."""
    game = context.application.bot_data.get("game")

    if not game or game.state != "waiting":
        await update.message.reply_text("❌ Гра вже почалася або ще не налаштована.")
        return

    game.state = "in_progress"

    # Список учасників
    player_list = "\n".join([f"- {data['name']}" for data in game.players.values()])
    start_message = (
        f"🎮 Гра розпочалася! Учасники:\n{player_list}\n\n"
        f"Ваш перший хід. Виберіть дію:\n"
        f"1: Скидання;\n"
        f"2: Очищення;\n"
        f"3: Штраф;\n"
        f"4: Премія."
    )

    # Повідомлення всім гравцям про початок гри
    for user_id in game.players.keys():
        await context.bot.send_message(chat_id=user_id, text=start_message)

    # Надсилаємо кнопки дій
    for user_id in game.players.keys():
        await prompt_action(context, user_id)


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
