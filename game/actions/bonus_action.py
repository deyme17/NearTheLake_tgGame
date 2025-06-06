from .action import BaseAction

class BonusAction(BaseAction):
    """Class of the action 'bonus'"""
    def apply(self, game, player):
        bonus_cost = -len(game.players)
        player.add_points(bonus_cost)