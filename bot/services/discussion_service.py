from messages.state_messages import not_member_message
from messages.events_messages import no_communication_message

class MessageRelayService:
    @staticmethod
    async def forward_player_message(update, context, game):
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
