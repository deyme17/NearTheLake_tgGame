from messages.error_messages import command_not_recognize_message

class BaseCommandManager:
    def __init__(self, commands: list):
        self.commands = commands

    async def handle(self, update, context, game):
        text = update.message.text.strip().lower()
        for command in self.commands:
            if command.matches(text):
                await command.execute(update, context, game)
                return
        await self.on_unknown(update)

    async def on_unknown(self, update):
        await update.message.reply_text(command_not_recognize_message)
