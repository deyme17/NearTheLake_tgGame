from config.settings import FLOOD_CLEAN_MIN, FLOOD_CLEAN_MAX
from game.lake import Lake
import random

def spring_flood(lake, turn):
    if (turn + 1) % 4 == 0:  # Кожен 4-й хід (квітень)
        flood_change = random.randint(FLOOD_CLEAN_MIN, FLOOD_CLEAN_MAX)  
        lake.update_quality(flood_change)
        return f"🌊 Весняний паводок! Якість води покращилася на {flood_change} пунктів."
    return None
