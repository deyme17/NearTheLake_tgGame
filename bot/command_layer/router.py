from bot.command_layer.command_managers.idle_command_manager import IdleStateCommandManager
from bot.command_layer.command_managers.in_game_command_manager import InGameStateCommandManager
from bot.command_layer.command_managers.waiting_lobby_command_manager import WaitingLobbyCommandManager
from bot.services.session_service import SessionService

class GameStateRouter:
    def __init__(self):
        self.managers = {
            "idle": IdleStateCommandManager(),
            "in_game": InGameStateCommandManager(),
            "waiting_lobby": WaitingLobbyCommandManager(),
        }

    def get_manager(self, context, user_id):
        state = SessionService.get_state(context, user_id)
        return self.managers.get(state)
