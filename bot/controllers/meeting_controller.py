from telegram import Update
from telegram.ext import CallbackContext
from bot.services.meeting_vote_service import MeetingVoteService
from config.helpers import get_game

class MeetingController:
    @staticmethod
    async def handle_end_vote(update: Update, context: CallbackContext):
        game = get_game(context)
        await MeetingVoteService.handle_end_vote(update, context, game)