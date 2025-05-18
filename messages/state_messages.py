from config.settings import MAX_PLAYERS

game_finished_message = "🏁 Гра завершена!"
new_game_message = "🔄 Гру завершено. Ви можете розпочати нову гру."
no_game_messege = "❌ Гра вже завершена або ще не розпочата."
game_started_or_not_configure_messege = "❌ Гра вже почалася або ще не налаштована."
game_not_configure_message = "❌ Гра ще не налаштована."
game_started_negative_messege = "❌ Гра вже почалася. Ви не можете приєднатися зараз."
game_not_created_messege = "❌ Гра ще не створена."
game_not_init_message = "Гра не ініціалізована."
game_not_found_message = "❌ Гру не знайдено."
comeback_to_menu_message = "Ви повернулися в меню."

def joined_message(user_name, current_count, game):
    return f"✅ Ви приєдналися до гри як {user_name}. Очікуємо інших гравців: {current_count}/{game.settings.max_players}."

def player_connected_message(user_name, current_count, game):
    return f"👤 Гравець {user_name} приєднався до гри. Гравців: {current_count}/{game.settings.max_players}."

game_full_message = "⚠️ Ви вже у грі або місця більше немає."
in_game_now_message = "✅ Ви вже приєдналися до гри."
not_registered_message = "Ви не зареєстровані у грі!"
not_member_message = "Ви не учасник гри."
