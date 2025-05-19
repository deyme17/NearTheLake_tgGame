from bot.services.meeting_service import MeetingService
from config.helpers import get_game

async def handle_end_meeting_vote(update, context):
    game = get_game(context)
    await MeetingService.handle_end_vote(update, context, game)