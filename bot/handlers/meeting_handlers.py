from bot.controllers.meeting_controller import MeetingController

async def handle_end_meeting_vote(update, context):
    await MeetingController.handle_end_vote(update, context)