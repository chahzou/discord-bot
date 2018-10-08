import re, asyncio, discord

from ..module import Module


class Info(Module):

    cmd_arg = 'info'
    info_msg = ("This is chahzou's discord bot. \nThe code is public: https://github.com/chahzou/discord-bot. " 
        "Use `help` for info on how to use its features.\n")
    
    async def run(self, args=None, message=None):
        if message:
            await self.bot.send_message(message.channel, self.info_msg)

    async def return_help(self, args=None):
        return "Provides info about the bot."