from config.settings import MAX_PLAYERS

def help_message():
    return f"""Вітаю! Ось доступні команди для гри "Біля озера":

    /help - Показати це повідомлення з допомогою
    /rule - Показати правила гри
    /end_game - Закінчити гру завчасно
    
    Щоб почати, просто введіть /start.
    Гра почнеться, коли в лоббі будуть {MAX_PLAYERS} гравців.
    """