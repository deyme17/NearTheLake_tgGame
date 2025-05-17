from abc import ABC, abstractmethod

class BaseAction(ABC):
    """Abstract class of a player action"""
    @abstractmethod
    def apply(self, game, player):
        """Applies an action to a player"""
        pass