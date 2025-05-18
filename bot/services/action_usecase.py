from game.gamelogic.turn_processor import TurnProcessor
from messages.state_messages import not_registered_message
from messages.state_messages import game_started_negative_messege
from messages.action_messages import choice_message, chosen_action_message, wait_others_message, have_chosen_action
from config.helpers import get_game
from telegram.error import BadRequest

class ActionUseCase:
    @staticmethod
    async def handle_action(update, context):
        game = get_game(context)
        query = update.callback_query
        action = query.data
        user_id = query.from_user.id

        if game.state != "in_progress":
            await query.answer(game_started_negative_messege)
            return

        if user_id not in game.players:
            await query.answer(not_registered_message)
            return

        player = game.players[user_id]
        if player.current_action is not None:
            await query.answer(have_chosen_action)
            return

        player.set_action(action)
        await query.answer(chosen_action_message(action))

        try:
            await query.edit_message_text(text=choice_message(action))
        except BadRequest as e:
            if "Message is not modified" not in str(e):
                raise

        if game.all_actions_collected():
            await TurnProcessor().process_turn(game, context)
        else:
            await context.bot.send_message(
                chat_id=user_id,
                text=wait_others_message
            )