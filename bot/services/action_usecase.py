from game.gamelogic.turn_processor import TurnProcessor
from messages.state_messages import not_registered_message, game_started_negative_messege
from messages.action_messages import (get_choice_message, get_chosen_action_message, 
                                      wait_others_message, have_chosen_action)
from config.helpers import get_game
from telegram.error import BadRequest
from game.core.game_coordinator import GameCoordinator
from bot.ui_components.promt_action import prompt_action

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
        await query.answer(get_chosen_action_message(action))

        try:
            await query.edit_message_text(text=get_choice_message(action))
        except BadRequest as e:
            if "Message is not modified" not in str(e):
                raise

        if game.all_actions_collected():
            actions = await TurnProcessor().process_turn(game, context)
            for act in actions:
                await ActionUseCase._execute_act(act, context, game)
        else:
            await context.bot.send_message(
                chat_id=user_id,
                text=wait_others_message
            )

    @staticmethod
    async def _execute_act(act, context, game):
        match act["type"]:
            case "send_message":
                await context.bot.send_message(
                    chat_id=act["chat_id"],
                    text=act["text"]
                )
            case "prompt_action":
                await prompt_action(context, act["chat_id"])
            case "start_meeting":
                from game.events.meeting import Meeting
                await Meeting.start_meeting(context, game)
            case "end_game":
                await GameCoordinator.end_game(game, context)