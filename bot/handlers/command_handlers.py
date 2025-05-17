from telegram import Update
from telegram.ext import CallbackContext, ContextTypes

from bot.services.registrar_service import PlayerRegistrar
from bot.controllers.info_controller import InfoController
from bot.controllers.game_controller import GameController

from bot.ui_components.keyboard import get_keyboard_for_state
from config.helpers import get_game
from messages.start_message import greeting_menu_messsge

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        greeting_menu_messsge,
        reply_markup=get_keyboard_for_state("idle")
    )

async def start_game_command(update: Update, context: CallbackContext):
    game = get_game(context)
    await PlayerRegistrar.handle_start(update, context, game)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await InfoController.help(update, context)

async def rule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await InfoController.rules(update, context)

async def end_game_command(update: Update, context: CallbackContext):
    await GameController.end_game(update, context)
