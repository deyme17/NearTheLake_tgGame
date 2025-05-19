from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from messages.general_messages import param_ua
from config.settings import SETTINGS_PARAMS

keyboards = {
    "idle": [
        ["Почати гру"],
        ["Налаштування", "Правила гри"]
    ],
    "in_game": [
        ["Завершити гру", "Правила гри"]
    ],
    "waiting_lobby": [
        ["Вийти з лобі"],
        ["Правила гри"]
    ]
}

def get_keyboard_for_state(state: str) -> ReplyKeyboardMarkup:
    keyboard = keyboards.get(state, [["Правила гри"]])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_settings_keyboard(game):
    buttons = []
    for param_key, icon in SETTINGS_PARAMS:
        value = getattr(game.settings, param_key.lower(), "N/A")
        label = f"{icon} {param_ua[param_key]} ({value})"
        callback = f"set_{param_key}"
        buttons.append([InlineKeyboardButton(label, callback_data=callback)])

    return InlineKeyboardMarkup(buttons)