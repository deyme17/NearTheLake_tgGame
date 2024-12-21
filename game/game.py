from bot.controller import end_game
from config.settings import MAX_PLAYERS, GAME_DURATION_MONTHS, SCORE_PENALTY, SCORE_REWARD, MEETING_DURATION, MEETING_INTERVAL, ACTION_1_CLEAR_VAL, ACTION_2_CLEAR_VAL
from game.lake import Lake
from game.player import Player
from game.events import spring_flood, start_meeting
from bot.utils import prompt_action


class Game:
    def __init__(self):
        self.players = {}  # {user_id: Player}
        self.max_players = MAX_PLAYERS
        self.state = "waiting"
        self.turn = 1
        self.lake = Lake()
        self.admin_chat_id = None

        self.meeting_active = False
        self.meeting_end_votes = set()

        self.total_points = 0
        self.turn_points = 0


    def add_player(self, user_id, name):
        """Додає гравця до гри"""
        if len(self.players) < self.max_players and user_id not in self.players:
            player = Player(user_id, name)
            self.players[user_id] = player
            
            if self.admin_chat_id is None:
                self.admin_chat_id = user_id
                
            return True, len(self.players)
        return False, len(self.players)
    
    
# the main fuction
    async def process_turn(self, context):
        """Обробка ходу гри"""
        if self.meeting_active or not self.all_actions_collected():
            return

        # Зберігаємо попередній стан озера
        previous_quality = (self.lake.level, self.lake.position)
        initial_scores = self.lake.get_current_scores()

        # Визначаємо наявність штрафів або нагород
        has_penalty = any(player.current_action == "3" for player in self.players.values())
        has_reward = any(player.current_action == "4" for player in self.players.values())

        for player in self.players.values():
            action = player.current_action 

            if action == "1": #  Скидання
                self.lake.update_quality(ACTION_1_CLEAR_VAL)
                if not has_penalty:
                    player.add_points(initial_scores[0])
                else:
                    self.apply_penalty(player)

            elif action == "2": # Очищення
                self.lake.update_quality(ACTION_2_CLEAR_VAL)
                player.add_points(initial_scores[1])
                if has_reward:
                    player.add_points(SCORE_REWARD)

            elif action == "3":  # Штраф
                earned_points = -len(self.players)
                player.add_points(earned_points)

            elif action == "4":  # Нагорода
                earned_points = -len(self.players)
                player.add_points(earned_points)

            # Оновлюємо очки гравця за хід
            player.clear_action()

        # Отримуємо новий стан озера
        next_scores = self.lake.get_current_scores()
        turn_info = self.get_turn_info(previous_quality, next_scores[0], next_scores[1])

        # Надсилаємо стан гравцям
        for player in self.players.values():
            personal_message = (
                f"⭐️ Ваші очки за цей хід: {player.current_turn_points}\n"
                f"🌟 Ваші загальні очки: {player.score}\n"
                f"{turn_info}"
            )
            await context.bot.send_message(chat_id=player.player_id, text=personal_message)

            # очищаємо current_turn_points
            player.clear_curr_turn_points()


        # Оновлюємо хід і перевіряємо завершення гри
        self.turn += 1
        if self.check_game_end():
            winners_message = self.get_winner()
            for player in self.players.values():
                await context.bot.send_message(chat_id=player.player_id, text="🏁 Гра завершена!")
                await context.bot.send_message(chat_id=player.player_id, text=winners_message)
            self.reset_game()
            return

        # Події (повінь, зустрічі тощо)
        if self.turn % 12 == 0:
            flood_message = spring_flood(self.lake)
            if flood_message:
                for player in self.players.values():
                    await context.bot.send_message(chat_id=player.player_id, text=flood_message)

        if self.turn % MEETING_INTERVAL == 0:
            await start_meeting(context, self)
            return

        # Запитуємо дії від гравців на наступний хід
        for player in self.players.values():
            await prompt_action(context, player.player_id)


    def apply_penalty(self, player):
        """Застосовує штраф до гравця"""
        player.add_points(-SCORE_PENALTY)

    def apply_reward(self, player):
        """Застосовує нагороду до гравця"""
        player.add_points(SCORE_REWARD)


    def all_actions_collected(self):
        """Перевіряє, чи всі гравці виконали свої дії"""
        return all(player.current_action is not None for player in self.players.values())
    

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
    

    def check_game_end(self):
        """Перевіряє, чи досягнуто кінця гри"""
        if self.turn >= GAME_DURATION_MONTHS:
            self.state = "ended"
            return True
        return False

    def get_winner(self):
        """Визначає переможця гри"""
        if self.state != "ended":
            return "Гра ще не завершена."

        sorted_players = sorted(
            self.players.values(),
            key=lambda player: player.score,
            reverse=True
        )

        table = "Результати гри:\n"
        table += "{:<4} {:<20} {:<10}\n".format("Місце", "Гравець", "Очки")
        table += "-" * 40 + "\n"

        for rank, player in enumerate(sorted_players, start=1):
            table += "{:<4} {:<20} {:<10}\n".format(
                rank,
                player.name,
                player.score
            )

        return table
    

    def reset_game(self):
        """Скидає стан гри"""
        for player in self.players.values():
            player.reset()
        self.players.clear()
        self.state = "waiting"
        self.turn = 0
        self.total_points = 0
        self.lake.reset_lake()
        self.meeting_active = False
        self.meeting_end_votes.clear()