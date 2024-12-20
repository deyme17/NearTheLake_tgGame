from bot.controller import end_game
from config.settings import MAX_PLAYERS, GAME_DURATION_MONTHS, SCORE_PENALTY, SCORE_REWARD_CLEAN, MEETING_DURATION, MEETING_INTERVAL, ACTION_1_CLEAR_VAL, ACTION_2_CLEAR_VAL
from game.lake import Lake
from game.events import spring_flood, start_meeting
from bot.utils import prompt_action



class Game:
    def __init__(self):
        self.players = {}  # {user_id: {"name": player_name, "score": 0, "current_action": None}}
        self.max_players = MAX_PLAYERS
        self.state = "waiting"  # waiting, in_progress, ended
        self.turn = 0
        self.lake = Lake()
        self.admin_chat_id = None

        self.meeting_active = False
        self.meeting_end_votes = set()  # Гравці, які натиснули "Закінчити нараду"

        self.decision_1_scores = [5, 19, 26, 33, 41, 51, 64, 80, 100, 110, 121, 133, 146, 161, 177]
        self.decision_2_scores = [-20, -8, -3, 3, 7, 14, 21, 28, 35, 48, 63, 79, 92, 111, 127]

        self.total_points = 0  
        self.turn_points = 0 


# !!!!!!!!!!!
    async def process_turn(self, context):
        """Обробка ходу гри."""
        if self.meeting_active:
            return

        if not self.all_actions_collected():
            return

        # Збереження початкового стану балів
        previous_quality = (self.lake.level, self.lake.position)
        initial_scores = self.lake.get_current_scores()  # Збереження балів до змін

        has_penalty = any(player["current_action"] == "3" for player in self.players.values())

        # Скидання очок за хід
        self.turn_points = 0

        # Обробка дій гравців
        for user_id, player_data in self.players.items():
            action = player_data["current_action"]
            earned_points = 0  # Очки гравця за поточний хід

            if action == "1":
                self.lake.update_quality(ACTION_1_CLEAR_VAL)
                if has_penalty:
                    self.apply_penalty(player_data, initial_scores[0])  # Використовуємо збережені бали
                else:
                    earned_points = initial_scores[0]
                    player_data["score"] += earned_points
            elif action == "2":
                self.lake.update_quality(ACTION_2_CLEAR_VAL)
                earned_points = initial_scores[1]  # Використовуємо збережені бали
                player_data["score"] += earned_points
            elif action == "3":
                for target_id, target_data in self.players.items():
                    if target_data["current_action"] == "1":
                        self.apply_penalty(target_data, initial_scores[0])  # Використовуємо збережені бали
                earned_points = -len(self.players)
                player_data["score"] += earned_points
            elif action == "4":
                for target_id, target_data in self.players.items():
                    if target_data["current_action"] == "2":
                        self.apply_reward(target_data)
                earned_points = -len(self.players)
                player_data["score"] += earned_points

            self.turn_points += earned_points  # Додаємо очки гравця до очок ходу
            player_data["current_action"] = None

        self.total_points += self.turn_points  # Оновлюємо сумарні очки

        # Формуємо статус озера і результати
        lake_status_message = self.get_turn_info(previous_quality, initial_scores[0], initial_scores[1])

        # Надсилаємо повідомлення
        for user_id in self.players.keys():
            await context.bot.send_message(chat_id=user_id, text=lake_status_message)

        self.turn += 1
        if self.check_game_end():
            winners_message = self.get_winner()
            for user_id in self.players.keys():
                await context.bot.send_message(chat_id=user_id, text="🏁 Гра завершена!")
                await context.bot.send_message(chat_id=user_id, text=winners_message)
            self.reset_game()
            return

        # Перевіряємо паводки
        if self.turn % 12 == 0:
            flood_message = spring_flood(self.lake, self.turn)
            if flood_message:
                for user_id in self.players.keys():
                    await context.bot.send_message(chat_id=user_id, text=flood_message)

        # Запуск наради
        if self.turn % MEETING_INTERVAL == 0:
            await start_meeting(context, self)
            return

        # Пропонуємо дії для наступного ходу
        for user_id in self.players.keys():
            await prompt_action(context, user_id)



    def add_player(self, user_id, name):
        """Adds a player to the game."""
        if len(self.players) < self.max_players and user_id not in self.players:
            self.players[user_id] = {"name": name, "score": 0, "current_action": None}

            # Assign the first player as admin
            if self.admin_chat_id is None:
                self.admin_chat_id = user_id

            return True, len(self.players)
        return False, len(self.players)


    def apply_penalty(self, player_data, score_1):
        player_data["score"] -= SCORE_PENALTY
        player_data["score"] -= score_1

    def apply_reward(self, player_data):
        player_data["score"] += SCORE_REWARD_CLEAN


    def all_actions_collected(self):
        """Перевіряє, чи всі гравці виконали свої дії."""
        return all(
            player_data["current_action"] is not None 
            for player_data in self.players.values()
        )


    def get_turn_info(self, previous_quality, score_1, score_2):
        """
        Формує текст повідомлення про інформацію після ходу.
        """
        previous_level, previous_position = previous_quality
        current_level, current_position = self.lake.level, self.lake.position

        water_status = (
            "Чиста вода" if current_level >= 4 else
            "Промислова чиста вода" if -3 <= current_level <= 3 else
            "Брудна вода"
        )

        result = (
            f"⭐️Отримано балів за хід: {self.turn_points}\n"
            f"🌟Сумарна кількість балів: {self.total_points}\n"
            f"----------------------------------------------------------\n"
            f"🌊 Стан озера: {water_status}\n"
            f"🔄 Зміна якості води: Рівень {previous_level} -> {current_level}, "
            f"Позиція {previous_position} -> {current_position}\n"
            f"----------------------------------------------------------\n"
            f"🏆 Поточний хід: {self.turn}/{GAME_DURATION_MONTHS}\n"
            f"📊 Бали за рішення:\n"
            f"   - Рішення №1 (скидання): {score_1}\n"
            f"   - Рішення №2 (очищення): {score_2}\n"
        )
        return result

    
    def calculate_action_scores(self):
        """Обчислює бали для дій №1 та №2 залежно від стану озера."""
        current_quality = self.lake.water_quality
        row_index = max(-8, min(current_quality, 6)) + 8  # Перетворення на індекс від 0 до 14
        score_1 = self.decision_1_scores[row_index]
        score_2 = self.decision_2_scores[row_index]
        return score_1, score_2


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
    
    
    def reset_game(self):
        """Скидає стан гри для початку нової."""
        self.players = {}
        self.state = "waiting"  # Ставимо стан гри на очікування
        self.turn = 0
        self.total_points = 0
        self.lake.reset_lake()  # Скидаємо стан озера
        self.meeting_active = False
        self.meeting_end_votes.clear()
