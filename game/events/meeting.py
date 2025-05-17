from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.ui_components.promt_action import prompt_action
from config.settings import MEETING_DURATION
from messages.events_messages import meeting_finished_messege, end_meeting, meeting_started_messege

class Meeting:
    @staticmethod
    async def start_meeting(context, game):
        game.meeting_active = True
        game.meeting_end_votes.clear()

        keyboard = [
            [InlineKeyboardButton(end_meeting, callback_data="end_meeting_vote")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        for user_id in game.players:
            await context.bot.send_message(
                chat_id=user_id,
                text=meeting_started_messege(),
                reply_markup=reply_markup,
            )

        context.job_queue.run_once(
            Meeting.auto_end_meeting, MEETING_DURATION,
            data={"game": game}, name="end_meeting"
        )

    @staticmethod
    async def auto_end_meeting(context):
        game = context.job.data["game"]
        if game.meeting_active:
            await Meeting.manual_end_meeting(context, game)

    @staticmethod
    async def manual_end_meeting(context, game):
        game.meeting_active = False
        game.meeting_end_votes.clear()

        for user_id in game.players:
            await context.bot.send_message(chat_id=user_id, text=meeting_finished_messege)

        for user_id in game.players.keys():
            await prompt_action(context, user_id)
