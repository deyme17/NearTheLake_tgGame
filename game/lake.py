class Lake:
    def __init__(self):
        self.level = 0  # Початковий рівень 
        self.position = 5  # Початкова позиція 

    def update_quality(self, change: int):
        """
        Оновлює якість води в озері, враховуючи позицію і рівень.
        change > 0: очищення (позиція вправо/вгору).
        change < 0: скидання (позиція вліво/вниз).
        """
        self.position += change

        # Перехід між рівнями:
        if self.position > 8:  
            self.level += 1  
            self.position = 1  
        elif self.position < 1:  
            self.level -= 1  
            self.position = 8  

        # Обмежуємо рівень в межах від -8 до 6
        self.level = max(-8, min(self.level, 6))

    def get_current_scores(self):
        """
        Повертає бали за дії 1 (скидання) і 2 (очищення)
        для поточного рівня озера.
        """
        decision_1_scores = [5, 19, 26, 33, 41, 51, 64, 80, 100, 110, 121, 133, 146, 161, 177]
        decision_2_scores = [-20, -8, -3, 3, 7, 14, 21, 28, 35, 48, 63, 79, 92, 111, 127]

        # Індекс для доступу до балів залежить від рівня
        index = self.level + 8
        return decision_1_scores[index], decision_2_scores[index]
    
    def reset_lake(self):
        """Скидає стан озера до початкового."""
        self.level = 0  
        self.position = 5  

