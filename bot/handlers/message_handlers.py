from messages.error_messages import uknown_state_message
from telegram import Update
from telegram.ext import CallbackContext
from config.helpers import get_game

from bot.command_managers.idle_command_manager import IdleStateCommandManager
from bot.command_managers.in_game_command_manager import InGameStateCommandManager
from bot.services.state_service import StateService


state_managers = {
    "idle": IdleStateCommandManager(),
    "in_game": InGameStateCommandManager(),
}

async def handle_player_message(update: Update, context: CallbackContext):
    game = get_game(context)
    state = StateService.get_state(context, update.effective_user.id)
    text = update.message.text.strip().lower()

    manager = state_managers.get(state)

    if state == "in_game" and manager:
        for command in manager.commands:
            if command.matches(text):
                await command.execute(update, context, game)
                return

        if game.meeting_active:
            from bot.services.discussion_service import MessageRelayService
            await MessageRelayService.forward_player_message(update, context, game)
        else:
            from messages.events_messages import no_communication_message
            await update.message.reply_text(no_communication_message)

    elif manager:
        await manager.handle(text, update, context, game)

    else:
        await update.message.reply_text(uknown_state_message)
