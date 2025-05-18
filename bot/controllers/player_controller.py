from bot.services.player_service import PlayerService
from game.gamelogic.game_engine import GameEngine

class PlayerController:
    @staticmethod
    async def register_player(update, context):
        game = context.application.bot_data.get("game")
        success, current_count = await PlayerService.register(update, context, game)

        if success and current_count == game.settings.max_players:
            await GameEngine(game, context).start_game()