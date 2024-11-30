# Кількість гравців у грі
MAX_PLAYERS = 7

# Тривалість гри в місяцях (4 роки = 48 місяців)
GAME_DURATION_MONTHS = 48

ACTION_1_CLEAR_VAL = -1
ACTION_2_CLEAR_VAL = 1

SCORE_PENALTY = 20       # Штраф, якщо гравець вибрав дію "скидання води"
SCORE_REWARD_CLEAN = 10   # Бонус для гравців, які вибрали "очищення води"

FLOOD_CLEAN_MIN = 2       # Мінімальне очищення озера під час паводку
FLOOD_CLEAN_MAX = 12     # Максимальне очищення озера під час паводку

MEETING_INTERVAL = 8      # Інтервал у місяцях між нарадами
MEETING_DURATION = 180    # Тривалість нараду (у секундах)