from config.settings import MAX_PLAYERS, GAME_DURATION_MONTHS, SCORE_PENALTY, SCORE_REWARD_CLEAN
from game.lake import Lake
from game.events import spring_flood
import random


class Game:
    def __init__(self):
        self.players = {}  # {user_id: {"name": player_name, "score": 0, "current_action": None}}
        self.max_players = MAX_PLAYERS
        self.state = "waiting"  # waiting, in_progress, ended
        self.turn = 0
        self.lake = Lake()

        self.decision_1_scores = [5, 19, 26, 33, 41, 51, 64, 80, 100, 110, 121, 133, 146, 161, 177]
        self.decision_2_scores = [-20, -8, -3, 3, 7, 14, 21, 28, 35, 48, 63, 79, 92, 111, 127]


    def add_player(self, user_id, name):
        if len(self.players) < self.max_players and user_id not in self.players:
            self.players[user_id] = {"name": name, "score": 0, "current_action": None}
            return True
        return False
    

    def start_game(self):
        if len(self.players) == self.max_players:
            self.state = "in_progress"
            return True
        return False
    

    def collect_actions(self, actions):
        for user_id, action in actions.items():
            if user_id in self.players:
                self.players[user_id]["current_action"] = action


    def apply_penalty(self, player_data, score_1):
        player_data["score"] -= SCORE_PENALTY
        player_data["score"] -= score_1

    def apply_reward(self, player_data):
        player_data["score"] += SCORE_REWARD_CLEAN


    def all_actions_collected(self):
        """Перевіряє, чи всі гравці виконали свої дії."""
        return all(player["current_action"] is not None for player in self.players.values())


    async def process_turn(self, context, admin_chat_id):

        if not self.all_actions_collected():
            await context.bot.send_message(chat_id=admin_chat_id, text="Не всі гравці виконали свої дії.")
            return

        previous_quality = self.lake.water_quality
        has_penalty = any(player["current_action"] == "штраф" for player in self.players.values())

        # Основна логіка ходів
        for user_id, player_data in self.players.items():
            action = player_data["current_action"]
            row_index = max(0, min(self.lake.water_quality, 14)) 
            score_1 = self.decision_1_scores[row_index]
            score_2 = self.decision_2_scores[row_index]

            if action == "скидання":
                if has_penalty:
                    self.apply_penalty(player_data, score_1)
                else:
                    player_data["score"] += score_1
                    self.lake.update_quality(-1)

            elif action == "очищення":
                player_data["score"] += score_2
                self.lake.update_quality(1)

            elif action == "штраф":
                for target_id, target_data in self.players.items():
                    if target_data["current_action"] == "скидання":
                        self.apply_penalty(target_data, score_1)
                player_data["score"] -= len(self.players)

            elif action == "премія":
                for target_id, target_data in self.players.items():
                    if target_data["current_action"] == "очищення":
                        self.apply_reward(target_data)
                player_data["score"] -= len(self.players)

        flood_message = spring_flood(self.lake, self.turn)

        # Очищення поточних дій
        for player_data in self.players.values():
            player_data["current_action"] = None

        self.turn += 1

        # Формуємо повідомлення про стан озера
        lake_status_message = self.get_lake_status(previous_quality, score_1, score_2)

        # Відправляємо оновлення всім гравцям
        for user_id in self.players.keys():
            await context.bot.send_message(chat_id=user_id, text=lake_status_message)
            if flood_message:  # Відправляємо повідомлення про паводок, якщо він був
                await context.bot.send_message(chat_id=user_id, text=flood_message)


    def get_lake_status(self, previous_quality, score_1, score_2):
        current_quality = self.lake.water_quality

        if current_quality >= 4:
            water_status = "Чиста вода"
        elif -3 <= current_quality <= 3:
            water_status = "Промислова чиста вода"
        else:
            water_status = "Брудна вода"

        quality_change = current_quality - previous_quality
        row_position = max(-8, min(current_quality, 6)) + 8

        result = (
            f"🌊 Стан озера: {water_status}\n"
            f"🔄 Зміна якості води: {'+' if quality_change > 0 else ''}{quality_change}\n"
            f"📊 Поточна позиція в матриці: {row_position - 8} (рівень: {current_quality})\n"
            f"🏆 Бали за рішення:\n"
            f"   - Рішення №1 (скидання): {score_1}\n"
            f"   - Рішення №2 (очищення): {score_2}\n"
        )
        return result
    

    def check_game_end(self):
        if self.turn >= GAME_DURATION_MONTHS:
            self.state = "ended"
            return True
        return False

    def get_winner(self):
        if self.state != "ended":
            return "Гра ще не завершена."

        sorted_players = sorted(
            self.players.items(),
            key=lambda item: item[1]["score"],
            reverse=True
        )

        table = "Результати гри:\n"
        table += "{:<4} {:<20} {:<10}\n".format("Місце", "Гравець", "Очки")
        table += "-" * 40 + "\n"

        for rank, (user_id, player_data) in enumerate(sorted_players, start=1):
            table += "{:<4} {:<20} {:<10}\n".format(
                rank,
                player_data["name"],
                player_data["score"]
            )

        return table
