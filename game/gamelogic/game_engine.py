from bot.services.state_service import StateService
from bot.services.ui_refresh_service import UIRefreshService
from messages.general_messages import start_message
from messages.state_messages import game_finished_message, no_game_messege, comeback_to_menu_message
from messages.action_messages import first_action
from bot.ui_components.promt_action import prompt_action
from messages.game_message_service import GameMessageService


class GameEngine:
    def __init__(self, game, context):
        self.game = game
        self.context = context
        self.bot = context.bot

    async def start_game(self):
        self.game.state = "in_progress"
        player_ids = list(self.game.players.keys())
        player_list = "\n".join([f"- {p.name}" for p in self.game.players.values()])

        StateService.set_all(self.context, player_ids, "in_game")

        for player in self.game.players.values():
            await self.bot.send_message(chat_id=player.player_id, text=start_message(player_list))
            await UIRefreshService.update_keyboard(
                bot=self.bot,
                chat_id=player.player_id,
                text=first_action,
                state="in_game"
            )
            await prompt_action(self.context, player.player_id)

    async def end_game(self, update=None):
        if self.game.state != "in_progress":
            if update:
                await update.message.reply_text(no_game_messege)
            return

        self.game.state = "ended"
        results = GameMessageService.get_winner_message(self.game.players, game_ended=True)

        StateService.set_all(self.context, list(self.game.players.keys()), "idle")

        for player in self.game.players.values():
            await self.bot.send_message(chat_id=player.player_id, text=game_finished_message)
            await self.bot.send_message(chat_id=player.player_id, text=results)
            await UIRefreshService.update_keyboard(
                bot=self.bot,
                chat_id=player.player_id,
                text=comeback_to_menu_message,
                state="idle"
            )

        self.game.reset_game()
