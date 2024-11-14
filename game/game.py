from config.settings import MAX_PLAYERS

class Game:
    def __init__(self):
        self.players = {}  # {user_id: {"name": player_name, "score": 0}}
        self.max_players = MAX_PLAYERS
        self.state = "waiting"  # waiting, in_progress, ended

    def add_player(self, user_id, name):
        if len(self.players) < self.max_players and user_id not in self.players:
            self.players[user_id] = {"name": name, "score": 0}
            return True
        return False

    def start_game(self):
        if len(self.players) == self.max_players:
            self.state = "in_progress"
            return True
        return False
