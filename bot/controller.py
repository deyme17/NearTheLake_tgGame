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
    player_list = "\n".join([f"- {player.name}" for player in game.players.values()])
    start_message = (
        f"🎮 Гра розпочалася! Учасники:\n{player_list}\n\n"
        f"Ваш перший хід. Виберіть дію:\n"
        f"1: Скидання;\n"
        f"2: Очищення;\n"
        f"3: Штраф;\n"
        f"4: Премія."
    )

    # Повідомлення всім гравцям про початок гри
    for player in game.players.values():
        await context.bot.send_message(chat_id=player.player_id, text=start_message)
        await prompt_action(context, player.player_id)

async def end_game(update: Update, context: CallbackContext):
    """Завершує гру та виводить підсумкові результати."""
    game = context.application.bot_data.get("game")
    if not game:
        await update.message.reply_text("❌ Гра ще не створена.")
        return

    if game.state != "in_progress":
        await update.message.reply_text("❌ Гра вже завершена або ще не розпочата.")
        return

    # Завершуємо гру та надсилаємо підсумки
    game.state = "ended"
    results = game.get_winner()
    for player in game.players.values():
        await context.bot.send_message(chat_id=player.player_id, text="🏁 Гра завершена!")
        await context.bot.send_message(chat_id=player.player_id, text=results)

    # Очищуємо стан гри для початку нової
    game.reset_game()
    await update.message.reply_text("🔄 Гру завершено. Ви можете розпочати нову гру.")