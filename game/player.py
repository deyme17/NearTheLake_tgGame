class Player:
    def __init__(self, player_id, name):
        self.player_id = player_id         # Ідентифікатор гравця
        self.name = name                   # Ім'я гравця
        self.score = 0                     # Початковий баланс очок
        self.current_action = None         # Обрана дія гравця на поточний хід
        self.current_turn_points = 0       # Бали, отримані за поточний хід
        self.turn_number = 0               # Номер поточного ходу

    def choose_action(self, action):
        self.current_action = action

    def update_score(self, points):
        self.current_turn_points = points
        self.score += points

    def new_turn(self):
        self.turn_number += 1
        self.current_action = None
        self.current_turn_points = 0

    def __str__(self):
        return (
            f"Номер ходу: {self.turn_number}"
            f"Код рішення: {self.current_action}"
            f"Бали: {self.current_turn_points}"
            f"Всього з початку гри: {self.score}"
        )
