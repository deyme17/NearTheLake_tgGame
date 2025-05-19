from messages.state_messages import (
    game_not_configure_message,
    game_started_negative_messege,
    get_joined_message,
    get_player_connected_message,
    game_full_message,
)
from bot.services.messenger_service import MessengerService

class SessionService:
    @staticmethod
    def get_state(context, user_id: int) -> str:
        return context.application.bot_data.get("user_states", {}).get(user_id, "idle")

    @staticmethod
    def set_state(context, user_id: int, state: str):
        user_states = context.application.bot_data.setdefault("user_states", {})
        user_states[user_id] = state

    @staticmethod
    def set_all(context, user_ids: list[int], state: str):
        user_states = context.application.bot_data.setdefault("user_states", {})
        for uid in user_ids:
            user_states[uid] = state

    @staticmethod
    def reset_all(context):
        context.application.bot_data["user_states"] = {}

    @staticmethod
    async def register_player(update, context, game):
        if not game:
            await update.message.reply_text(game_not_configure_message)
            return False, None

        if game.state != "waiting":
            await update.message.reply_text(game_started_negative_messege)
            return False, None

        user_id = update.effective_user.id
        user_name = update.effective_user.first_name

        success, current_count = game.add_player(user_id, user_name)
        if not success:
            await update.message.reply_text(game_full_message)
            return False, None

        SessionService.set_state(context, user_id, "waiting_lobby")

        await MessengerService.send(
            context=context,
            chat_id=user_id,
            text=get_joined_message(user_name, current_count, game),
            state="waiting_lobby"
        )
        await MessengerService.send_all_except(
            bot=context.bot,
            players=game.players,
            excluded_id=user_id,
            text=get_player_connected_message(user_name, current_count, game)
        )

        if current_count == game.settings.max_players:
            from game.core.game_coordinator import GameCoordinator
            await GameCoordinator.start_game(game, context)

        return True, current_count