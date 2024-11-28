from config.settings import FLOOD_CLEAN_MIN, FLOOD_CLEAN_MAX, MEETING_DURATION
from game.lake import Lake
import random

def spring_flood(lake, turn):
    if (turn + 1) % 4 == 0:  # Кожен 4-й хід (квітень)
        flood_change = random.randint(FLOOD_CLEAN_MIN, FLOOD_CLEAN_MAX)  
        lake.update_quality(flood_change)
        return f"🌊 Весняний паводок! Якість води покращилася на {flood_change} пунктів."
    return None

def start_meeting(game, context):
    """Починає нараду між гравцями."""
    game.is_meeting_active = True
    return f"🗣️ Нарада почалася! Гравці можуть обговорювати свої дії протягом {MEETING_DURATION // 60} хвилин."


def end_meeting(game, context):
    """Завершує нараду між гравцями."""
    game.is_meeting_active = False
    return "⏳ Нарада завершена. Повертаємося до гри!"
