from config.settings import MAX_PLAYERS, GAME_DURATION_MONTHS, SCORE_PENALTY, SCORE_REWARD_CLEAN, MEETING_DURATION, MEETING_INTERVAL, ACTION_1_CLEAR_VAL, ACTION_2_CLEAR_VAL
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
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


    def add_player(self, user_id, name):
        """Adds a player to the game."""
        if len(self.players) < self.max_players and user_id not in self.players:
            self.players[user_id] = {"name": name, "score": 0, "current_action": None}

            # Assign the first player as admin
            if self.admin_chat_id is None:
                self.admin_chat_id = user_id

            return True, len(self.players)
        return False, len(self.players)
    
    def get_admin_chat_id(self):
        """Returns the admin chat ID."""
        return self.admin_chat_id

    
    async def start_game(self, context):
        """Запускає гру та надсилає початкові повідомлення гравцям."""
        self.state = "in_progress"
        player_list = "\n".join([f"- {data['name']}" for data in self.players.values()])
        
        # Отримуємо бали для дій
        score_1, score_2 = self.calculate_action_scores()

        start_message = (
            f"🎮 Гра розпочалася! Учасники:\n{player_list}\n\n"
            f"На початку гри:\n"
            f"- Рішення №1 (Скидання): {score_1} очок\n"
            f"- Рішення №2 (Очищення): {score_2} очок\n"
            f"- Рішення №3 (Штраф): -{SCORE_PENALTY} очок\n"
            f"- Рішення №4 (Премія): +{SCORE_REWARD_CLEAN} очок\n\n"
            f"Ваш перший хід. Виберіть дію (1: Скидання, 2: Очищення, 3: Штраф, 4: Премія)."
        )
        for user_id in self.players.keys():
            await context.bot.send_message(chat_id=user_id, text=start_message)


    def collect_actions(self, actions):
        if self.state == "ended":
            return 

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


# !!!!!!!!!!!
    async def process_turn(self, context):
        """Обробка ходу гри."""
        if self.meeting_active:
            # Повідомлення для гравців, що нарада триває
            for user_id in self.players:
                await context.bot.send_message(
                    chat_id=user_id,
                    text="⏳ Нарада триває. Хід не може розпочатися, поки нарада не завершена."
                )
            return

        if not self.all_actions_collected():
            for user_id in self.players:
                await context.bot.send_message(
                    chat_id=user_id,
                    text="Не всі гравці виконали свої дії. Очікуються дії від інших гравців."
                )
            return

        previous_quality = (self.lake.level, self.lake.position)
        has_penalty = any(player["current_action"] == "3" for player in self.players.values())

        # Обробка дій гравців
        for user_id, player_data in self.players.items():
            action = player_data["current_action"]
            if action == "1":
                self.lake.update_quality(-1)
            elif action == "2":
                self.lake.update_quality(1)

        # Оновлення балів
        score_1, score_2 = self.lake.get_current_scores()

        for user_id, player_data in self.players.items():
            action = player_data["current_action"]
            earned_points = 0
            if action == "1":
                if has_penalty:
                    self.apply_penalty(player_data, score_1)
                    earned_points = -score_1 - SCORE_PENALTY
                else:
                    player_data["score"] += score_1
                    earned_points = score_1
            elif action == "2":
                player_data["score"] += score_2
                earned_points = score_2
            elif action == "3":
                for target_id, target_data in self.players.items():
                    if target_data["current_action"] == "1":
                        self.apply_penalty(target_data, score_1)
                player_data["score"] -= len(self.players)
                earned_points = -len(self.players)
            elif action == "4":
                for target_id, target_data in self.players.items():
                    if target_data["current_action"] == "2":
                        self.apply_reward(target_data)
                player_data["score"] -= len(self.players)
                earned_points = -len(self.players)

            # Надсилаємо повідомлення про очки
            await context.bot.send_message(
                chat_id=user_id,
                text=(f"🎲 Ваш хід завершено! Ви заробили {earned_points} очок.\n"
                    f"📊 Ваш загальний рахунок: {player_data['score']} очок.")
            )

        # Надсилаємо статус озера
        lake_status_message = self.get_lake_status(previous_quality, score_1, score_2)
        for user_id in self.players.keys():
            await context.bot.send_message(chat_id=user_id, text=lake_status_message)

        self.turn += 1

        if self.check_game_end():
            winners_message = self.get_winner()
            for user_id in self.players.keys():
                await context.bot.send_message(chat_id=user_id, text="🏁 Гра завершена!")
                await context.bot.send_message(chat_id=user_id, text=winners_message)
            return

        # Запуск наради після кожного 8-го ходу
        if self.turn % MEETING_INTERVAL == 0:
            await start_meeting(context, self)
            return  # Після запуску наради хід не повинен продовжуватись

        # Пропонуємо дії для наступного ходу
        for user_id in self.players.keys():
            await prompt_action(context, user_id)



    def get_lake_status(self, previous_quality, score_1, score_2):
        """
        Формує текст повідомлення про стан озера після ходу.
        """
        previous_level, previous_position = previous_quality
        current_level, current_position = self.lake.level, self.lake.position

        water_status = (
            "Чиста вода" if current_level >= 4 else
            "Промислова чиста вода" if -3 <= current_level <= 3 else
            "Брудна вода"
        )

        result = (
            f"🌊 Стан озера: {water_status}\n"
            f"🔄 Зміна якості води: Рівень {previous_level} -> {current_level}, "
            f"Позиція {previous_position} -> {current_position}\n"
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