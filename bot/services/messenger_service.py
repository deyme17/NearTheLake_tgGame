from bot.ui_components.promt_action import prompt_action
from bot.ui_components.keyboard import get_keyboard_for_state

class MessengerService:
    @staticmethod
    async def send(context, chat_id: int, text: str, state: str = "idle"):
        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=get_keyboard_for_state(state)
        )

    @staticmethod
    async def reply(update, context, text: str, state: str = None):
        state = state or context.user_data.get("state", "idle")
        await update.message.reply_text(
            text,
            reply_markup=get_keyboard_for_state(state)
        )

    @staticmethod
    async def send_all(bot, players: dict, text: str, reply_markup=None):
        if callable(text):
            text = text()
        for player in players.values():
            await bot.send_message(
                chat_id=player.player_id,
                text=text,
                reply_markup=reply_markup
            )

    @staticmethod
    async def send_all_except(bot, players: dict, excluded_id: int, text: str, reply_markup=None):
        if callable(text):
            text = text()
        for player in players.values():
            if player.player_id != excluded_id:
                await bot.send_message(
                    chat_id=player.player_id,
                    text=text,
                    reply_markup=reply_markup
                )

    @staticmethod
    async def handle_actions(context, actions: list[dict]):
        for act in actions:
            if act["type"] == "send_message":
                await MessengerService.send(
                    context=context,
                    chat_id=act["chat_id"],
                    text=act["text"],
                    state=act.get("keyboard_state", "in_game")
                )
            elif act["type"] == "prompt_action":
                await prompt_action(context, act["chat_id"])

    @staticmethod
    async def send_state_change(context, chat_id: int, state: str, message: str = "✅ Стан оновлено"):
        from bot.ui_components.keyboard import get_keyboard_for_state

        await context.bot.send_message(
            chat_id=chat_id,
            text=message,
            reply_markup=get_keyboard_for_state(state)
        )
