from bot.services.meeting_service import MeetingService

async def handle_end_meeting_vote(update, context):
    game = context.application.bot_data["game"]
    await MeetingService.handle_end_vote(update, context, game)