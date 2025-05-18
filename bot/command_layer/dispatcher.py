from bot.command_layer.router import GameStateRouter
from messages.error_messages import uknown_state_message

class CommandDispatcher:
    def __init__(self):
        self.router = GameStateRouter()

    async def dispatch(self, update, context, game):
        user_id = update.effective_user.id
        manager = self.router.get_manager(context, user_id)

        if manager:
            await manager.handle(update, context, game)
        else:
            await update.message.reply_text(uknown_state_message)
