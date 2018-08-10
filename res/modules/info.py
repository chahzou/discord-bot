import re, asyncio, discord

from ..module import Module


class Info(Module):

    cmd_arg = 'info'
    
    async def run(self, args=None, message=None):
        await self.bot.send_message(message.channel, "This is chahzou's discord bot.\nYou can view the code here: https://github.com/chahzou/discord-bot")

    async def return_help(self, args=None):
        return "Provides info about the bot."