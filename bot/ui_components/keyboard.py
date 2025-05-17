from telegram import ReplyKeyboardMarkup

def main_menu_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            ["Почати гру", "Завершити гру"],
            ["Правила гри", "Налаштування"]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )