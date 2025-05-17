from config.settings import ACTION_CLEAN_CLEAR_VAL, BONUS_SCORE
from config.constants import ACTION_BONUS
from .action import BaseAction

class CleanAction(BaseAction):
    """Class of the action 'clean'"""
    def apply(self, game, player):
        game.lake.update_quality(ACTION_CLEAN_CLEAR_VAL)
        score = game.lake.get_current_scores()[1]

        player.add_points(score)

        has_bonus = any(player.current_action == ACTION_BONUS for player in game.players.values())
        if has_bonus:
            player.add_points(BONUS_SCORE)


