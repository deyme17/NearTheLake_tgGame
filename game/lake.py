from config.settings import FLOOD_CLEAN_MIN, FLOOD_CLEAN_MAX
import random


class Lake:
    def __init__(self):
        self.water_quality = 0  # Початковий рівень якості води (0 - нейтральний)

    def update_quality(self, effect):
        self.water_quality += effect

    def get_quality(self):
        return self.water_quality

    def flood_event(self, min_clean=FLOOD_CLEAN_MIN, max_clean=FLOOD_CLEAN_MAX):
        clean_amount = random.randint(min_clean, max_clean)
        self.update_quality(clean_amount)
        return clean_amount

    def __str__(self):
        return f"Якість води: {self.water_quality}"
