from telegram import Update
from telegram.ext import CallbackContext

from messages.events_messages import (
    meeting_inactive_message,
    voted_message,
    vote_enrolled_message
)
from game.events.meeting import Meeting


class MeetingVoteService:
    @staticmethod
    async def handle_end_vote(update: Update, context: CallbackContext, game):
        user_id = update.effective_user.id

        if not game or not game.meeting_active:
            await update.callback_query.answer(meeting_inactive_message)
            return

        if user_id in game.meeting_end_votes:
            await update.callback_query.answer(voted_message)
            return

        game.meeting_end_votes.add(user_id)
        await update.callback_query.answer(vote_enrolled_message)

        if len(game.meeting_end_votes) == len(game.players):
            await Meeting.manual_end_meeting(context, game)
