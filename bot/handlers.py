from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from game.game import Game
from bot.message import help_message, rule_message
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from bot.utils import prompt_action
from bot.controller import start_game
from config.settings import MAX_PLAYERS



ENTER_NAME = 0


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


async def reset_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Скидає поточну гру."""
    context.application.bot_data["game"] = Game()
    await update.message.reply_text("Гру скинуто. Ви можете почати нову гру.")


async def game_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Відправляє стан гри адміністратору."""
    game = context.application.bot_data.get("game")
    if not game:
        await update.message.reply_text("Гра ще не створена.")
        return
    
    status = f"Стан гри:\n" \
             f"Гравців: {len(game.players)}/{game.max_players}\n" \
             f"Хід: {game.turn}\n" \
             f"Якість води: {game.lake.water_quality}"
    await update.message.reply_text(status)


async def start_meeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запускає нараду для гравців."""
    game = context.application.bot_data.get("game")
    if not game or game.state != "in_progress":
        await update.message.reply_text("Гра ще не розпочата.")
        return

    if game.is_meeting_active:
        await update.message.reply_text("Нарада вже активна!")
        return

    game.start_meeting()
    await update.message.reply_text("🗣️ Нарада почалася! Гравці можуть спілкуватися протягом 3 хвилин.")


async def player_message(update, context):
    """Обробляє повідомлення гравців під час нарад."""
    game = context.application.bot_data.get("game")
    if not game or game.state != "in_progress":
        await update.message.reply_text("Гра ще не розпочалася. Будь ласка, дочекайтеся початку.")
        return

    if not game.is_meeting_active:
        await update.message.reply_text("Нарада не активна зараз.")
        return

    # Додавання повідомлення до чату наради
    user_id = update.effective_user.id
    name = game.players.get(user_id, {}).get("name", "Невідомий гравець")
    text = update.message.text

    for player_id in game.players:
        if player_id != user_id:
            await context.bot.send_message(chat_id=player_id, text=f"{name}: {text}")


    # Розсилка повідомлення всім гравцям
    sender = update.effective_user.first_name
    message = f"{sender}: {update.message.text}"

    for user_id in game.players.keys():
        if user_id != update.effective_user.id:  # Не надсилати повідомлення собі
            await context.bot.send_message(chat_id=user_id, text=message)


async def end_meeting(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершує нараду."""
    game = context.application.bot_data.get("game")
    if not game or not game.is_meeting_active:
        await update.message.reply_text("Нарада не активна зараз.")
        return

    game.end_meeting()
    await update.message.reply_text("⏳ Нарада завершена. Повертаємося до гри!")


async def handle_action_callback(update, context):
    """Обробляє вибір гравця через кнопки."""
    query = update.callback_query
    action = query.data  # Отримуємо вибране значення (1, 2, 3, 4)
    user_id = query.from_user.id

    game = context.application.bot_data.get("game")
    if not game or game.state != "in_progress":
        await query.answer("Гра ще не розпочалася або вже завершена!")
        return

    if user_id not in game.players:
        await query.answer("Ви не зареєстровані у грі!")
        return

    game.players[user_id]["current_action"] = action
    await query.answer(f"Ви вибрали: {action}")
    await query.edit_message_text(text=f"Ваш вибір: {action}")

    if game.all_actions_collected():
        admin_chat_id = context.bot_data.get("admin_chat_id")
        await game.process_turn(context, admin_chat_id)
