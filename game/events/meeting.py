from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from messages.events_messages import (
    meeting_started_message,
    meeting_finished_message,
    no_communication_message,
    end_meeting
)
from bot.services.message_broadcast_service import MessageBroadcastService
from bot.services.keyboard_messenger import KeyboardMessenger
from bot.ui_components.promt_action import prompt_action
from config.settings import MEETING_DURATION


class Meeting:
    @staticmethod
    async def start_meeting(context, game):
        game.meeting_active = True
        game.meeting_end_votes.clear()

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(end_meeting, callback_data="end_meeting_vote")]
        ])

        await MessageBroadcastService.send_all(
            bot=context.bot,
            players=game.players,
            text=meeting_started_message(game),
            reply_markup=keyboard
        )

        # auto end meeting
        context.job_queue.run_once(
            callback=Meeting.auto_end_meeting_job,
            when=MEETING_DURATION
        )

    @staticmethod
    async def auto_end_meeting_job(context):
        game = context.application.bot_data.get("game")
        if game and game.meeting_active:
            await Meeting.manual_end_meeting(context, game)

    @staticmethod
    async def manual_end_meeting(context, game):
        if not game.meeting_active:
            return
    
        game.meeting_active = False
        game.meeting_end_votes.clear()

        for player in game.players.values():
            await KeyboardMessenger.send(
                bot=context.bot,
                chat_id=player.player_id,
                text=meeting_finished_message,
                state="in_game"
            )
            await prompt_action(context, player.player_id)
