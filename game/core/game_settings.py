from config import settings

class GameSettings:
    def __init__(self):
        self.max_players = settings.MAX_PLAYERS
        self.game_duration_months = settings.GAME_DURATION_MONTHS
        self.action_dump_clear_val = settings.ACTION_DUMP_CLEAR_VAL
        self.action_clean_clear_val = settings.ACTION_CLEAN_CLEAR_VAL
        self.penalty_score = settings.PENALTY_SCORE
        self.bonus_score = settings.BONUS_SCORE
        self.flood_clean_min = settings.FLOOD_CLEAN_MIN
        self.flood_clean_max = settings.FLOOD_CLEAN_MAX
        self.meeting_interval = settings.MEETING_INTERVAL
        self.meeting_duration = settings.MEETING_DURATION
        self.flood_interval = settings.FLOOD_INTERVAL
        self.dump_scores = settings.DUMP_SCORES
        self.clean_scores = settings.CLEAN_SCORES

    def update(self, key: str, value: int) -> bool:
        attr = key.lower()
        if hasattr(self, attr):
            setattr(self, attr, value)
            return True
        return False
