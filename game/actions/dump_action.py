from config.settings import ACTION_DUMP_CLEAR_VAL
from .action import BaseAction

class DumpAction(BaseAction):
    """Class of the action 'dump'"""
    def apply(self, game, player):
        game.lake.update_quality(ACTION_DUMP_CLEAR_VAL)
        if getattr(game, 'has_penalty', False):
            player.add_points(game.settings.penalty_score)
        else:
            score = game.lake.get_current_scores()[0]
            player.add_points(score)