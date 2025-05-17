class Player:
    def __init__(self, player_id, name):
        self.player_id = player_id 
        self.name = name  
        self.score = 0  
        self.current_action = None 
        self.current_turn_points = 0  
        self.turn_number = 0  

    def reset(self):
        """
        Resets all player parameters to their original state.
        """
        self.score = 0
        self.current_action = None
        self.current_turn_points = 0
        self.turn_number = 0

    def add_points(self, points):
        """
        Adds points to the player for the current turn.
        """
        self.score += points
        self.current_turn_points += points

    def set_action(self, action):
        """
        Sets the player's action for the current turn.
        """
        self.current_action = action

    def clear_action(self):
        """
        Clears the player's action after processing the current turn.
        """
        self.current_action = None
        self.turn_number += 1

    def clear_curr_turn_points(self):
        """Clear current_turn_points"""
        self.current_turn_points = 0

    def __str__(self):
        """
        Returns a text description of the player.
        """
        return (
            f"Гравець {self.name} (ID: {self.player_id}):\n"
            f"  Рахунок: {self.score}\n"
            f"  Очки за поточний хід: {self.current_turn_points}\n"
            f"  Дія: {self.current_action}\n"
            f"  Номер ходу: {self.turn_number}"
        )
