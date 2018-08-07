import sys, asyncio, discord

from .util.util import Utility
from .config import config

from .modules.info import Info
from .modules.test import Test
from .modules.help import Help
from .modules.color_roles import ColorRoles

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
        self.info = Info(self)
        self.test = Test(self)
        self.help = Help(self)
        self.util = Utility(self)
        self.color_roles = ColorRoles(self)


    # Runs "run" method in specified module of command (See command <-> module association in config)
    async def on_message(self, message):

        if await self.util.is_command(message.content):

            executed = False

            # Remove operator
            cmd = message.content[len(self.config.general['cmd_op']):]

            # Get argument list
            args = await self.util.return_args(cmd)
            
            # Call module specified by first argument
            if args[0] in config.arg_mod_assoc:       # If config contains module
                await self.call_module_function('run', args, message)
                executed = True

            # Sends an error message if command is not in cmdList
            if not executed or not args[0]:
                await self.util.error_message(message.channel, "No module for \'" + args[0] + "\' was found or configured.")

        # elif: Actions for non-command messages


    async def call_module_function(self, function, args=None, message=None):

        if args and message:
            if self.config.arg_mod_assoc[args[0]]:
                return await getattr(getattr(self, '%s' % config.arg_mod_assoc[args[0]]), function)(args, message)
        else:
            return await getattr(getattr(self, '%s' % config.arg_mod_assoc[args[0]]), function)()