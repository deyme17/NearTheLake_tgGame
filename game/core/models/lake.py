class Lake:
    def __init__(self):
        self.level = 0 
        self.position = 5

    def update_quality(self, change: int):
        """
        Updates the water quality in the lake, taking into account the position and level.
        change > 0: clean (position right/up).
        change < 0: reset (position left/down).
        """
        self.position += change

        if self.position > 8:  
            self.level += 1  
            self.position = 1  

        elif self.position < 1:  
            self.level -= 1  
            self.position = 8  

        # limits
        self.level = max(-8, min(self.level, 6))

    def get_current_scores(self, game):
        """
        Returns the points for actions 'dump' and 'clean' for the current lake level.
        """
        index = self.level + 8
        return game.settings.dump_scores[index], game.settings.clean_scores[index]

    def reset_lake(self):
        """Resets the lake to its initial state."""
        self.level = 0  
        self.position = 5  

