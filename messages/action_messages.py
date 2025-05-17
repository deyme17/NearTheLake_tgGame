from config.constants import ACTION_NAMES

wait_others_message = "Очікуємо вибір інших гравців"
have_chosen_action = "Ви вже зробили свій вибір в цьому ході!"
choose_action_message = "Виберіть вашу дію:"
first_action = "Ваш перший хід"

def chosen_action_message(action):
    return f"Ви вибрали: {ACTION_NAMES[action]}"
def choice_message(action):
    return f"Ваш вибір: {ACTION_NAMES[action]}"
