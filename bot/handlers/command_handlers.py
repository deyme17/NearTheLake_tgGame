from telegram import Update
from telegram.ext import CallbackContext, ContextTypes

from bot.services.session_service import SessionService
from game.core.game_coordinator import GameCoordinator

from messages.rules_messages import get_rule_message
from messages.general_messages import get_help_message
from bot.ui_components.keyboard import get_keyboard_for_state
from config.helpers import get_game
from messages.general_messages import greeting_menu_messsge

async def start(update: Update, context: CallbackContext):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=greeting_menu_messsge,
        reply_markup=get_keyboard_for_state("idle")
    )

async def start_game_command(update: Update, context: CallbackContext):
    game = get_game(context)
    await SessionService.register_player(update, context, game)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_help_message())

async def rule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_rule_message())

async def end_game_command(update: Update, context: CallbackContext):
    await GameCoordinator.end_game(get_game(context), context, update)


