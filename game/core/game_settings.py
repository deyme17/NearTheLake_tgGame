from config import settings

class GameSettings:
    def __init__(self):
        self.max_players = settings.MAX_PLAYERS
        self.game_duration_months = settings.GAME_DURATION_MONTHS
        self.meeting_interval = settings.MEETING_INTERVAL
        self.bonus_score = settings.BONUS_SCORE
        self.penalty_score = settings.PENALTY_SCORE

    def update(self, key: str, value: int) -> bool:
        attr = key.lower()
        if hasattr(self, attr):
            setattr(self, attr, value)
            return True
        return False