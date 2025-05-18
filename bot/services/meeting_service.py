from telegram import Update
from telegram.ext import CallbackContext
from messages.events_messages import (
    meeting_inactive_message,
    voted_message,
    vote_enrolled_message,
    no_communication_message,
)
from messages.state_messages import not_member_message
from bot.services.messenger_service import MessengerService


class MeetingService:
    @staticmethod
    async def forward_player_message(update: Update, context: CallbackContext, game):
        user_id = update.effective_user.id

        if not game or user_id not in game.players:
            await update.message.reply_text(not_member_message)
            return

        if not game.meeting_active:
            await update.message.reply_text(no_communication_message)
            return

        sender = game.players[user_id]
        message_text = update.message.text

        for other_player in game.players.values():
            if other_player.player_id != user_id:
                await context.bot.send_message(
                    chat_id=other_player.player_id,
                    text=f"💬 {sender.name}: {message_text}"
                )

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
            from game.events.meeting import Meeting
            actions = Meeting.manual_end_meeting(game)
            await MessengerService.handle_actions(context, actions)

