class GameMessageService:
    @staticmethod
    def get_turn_info(previous_quality, current_quality, turn, game_duration_months, current_points, score):
        previous_level, previous_position = previous_quality
        current_level, current_position = current_quality

        water_status = (
            "Чиста вода" if current_level >= 4 else
            "Промислова чиста вода" if -3 <= current_level <= 3 else
            "Брудна вода"
        )

        score_1, score_2 = current_quality[2], current_quality[3] if len(current_quality) > 2 else (0, 0)

        return (
            f"⭐️ Ваші очки за цей хід: {current_points}\n"
            f"🌟 Ваші загальні очки: {score}\n"
            f"----------------------------------------------------------\n"
            f"🌊 Стан озера: {water_status}\n"
            f"🔄 Зміна якості води: Рівень {previous_level} -> {current_level}, "
            f"Позиція {previous_position} -> {current_position}\n"
            f"----------------------------------------------------------\n"
            f"🏆 Поточний хід: {turn}/{game_duration_months}\n"
            f"📊 Бали за рішення:\n"
            f"   - Рішення №1 (скидання): {score_1}\n"
            f"   - Рішення №2 (очищення): {score_2}\n"
        )

    @staticmethod
    def get_winner_message(players, game_ended):
        if not game_ended:
            return "Гра ще не завершена."

        sorted_players = sorted(players.values(), key=lambda p: p.score, reverse=True)

        table = "Результати гри:\n"
        table += "{:<4} {:<20} {:<10}\n".format("Місце", "Гравець", "Очки")
        table += "-" * 40 + "\n"

        for rank, player in enumerate(sorted_players, start=1):
            table += "{:<4} {:<20} {:<10}\n".format(rank, player.name, player.score)

        return table
