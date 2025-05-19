def get_spring_flood_message(flood_change):
    return f"🌊 Весняний паводок! Якість води покращилася на {flood_change} пунктів."

def get_meeting_started_message(game):
    return (
        f"🗣️ Нарада почалася! Ви маєте {game.meeting_duration // 60} хвилин для обговорення.\n"
        "Натисніть 'Закінчити нараду', якщо всі згодні завершити достроково."
    )

meeting_finished_message = "⏳ Нарада завершена."
meeting_continues_message = "⏳ Зараз триває нарада. Хід буде доступний після завершення наради."
end_meeting = "Завершити нараду"
no_communication_message = "Нарада не активна. Повідомлення не приймаються."
meeting_inactive_message = "Нарада не активна зараз."
voted_message = "Ви вже проголосували."
vote_enrolled_message = "Ваш голос за завершення наради зараховано."
