from bot.command_layer.commands.command import BaseCommand
from messages.state_messages import left_game_message, not_member_message, get_left_lobby_message
from bot.services.session_service import SessionService
from bot.services.messenger_service import MessengerService


class LeaveLobbyCommand(BaseCommand):
    def matches(self, text: str) -> bool:
        return text.strip().lower() == "вийти з лобі"

    async def execute(self, update, context, game):
        user_id = update.effective_user.id

        if user_id in game.players:
            player = game.players.pop(user_id)
            SessionService.set_state(context, user_id, "idle")

            await MessengerService.send(
                context=context,
                chat_id=user_id,
                text=left_game_message(player.name),
                state="idle"
            )

            await MessengerService.send_all_except(
                bot=context.bot,
                players=game.players,
                excluded_id=user_id,
                text=get_left_lobby_message(player)
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=not_member_message
            )