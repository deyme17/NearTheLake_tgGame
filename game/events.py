from config.settings import FLOOD_CLEAN_MIN, FLOOD_CLEAN_MAX, MEETING_DURATION
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils import prompt_action


import random

def spring_flood(lake, turn):
    if (turn + 1) % 12 == 0:  # раз на рік
        flood_change = random.randint(FLOOD_CLEAN_MIN, FLOOD_CLEAN_MAX)
        lake.update_quality(flood_change)
        return f"🌊 Весняний паводок! Якість води покращилася на {flood_change} пунктів."
    return None


async def start_meeting(context, game):
    """Запускає нараду."""
    game.meeting_active = True
    game.meeting_end_votes.clear()

    keyboard = [
        [InlineKeyboardButton("Закінчити нараду", callback_data="end_meeting_vote")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    for user_id in game.players:
        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"🗣️ Нарада почалася! Ви маєте {MEETING_DURATION // 60} хвилини для обговорення.\n"
                "Натисніть 'Закінчити нараду', якщо всі згодні завершити достроково."
            ),
            reply_markup=reply_markup,
        )

    # Запустити автоматичне завершення наради через MEETING_DURATION
    context.job_queue.run_once(
        end_meeting_job, MEETING_DURATION, data={"game": game}, name="end_meeting"
    )


async def end_meeting_job(context):
    """Автоматичне завершення наради."""
    job_data = context.job.data
    game = job_data["game"]
    await end_meeting(context, game)


async def end_meeting(context, game):
    """Завершує нараду."""
    game.meeting_active = False
    game.meeting_end_votes.clear()

    for user_id in game.players:
        await context.bot.send_message(chat_id=user_id, text="⏳ Нарада завершена.")

    # Пропонувати дії для наступного ходу
    for user_id in game.players.keys():
        await prompt_action(context, user_id)
