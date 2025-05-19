from messages.events_messages import (
    meeting_started_message,
    meeting_finished_message,
    end_meeting,
)
from bot.services.meeting_service import MessengerService
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

class Meeting:
    @staticmethod
    async def start_meeting(context, game):
        game.meeting_active = True
        game.meeting_end_votes.clear()

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(end_meeting, callback_data="end_meeting_vote")]
        ])

        for player in game.players.values():
            await context.bot.send_message(
                chat_id=player.player_id,
                text=meeting_started_message(game),
                reply_markup=keyboard
            )

        # automatic end of the meeting
        context.job_queue.run_once(
            callback=Meeting._auto_end_meeting_job,
            when=game.settings.meeting_duration
        )

    @staticmethod
    async def _auto_end_meeting_job(context):
        game = context.application.bot_data.get("game")
        if game and game.meeting_active:
            actions = Meeting.manual_end_meeting(game)
            await MessengerService.handle_actions(context, actions)

    @staticmethod
    def manual_end_meeting(game):
        if not game.meeting_active:
            return []

        game.meeting_active = False
        game.meeting_end_votes.clear()

        actions = []
        for player in game.players.values():
            actions.append({
                "type": "send_message",
                "chat_id": player.player_id,
                "text": meeting_finished_message,
                "keyboard_state": "in_game"
            })
            actions.append({
                "type": "prompt_action",
                "chat_id": player.player_id
            })

        return actions

    @staticmethod
    async def _execute_action(act, context):
        from bot.ui_components.promt_action import prompt_action
        from bot.services.messenger_service import Me

        if act["type"] == "send_message":
            await MessengerService.send(
                context=context,
                chat_id=act["chat_id"],
                text=act["text"],
                state=act.get("keyboard_state", "in_game")
            )
        elif act["type"] == "prompt_action":
            await prompt_action(context, act["chat_id"])
