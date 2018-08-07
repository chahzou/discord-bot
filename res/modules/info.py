import re, asyncio, discord

from ..module import Module


class Info(Module):

    async def return_help(self):
        return "Provides info about the mod."
    
    async def run(self, message):
        await self.bot.send_message(message.channel, "This is chahzou's discord bot.\nYou can view the code here: https://github.com/chahzou/discord-bot")