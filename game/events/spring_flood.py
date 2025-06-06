from messages.events_messages import get_spring_flood_message

import random

class SpringFlood:
    @staticmethod
    def start_flood(lake, game):
        flood_change = random.randint(game.settings.flood_clean_min, game.settings.flood_clean_max)
        lake.update_quality(flood_change)
        return get_spring_flood_message(flood_change)