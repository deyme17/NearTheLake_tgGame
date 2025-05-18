from game.core.game_settings import GameSettings
from game.core.lake import Lake
from game.core.player import Player
from config import settings

class Game:
    def __init__(self):
        # settings
        self.settings = GameSettings()

        self.players = {}  # {user_id: Player}
        self.state = "waiting"
        self.turn = 1
        self.lake = Lake()
        self.admin_chat_id = None

        self.meeting_active = False
        self.meeting_end_votes = set()

        self.end_game_votes = set()
        self.end_vote_active = False

        self.total_points = 0
        self.turn_points = 0

    def add_player(self, user_id, name):
        """Adds a player to the game"""
        if len(self.players) < self.settings.max_players and user_id not in self.players:
            player = Player(user_id, name)
            self.players[user_id] = player
            
            if self.admin_chat_id is None:
                self.admin_chat_id = user_id
                
            return True, len(self.players)
        return False, len(self.players)


    def all_actions_collected(self):
        """Checks if all players have performed an action"""
        return all(player.current_action is not None for player in self.players.values())

    def check_game_end(self):
        """Checks if the game end has been reached"""
        if self.turn >= self.settings.game_duration_months:
            return True
        return False

    def reset_game(self):
        """Resets the game"""
        for player in self.players.values():
            player.reset()
        self.players.clear()
        self.state = "waiting"
        self.turn = 1
        self.total_points = 0
        self.lake.reset_lake()
        self.meeting_active = False
        self.meeting_end_votes.clear()
        self.end_vote_active = False
        self.end_game_votes.clear()
