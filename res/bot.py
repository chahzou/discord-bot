import sys, asyncio, discord

from .util.util import Utility
from .config import config

from .modules.test import Test
from .modules.help import Help
from .modules.color_roles import ColorRoles
from .modules.other import Other

# TODO: Import all python files from modules folder automatically (Pasted)
'''from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/modules/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]'''


# Notes:
# Always "await" coroutines of built-in functions (also works in statements)
# Boolean: capital (True)
# Using variables in code: getattr(this_module, "%s" % variable) - NEVER DIRECTLY USE USER-INPUT!
# Permissions: message.author.server_permissions.[ex: manage_messages]


class Bot(discord.Client):

    async def on_ready(self):
        
        self.util = Utility(self)
        self.config = config
        await self.load_modules()

        print('Logged in as {0}'.format(self.user))
        # await client.send_message(client.get_channel(defChannelID), '')


    # Initializes modules
    async def load_modules(self):
        self.test = Test(self)
        self.color_roles = ColorRoles(self)


    async def on_message(self, message):

        cmd = message.content

        if await self.util.is_command(cmd):

            executed = False

            # Get first command without identifier
            cmd_mod = await self.util.get_content_part(cmd, 1, 1)

            # TODO: Match commands to modules
            if cmd_mod in config.cmd_mod_assoc:       # If config contains module
                await getattr(self, '%s' % config.cmd_mod_assoc[cmd_mod]).run(message)
                executed = True

            # Sends an error message if command is not in cmdList
            if not executed or not cmd_mod:
                await self.util.error_message(message.channel, "No module for \'" + cmd_mod + "\' was found.")

        # elif: Actions for non-command messages
