from bot.services.player_service import PlayerService

class PlayerController:
    @staticmethod
    async def register_player(update, context):
        game = context.application.bot_data.get("game")
        await PlayerService.register(update, context, game)