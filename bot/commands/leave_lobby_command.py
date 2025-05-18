from bot.commands.command import BaseCommand
from messages.state_messages import left_game_message, not_member_message
from bot.services.state_service import StateService
from bot.services.keyboard_messenger import KeyboardMessenger
from bot.services.message_broadcast_service import MessageBroadcastService

class LeaveLobbyCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "вийти з лобі"

    async def execute(self, update, context, game):
        user_id = update.effective_user.id

        if user_id in game.players:
            player = game.players.pop(user_id)
            StateService.set_state(context, user_id, "idle")

            await KeyboardMessenger.send(
                bot=context.bot,
                chat_id=user_id,
                text=left_game_message(player.name),
                state="idle"
            )

            await MessageBroadcastService.send_all_except(
                bot=context.bot,
                players=game.players,
                excluded_id=user_id,
                text=f"❗️{player.name} вийшов із лобі."
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=not_member_message
            )