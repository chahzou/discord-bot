import sys, asyncio, discord

from .util.util import Utility
from .config import config

from .modules.color_roles import ColorRoles


# Notes:
# Always "await" coroutines of built-in functions (also works in statements)
# Boolean: capital (True)
# Using variables in code: getattr(this_module, "%s" % variable) - NEVER USE USER-INPUT!
# Permissions: message.author.server_permissions.[ex: manage_messages]



class Bot(discord.Client):

    async def on_ready(self):
        await self.load_modules()
        self.util = Utility(self)
        print('Logged in as {0}'.format(self.user))
        # await client.send_message(client.get_channel(defChannelID), '')


    async def load_modules(self):
        self.color_roles = ColorRoles(self)


    async def on_message(self, message):

        if await self.util.is_command(message.content):

            # Get command without identifier
            cmd_input = await self.util.get_content_part(message.content, 1, 1)       
            called = False

            # TODO: Match commands to modules and functions in modules
            if cmd_input in config.cmd_mod:     # If command has module
                await getattr(self, '%s' % config.cmd_mod[cmd_input])(message)
                called = True

            # Sends an error message if command is not in cmdList
            if not called or not cmd_input:
                await self.util.error_message(message.channel, "Command `"+cmd_input+"` not found.")

        # elif: Actions for not-command messages