from bot.ui_components.promt_action import prompt_action
from messages.game_message_service import GameMessageService
from messages.start_message import start_message
from messages.game_state_messages import game_finished_message, new_game_message, no_game_messege

class GameFlowManager:
    @staticmethod
    async def start_game(game, context):
        game.state = "in_progress"

        player_list = "\n".join([f"- {player.name}" for player in game.players.values()])
        start_msg = start_message(player_list)

        for player in game.players.values():
            await context.bot.send_message(chat_id=player.player_id, text=start_msg)
            await prompt_action(context, player.player_id)

    @staticmethod
    async def end_game(game, context, update=None):
        if game.state != "in_progress":
            if update:
                await update.message.reply_text(no_game_messege)
            return

        game.state = "ended"
        results = GameMessageService.get_winner_message(game.players, True)

        for player in game.players.values():
            await context.bot.send_message(chat_id=player.player_id, text=game_finished_message)
            await context.bot.send_message(chat_id=player.player_id, text=results)

        game.reset_game()

        if update:
            await update.message.reply_text(new_game_message)
