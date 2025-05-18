from bot.command_managers.idle_command_manager import IdleStateCommandManager
from bot.command_managers.in_game_command_manager import InGameStateCommandManager
from bot.command_managers.waiting_lobby_command_manager import WaitingLobbyCommandManager
from bot.services.state_service import StateService

class GameStateRouter:
    def __init__(self):
        self.managers = {
            "idle": IdleStateCommandManager(),
            "in_game": InGameStateCommandManager(),
            "waiting_lobby": WaitingLobbyCommandManager(),
        }

    def get_manager(self, context, user_id):
        state = StateService.get_state(context, user_id)
        return self.managers.get(state)
