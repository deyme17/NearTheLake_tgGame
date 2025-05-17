from game.gamelogic.action_service import ActionService
from messages.game_message_service import GameMessageService
from game.gamelogic.game_flow_manager import GameFlowManager
from bot.ui_components.promt_action import prompt_action
from config.settings import MEETING_INTERVAL, FLOOD_INTERVAL, GAME_DURATION_MONTHS
from game.events.meeting import Meeting
from game.events.spring_flood import SpringFlood
from messages.state_messages import game_finished_message

class TurnProcessor:
    def __init__(self):
        self.action_service = ActionService()

    async def process_turn(self, game, context):
        if not self._check_preconditions(game):
            return

        previous_quality = (game.lake.level, game.lake.position)

        self._apply_all_actions(game)
        await self._notify_players_results(game, context, previous_quality)

        game.turn += 1
        if await self._advance_turn_and_check_end(game, context):
            return

        await self._trigger_events(game, context)
        await self._prompt_next_actions(game, context)

    def _check_preconditions(self, game):
        return not game.meeting_active and game.all_actions_collected()

    def _apply_all_actions(self, game):
        for player in game.players.values():
            self.action_service.apply_action(game, player)
            player.clear_action()

    async def _clear_previous_turn_results(self, player, context):
        if hasattr(player, "last_message_id") and player.last_message_id:
            try:
                await context.bot.delete_message(chat_id=player.player_id, message_id=player.last_message_id)
            except:
                pass

    async def _notify_players_results(self, game, context, previous_quality):
        next_scores = game.lake.get_current_scores()
        current_quality = (
            game.lake.level,
            game.lake.position,
            next_scores[0],
            next_scores[1]
        )

        for player in game.players.values():
            await self._clear_previous_turn_results(player, context)

            turn_info = GameMessageService.get_turn_info(
                previous_quality,
                current_quality,
                game.turn,
                GAME_DURATION_MONTHS,
                player.current_turn_points,
                player.score
            )

            msg = await context.bot.send_message(chat_id=player.player_id, text=turn_info)
            player.last_message_id = msg.message_id

            player.clear_curr_turn_points()

    async def _advance_turn_and_check_end(self, game, context):
        if game.check_game_end():
            await GameFlowManager.end_game(game, context)
            return True
        return False

    async def _trigger_events(self, game, context):
        if game.turn % FLOOD_INTERVAL == 0:
            flood_message = SpringFlood.start_flood(game.lake)
            if flood_message:
                for player in game.players.values():
                    await context.bot.send_message(chat_id=player.player_id, text=flood_message)

        if game.turn % MEETING_INTERVAL == 0:
            await Meeting.start_meeting(context, game)

    async def _prompt_next_actions(self, game, context):
        if game.turn % MEETING_INTERVAL != 0:
            for player in game.players.values():
                await prompt_action(context, player.player_id)