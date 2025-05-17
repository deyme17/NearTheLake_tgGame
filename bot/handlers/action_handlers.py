from bot.services.action_service import ActionUseCase

async def handle_action_callback(update, context):
    await ActionUseCase.handle_action(update, context)
