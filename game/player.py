class Player:
    def __init__(self, player_id, name):
        self.player_id = player_id         # Ідентифікатор гравця
        self.name = name                   # Ім'я гравця
        self.score = 0                     # Початковий баланс очок
        self.current_action = None         # Обрана дія гравця на поточний хід
        self.current_turn_points = 0       # Бали, отримані за поточний хід
        self.turn_number = 0               # Номер поточного ходу