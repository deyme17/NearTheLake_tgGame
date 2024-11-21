from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from game.game import Game
from bot.message import help_message, rule_message

ENTER_NAME = 0


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обробляє команду /start для нового гравця."""
    if "game" not in context.application.bot_data:
        context.application.bot_data["game"] = Game()

    game = context.application.bot_data["game"]

    if game.state == "in_progress":
        # Якщо гра вже запущена, нічого не робимо
        await update.message.reply_text("Гра вже розпочата. Приєднатися неможливо.")
        return

    if game.state == "waiting":
        # Реєструємо нового гравця
        user_id = update.effective_user.id
        name = update.effective_user.first_name

        if user_id not in game.players:
            if game.add_player(user_id, name):
                await update.message.reply_text(
                    f"✅ Ви приєдналися до гри як {name}.\n"
                    f"Очікуємо інших гравців: {len(game.players)}/{game.max_players}."
                )
            else:
                await update.message.reply_text("🙁 Ви не можете приєднатися до гри.")
        else:
            await update.message.reply_text(
                f"Ви вже у грі. Зараз гравців: {len(game.players)}/{game.max_players}."
            )



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Відправляє повідомлення з довідкою."""
    await update.message.reply_text(help_message())


async def rule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Відправляє правила гри."""
    await update.message.reply_text(rule_message())
