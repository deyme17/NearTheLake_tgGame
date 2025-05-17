from config.settings import ACTION_DUMP_CLEAR_VAL, PENALTY_SCORE
from config.constants import ACTION_PENALTY
from .action import BaseAction

class DumpAction(BaseAction):
    """Class of the action 'dump'"""
    def apply(self, game, player):
        game.lake.update_quality(ACTION_DUMP_CLEAR_VAL)
        score = game.lake.get_current_scores()[0]

        has_penalty = any(player.current_action == ACTION_PENALTY for player in game.players.values())
        if has_penalty:
            player.add_points(PENALTY_SCORE)
        else:
            player.add_points(score)