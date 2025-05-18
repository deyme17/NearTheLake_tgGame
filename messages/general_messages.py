
def help_message():
    return f"""Вітаю! Ось доступні команди для гри "Біля озера":

    /help - Показати це повідомлення з допомогою
    /rule - Показати правила гри
    /end_game - Закінчити гру завчасно
    
    Щоб почати, просто введіть /start.
    Гра почнеться, коли в лоббі будуть всі гравці.
    """

settings_not_available_message = "⚠️ Налаштування доступні лише до початку гри."

def start_message(player_list):
    return (
        f"🎮 Гра розпочалася! Учасники:\n{player_list}\n\n"
    )

greeting_menu_messsge = (
    "🎮 Ласкаво просимо до гри «Біля озера»!\n\n"
    "Це стратегічна гра про управління ресурсами. "
    "Приймайте рішення, стежте за станом озера та збільшуйте свій прибуток!.\n\n"
    "📍 Ви в головному меню. Виберіть один із варіантів нижче:\n"
    "— «Почати гру» — щоб створити або приєднатись до гри\n"
    "— «Налаштування» — щоб змінити параметри\n"
    "— «Правила гри» — щоб переглянути правила гри"
)

settings_menu_title = "⚙️ Оберіть параметр для редагування:"
settings_enter_value_message = lambda param: f"✏️ Введіть нове значення для {param_ua.get(param, param)}:"
settings_updated_message = lambda param, val: f"✅ {param_ua.get(param, param)} оновлено до {val}."
settings_invalid_value = "❌ Введіть ціле число."
settings_unavailable_message = "⚠️ Налаштування недоступні під час гри."

param_ua = {
    "MAX_PLAYERS": "Кількість гравців",
    "GAME_DURATION_MONTHS": "Тривалість гри (в місяцях)",
    "MEETING_INTERVAL": "Інтервал між нарадами",
    "BONUS_SCORE": "Премія за очищення",
    "PENALTY_SCORE": "Штраф за скидання"
}
