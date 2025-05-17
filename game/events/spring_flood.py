from config.settings import FLOOD_CLEAN_MIN, FLOOD_CLEAN_MAX
from messages.events_messages import spring_flood_messege

import random

class SpringFlood:
    @staticmethod
    def start_flood(lake):
        flood_change = random.randint(FLOOD_CLEAN_MIN, FLOOD_CLEAN_MAX)
        lake.update_quality(flood_change)
        return spring_flood_messege(flood_change)