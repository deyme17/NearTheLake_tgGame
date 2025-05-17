from config.settings import MAX_PLAYERS

def joined_message(user_name, current_count):
    return f"✅ Ви приєдналися до гри як {user_name}. Очікуємо інших гравців: {current_count}/{MAX_PLAYERS}."

def player_connected_message(user_name, current_count):
    return f"👤 Гравець {user_name} приєднався до гри. Гравців: {current_count}/{MAX_PLAYERS}."

game_full_message = "⚠️ Ви вже у грі або місця більше немає."
in_game_now_message = "✅ Ви вже приєдналися до гри."
not_registered_message = "Ви не зареєстровані у грі!"
not_member_message = "Ви не учасник гри."