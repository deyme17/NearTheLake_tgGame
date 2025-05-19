from .action import BaseAction

class DumpAction(BaseAction):
    """Class of the action 'dump'"""
    def apply(self, game, player):
        game.lake.update_quality(game.settings.action_dump_clear_val)
        if getattr(game, 'has_penalty', False):
            player.add_points(game.settings.penalty_score)
        else:
            score = game.lake.get_current_scores()[0]
            player.add_points(score)