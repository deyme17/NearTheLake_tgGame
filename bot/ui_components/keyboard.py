from telegram import ReplyKeyboardMarkup

keyboards = {
    "idle": [
        ["Почати гру"],
        ["Налаштування", "Правила гри"]
    ],
    "in_game": [
        ["Завершити гру", "Правила гри"]
    ]
}

def get_keyboard_for_state(state: str) -> ReplyKeyboardMarkup:
    keyboard = keyboards.get(state, [["Правила гри"]])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
