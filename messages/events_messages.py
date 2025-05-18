
from config.settings import MEETING_DURATION

def spring_flood_messege(flood_change):
    return f"🌊 Весняний паводок! Якість води покращилася на {flood_change} пунктів."

def meeting_started_messege(game):
    return (
        f"🗣️ Нарада почалася! Ви маєте {MEETING_DURATION // 60} хвилин для обговорення.\n"
        "Натисніть 'Закінчити нараду', якщо всі згодні завершити достроково."
    )

meeting_finished_messege = "⏳ Нарада завершена."
meeting_continues_message = "⏳ Зараз триває нарада. Хід буде доступний після завершення наради."
end_meeting = "Завершити нараду"
no_communication_message = "Нарада не активна. Повідомлення не приймаються."
meeting_inactive_message = "Нарада не активна зараз."
voted_message = "Ви вже проголосували."
vote_enrolled_message = "Ваш голос за завершення наради зараховано."
