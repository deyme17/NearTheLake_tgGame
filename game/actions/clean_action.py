from .action import BaseAction

class CleanAction(BaseAction):
    def apply(self, game, player):
        game.lake.update_quality(game.settings.action_clean_clear_val)
        score = game.lake.get_current_scores(game)[1]
        player.add_points(score)
        if getattr(game, 'has_bonus', False):
            player.add_points(game.settings.bonus_score)

