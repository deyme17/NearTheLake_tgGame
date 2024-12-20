from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from game.game import Game
from bot.message import help_message, rule_message
from telegram.ext import CallbackContext
from game.events import end_meeting
from bot.controller import start_game
from config.settings import MAX_PLAYERS



async def start(update: Update, context: CallbackContext):
    """Обробляє команду /start і додає гравців до гри."""
    game = context.application.bot_data.get("game")

    if not game:
        await update.message.reply_text("❌ Гра ще не налаштована.")
        return

    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    if game.state != "waiting":
        await update.message.reply_text("❌ Гра вже почалася. Ви не можете приєднатися зараз.")
        return

    success, current_count = game.add_player(user_id, user_name)
    if success:
        await update.message.reply_text(
            f"✅ Ви приєдналися до гри як {user_name}. Очікуємо інших гравців: {current_count}/{MAX_PLAYERS}."
        )

        # Оповіщення інших гравців
        for other_id in game.players:
            if other_id != user_id:
                await context.bot.send_message(
                    chat_id=other_id,
                    text=f"👤 Гравець {user_name} приєднався до гри. Гравців: {current_count}/{MAX_PLAYERS}."
                )

        # Якщо всі гравці зібрані, запускаємо гру
        if current_count == MAX_PLAYERS:
            await start_game(update, context)
    else:
        await update.message.reply_text("⚠️ Ви вже у грі або місця більше немає.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Відправляє повідомлення з довідкою."""
    await update.message.reply_text(help_message())


async def rule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Відправляє правила гри."""
    await update.message.reply_text(rule_message())

    # Відправка зображення ігрової матриці
    try:
        with open("assets/gameMatrix_NearTheLake.png", "rb") as photo:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo,
                caption=(
                    "🗺️ **Ігрова матриця стану води:**\n\n"
                    "Вона показує, як змінюється якість води залежно від ваших рішень:\n"
                    "1️⃣ **Скидання** – дає прибуток, але погіршує якість води.\n"
                    "2️⃣ **Очищення** – поліпшує якість води, але приносить менше прибутку.\n\n"
                    "🔄 **Індикатор якості води** переміщується:\n"
                    "  - Вліво при скиданні (1️⃣).\n"
                    "  - Вправо при очищенні (2️⃣).\n"
                    "  - Рівень змінюється при переході через край матриці."
                )
            )
    except FileNotFoundError:
        await update.message.reply_text("⚠️ Не вдалося знайти зображення ігрової матриці.")

async def player_message(update, context):
    """Обробляє текстові повідомлення від гравців."""
    game = context.application.bot_data.get("game")
    user_id = update.effective_user.id

    if not game or not game.meeting_active:
        await update.message.reply_text("Нарада не активна. Повідомлення не приймаються.")
        return

    player_name = game.players[user_id]["name"]
    message_text = update.message.text

    # Надсилаємо повідомлення всім гравцям
    for target_user_id in game.players:
        if target_user_id != user_id:  # Уникати надсилання повідомлення самому відправнику
            await context.bot.send_message(
                chat_id=target_user_id,
                text=f"💬 {player_name}: {message_text}"
            )


async def handle_action_callback(update, context):
    """Handles player actions via callback buttons."""
    query = update.callback_query
    action = query.data
    user_id = query.from_user.id

    game = context.application.bot_data.get("game")
    if not game or game.state != "in_progress":
        await query.answer("Гра ще не розпочалася або вже завершена!")
        return

    if user_id not in game.players:
        await query.answer("Ви не зареєстровані у грі!")
        return

    if game.players[user_id]["current_action"] is not None:
        await query.answer("Ви вже зробили свій вибір в цьому ході!")
        return

    # Записуємо дію гравця
    game.players[user_id]["current_action"] = action
    
    # Повідомляємо про успішний вибір
    action_names = {
        "1": "Скидання",
        "2": "Очищення",
        "3": "Штраф",
        "4": "Премія"
    }
    await query.answer(f"Ви вибрали: {action_names[action]}")
    await query.edit_message_text(text=f"Ваш вибір: {action_names[action]}")

    # Перевіряємо, чи всі гравці зробили свій вибір
    if game.all_actions_collected():
        await game.process_turn(context)
    else:
        await context.bot.send_message(
            chat_id=user_id,
            text="Очікуємо вибір інших гравців"
        )

async def handle_end_meeting_vote(update, context):
    """Обробляє голосування за завершення наради."""
    game = context.application.bot_data.get("game")
    user_id = update.effective_user.id

    if not game or not game.meeting_active:
        await update.callback_query.answer("Нарада не активна зараз.")
        return

    if user_id in game.meeting_end_votes:
        await update.callback_query.answer("Ви вже проголосували.")
        return

    game.meeting_end_votes.add(user_id)
    await update.callback_query.answer("Ваш голос за завершення наради зараховано.")

    # Перевіряємо, чи всі проголосували
    if len(game.meeting_end_votes) == len(game.players):
        await end_meeting(context, game)  # Викликаємо функцію з events.py
