from config.settings import ACTION_CLEAN_CLEAR_VAL
from .action import BaseAction

class CleanAction(BaseAction):
    def apply(self, game, player):
        game.lake.update_quality(ACTION_CLEAN_CLEAR_VAL)
        score = game.lake.get_current_scores()[1]
        player.add_points(score)
        if getattr(game, 'has_bonus', False):
            player.add_points(game.settings.bonus_score)

