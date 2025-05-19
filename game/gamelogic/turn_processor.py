from game.gamelogic.action_executor import ActionService
from config.constants import ACTION_BONUS, ACTION_PENALTY
from game.events.meeting import Meeting
from game.events.spring_flood import SpringFlood
from messages.game_message_service import GameMessageService

class TurnProcessor:
    def __init__(self):
        self.action_service = ActionService()

    async def process_turn(self, game, context):
        if not self._check_preconditions(game):
            return []

        previous_quality = (game.lake.level, game.lake.position)

        self._collect_flags(game)
        self._apply_all_actions(game)

        await self._generate_result_messages(game, previous_quality, context)

        game.turn += 1

        if game.check_game_end():
            return [{"type": "end_game"}]

        messages = self._trigger_events(game)
        messages += self._generate_next_action_prompts(game)
        return messages

    def _check_preconditions(self, game):
        return not game.meeting_active and game.all_actions_collected()

    def _apply_all_actions(self, game):
        for player in game.players.values():
            self.action_service.apply_action(game, player)
            player.clear_action()

        delattr(game, 'has_bonus')
        delattr(game, 'has_penalty')

    def _collect_flags(self, game):
        game.has_bonus = any(p.current_action == ACTION_BONUS for p in game.players.values())
        game.has_penalty = any(p.current_action == ACTION_PENALTY for p in game.players.values())

    async def _generate_result_messages(self, game, previous_quality, context):
        next_scores = game.lake.get_current_scores(game)
        current_quality = (
            game.lake.level,
            game.lake.position,
            next_scores[0],
            next_scores[1]
        )

        for player in game.players.values():
            turn_info = GameMessageService.get_turn_info(
                previous_quality,
                current_quality,
                game.turn,
                game.settings.game_duration_months,
                player.current_turn_points,
                player.score
            )

            await self._delete_previous_messages(player, context)

            msg = await context.bot.send_message(
                chat_id=player.player_id,
                text=turn_info
            )
            player.last_result_msg_id = msg.message_id
            player.clear_curr_turn_points()

    async def _delete_previous_messages(self, player, context):            
        if player.last_result_msg_id:
            try:
                await context.bot.delete_message(
                    chat_id=player.player_id,
                    message_id=player.last_result_msg_id
                )
            except:
                pass

    def _trigger_events(self, game):
        results = []

        if game.turn % game.settings.flood_interval == 0:
            flood_message = SpringFlood.start_flood(game.lake, game)
            if flood_message:
                for player in game.players.values():
                    results.append({
                        "type": "send_message",
                        "chat_id": player.player_id,
                        "text": flood_message
                    })

        if game.turn % game.settings.meeting_interval == 0:
            results.append({"type": "start_meeting"})

        return results

    def _generate_next_action_prompts(self, game):
        if game.turn == 1 or game.turn % game.settings.meeting_interval == 0:
            return []

        return [
            {"type": "prompt_action", "chat_id": player.player_id}
            for player in game.players.values()
        ]
