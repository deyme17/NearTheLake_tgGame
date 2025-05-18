class MessageBroadcastService:
    @staticmethod
    async def send_all(bot, players: dict, text: str, reply_markup=None):
        if callable(text):
            text = text()
        for player in players.values():
            await bot.send_message(
                chat_id=player.player_id,
                text=text,
                reply_markup=reply_markup
            )

    @staticmethod
    async def send_all_except(bot, players: dict, excluded_id: int, text: str, reply_markup=None):
        if callable(text):
            text = text()
        for player in players.values():
            if player.player_id != excluded_id:
                await bot.send_message(
                    chat_id=player.player_id,
                    text=text,
                    reply_markup=reply_markup
                )

