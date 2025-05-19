from bot.ui_components.promt_action import prompt_action
from bot.services.messenger_service import MessengerService
from bot.services.session_service import SessionService
from messages.general_messages import start_message
from messages.state_messages import comeback_to_menu_message, game_finished_message, no_game_messege
from messages.game_message_service import GameMessageService

from bot.ui_components.promt_action import prompt_action
from bot.services.messenger_service import MessengerService
from bot.services.session_service import SessionService
from bot.ui_components.keyboard import get_keyboard_for_state
from messages.general_messages import start_message
from messages.state_messages import comeback_to_menu_message, game_finished_message, no_game_messege
from messages.action_messages import first_turn_message
from messages.game_message_service import GameMessageService

class GameCoordinator:
    @staticmethod
    async def start_game(game, context):
        if game.state != "waiting":
            return

        game.state = "in_progress"
        player_ids = list(game.players.keys())
        player_list = "\n".join([f"- {p.name}" for p in game.players.values()])

        SessionService.set_all(context, player_ids, "in_game")

        await MessengerService.send_all(
            bot=context.bot,
            players=game.players,
            text=start_message(player_list)
        )

        for player in game.players.values():
            await MessengerService.send_state_change(
                context=context,
                chat_id=player.player_id,
                state="in_game",
                message=first_turn_message
            )
            await prompt_action(context, player.player_id)

    @staticmethod
    async def end_game(game, context, update=None):
        if game.state != "in_progress":
            if update:
                await update.message.reply_text(no_game_messege)
            return

        game.state = "ended"
        results = GameMessageService.get_winner_message(game.players, game_ended=True)

        SessionService.set_all(context, list(game.players.keys()), "idle")

        await MessengerService.send_all(
            bot=context.bot,
            players=game.players,
            text=game_finished_message
        )

        for player in game.players.values():
            await MessengerService.send(
                context=context,
                chat_id=player.player_id,
                text=results,
                state="idle"
            )
            await MessengerService.send(
                context=context,
                chat_id=player.player_id,
                text=comeback_to_menu_message,
                state="idle"
            )

        game.reset_game()