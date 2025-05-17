from .action import BaseAction

class PenaltyAction(BaseAction):
    """Class of the action 'penalty'"""
    def apply(self, game, player):
        penalty_cost = -len(game.players)
        player.add_points(penalty_cost)