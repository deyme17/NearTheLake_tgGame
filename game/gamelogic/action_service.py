from config.constants import ACTION_DUMP, ACTION_CLEAN, ACTION_BONUS, ACTION_PENALTY

from game.actions.dump_action import DumpAction
from game.actions.clean_action import CleanAction
from game.actions.penalty_action import PenaltyAction
from game.actions.bonus_action import BonusAction

class ActionService:
    def __init__(self):
        self.action_map = {
            ACTION_DUMP: DumpAction,
            ACTION_CLEAN: CleanAction,
            ACTION_PENALTY: PenaltyAction,
            ACTION_BONUS: BonusAction,
        }

    def apply_action(self, game, player):
        action_code = player.current_action
        action_class = self.action_map.get(action_code)

        if action_class:
            action_instance = action_class()
            action_instance.apply(game, player)