from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from game.game import Game
from bot.message import help_message, rule_message

ENTER_NAME = 0
game = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game
    if game is None:
        game = Game()
    
    if game.state == "waiting" and update.effective_user.id not in game.players:
        await update.message.reply_text("Ласкаво просимо до гри 'Біля озера'! Будь ласка, введіть ваше ім'я:")
        return ENTER_NAME
    elif update.effective_user.id in game.players:
        await update.message.reply_text(f"Ви вже в грі. Очікуємо інших гравців. Зараз гравців: {len(game.players)}/{game.max_players}")
    else:
        await update.message.reply_text("Гра вже почалася. Спробуйте пізніше.")
    return ConversationHandler.END

async def enter_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game
    user_id = update.effective_user.id
    name = update.message.text

    if game.add_player(user_id, name):
        await update.message.reply_text(f"Дякую, {name}! Ви успішно приєдналися до гри.")
        await broadcast_player_count(context)
        
        if game.start_game():
            await start_game(update, context)
    else:
        await update.message.reply_text("На жаль, ви не можете приєднатися до гри. Можливо, вона вже заповнена.")
    
    return ConversationHandler.END

async def broadcast_player_count(context: ContextTypes.DEFAULT_TYPE):
    global game
    for user_id in game.players:
        await context.bot.send_message(
            chat_id=user_id, 
            text=f"Кількість гравців: {len(game.players)}/{game.max_players}"
        )

async def start_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global game
    game.state = "in_progress"
    player_list = "\n".join([f"{data['name']}" for data in game.players.values()])
    message = f"Гра починається! Учасники:\n{player_list}"
    for user_id in game.players:
        await context.bot.send_message(chat_id=user_id, text=message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = help_message() 
    await update.message.reply_text(help_text)

async def rule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rule_text = rule_message()  
    await update.message.reply_text(rule_text)