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
waiting_for_player_message = "⏳ Ви ще не приєдналися до гри. Натисніть «Почати гру», щоб увійти до лобі."
left_game_message = lambda name: f"🚪 Гравець {name} вийшов з лобі. Ви повернулись до головного меню."

def joined_message(user_name, current_count, game):
    return f"✅ Ви приєдналися до гри як {user_name}. Очікуємо інших гравців: {current_count}/{game.settings.max_players}."

def player_connected_message(user_name, current_count, game):
    return f"👤 Гравець {user_name} приєднався до гри. Гравців: {current_count}/{game.settings.max_players}."

def left_lobby_message(player):
    return f"❗️{player.name} вийшов із лобі."

game_full_message = "⚠️ Ви вже у грі або місця більше немає."
in_game_now_message = "✅ Ви вже приєдналися до гри."
not_registered_message = "Ви не зареєстровані у грі!"
not_member_message = "Ви не учасник гри."

vote_started_message = lambda initiator: f"🗳 Гравець {initiator} запропонував завершити гру.\nЩоб підтримати — надішліть 'Завершити гру'."
vote_registered_message = "✅ Ваш голос за завершення гри враховано. Очікуємо на інших гравців..."
you_voted_now_message = "⚠️ Ви вже проголосували."