from bot.command_managers.idle_command_manager import IdleStateCommandManager
from bot.command_managers.in_game_command_manager import InGameStateCommandManager
from bot.services.state_service import StateService
from messages.error_messages import uknown_state_message

class CommandDispatcher:
    def __init__(self):
        self.managers = {
            "idle": IdleStateCommandManager(),
            "in_game": InGameStateCommandManager(),
        }

    async def dispatch(self, update, context, game):
        state = StateService.get_state(context, update.effective_user.id)
        manager = self.managers.get(state)

        if manager:
            await manager.handle(update, context, game)
        else:
            await update.message.reply_text(uknown_state_message)