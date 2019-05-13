import re, asyncio, discord

from ..module import Module


class Info(Module):

    cmd_arg = 'info'

    async def run(self, args=None, message=None):
        if message:
            cmd_op = self.bot.cfg.general['cmd_op']
            info_msg = ("This is chahzou's discord bot. \nThe code is public: https://github.com/chahzou/discord-bot. " 
                "Use `"+ cmd_op + "help` for info on how to use its features.\n")
            await message.channel.send(info_msg)


    async def return_help(self, args=None):
        return "Provides info about the bot."