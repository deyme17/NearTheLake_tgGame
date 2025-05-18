from abc import ABC, abstractmethod
from telegram import Update
from telegram.ext import CallbackContext

class BaseCommand(ABC):
    @abstractmethod
    def matches(self, text: str) -> bool:
        pass

    @abstractmethod
    async def execute(self, update: Update, context: CallbackContext, game):
        pass
