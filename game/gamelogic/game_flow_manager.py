from bot.ui_components.promt_action import prompt_action
from bot.ui_components.keyboard import get_keyboard_for_state
from messages.game_message_service import GameMessageService
from bot.services.state_service import StateService
from bot.services.ui_refresh_service import UIRefreshService
from messages.start_message import start_message
from messages.game_state_messages import game_finished_message, comeback_to_menu_message, no_game_messege
from messages.action_messages import first_action
from bot.services.ui_refresh_service import UIRefreshService
from bot.services.state_service import StateService
from bot.ui_components.promt_action import prompt_action
from messages.start_message import start_message

class GameFlowManager:
    @staticmethod
    async def start_game(game, context):
        game.state = "in_progress"

        player_list = "\n".join([f"- {player.name}" for player in game.players.values()])
        start_msg = start_message(player_list)

        StateService.set_all(context, list(game.players.keys()), "in_game")

        for player in game.players.values():
            await context.bot.send_message(chat_id=player.player_id, text=start_msg)

            await UIRefreshService.update_keyboard(
                bot=context.bot,
                chat_id=player.player_id,
                text=first_action,
                state="in_game"
            )
            await prompt_action(context, player.player_id)


    @staticmethod
    async def end_game(game, context, update=None):
        if game.state != "in_progress":
            if update:
                await update.message.reply_text(no_game_messege)
            return

        game.state = "ended"
        results = GameMessageService.get_winner_message(game.players, True)

        StateService.set_all(context, list(game.players.keys()), "idle")

        for player in game.players.values():
            await context.bot.send_message(
                chat_id=player.player_id,
                text=game_finished_message
            )
            await context.bot.send_message(
                chat_id=player.player_id,
                text=results
            )
            await UIRefreshService.update_keyboard(
                bot=context.bot,
                chat_id=player.player_id,
                text=comeback_to_menu_message,
                state="idle"
            )

        game.reset_game()