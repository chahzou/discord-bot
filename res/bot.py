import sys, re, discord

from .util.util import Utility
from .config import config

from .modules.info import Info
from .modules.test import Test
from .modules.administration import Administration
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
        self.cfg = config

        await self.load_modules()

        print('Ready! (Logged in as {0}'.format(self.user) + ")")
        await self.send_message(self.get_channel(self.cfg.general['def_channel_id']), "Now online.")


    # Automatically creates instances of all modules which are configured in config and imported here
    # Also creates dictionary for association of modules with their command argument
    # TODO: Check safety
    # TODO: Automate import
    async def load_modules(self):

        self.arg_mod_assoc = {}

        regex_arg = re.compile('^[A-Za-z0-9_]+$')

        # Create instances of all modules, get their command arguments and save them to dictionary

        count = 0
        for mod_class_name in self.cfg.modules:
            if regex_arg.match(mod_class_name):
                
                mod_cl = globals()[mod_class_name]
                mod_inst = mod_cl(self)

                self.arg_mod_assoc[mod_inst.cmd_arg] = mod_inst
                count += 1

        print("Initialized " + str(count) + " modules.")


    # Runs "run" method in specified module
    async def on_message(self, message):

        if await self.util.is_command(message.content):

            executed = False

            # Remove operator
            cmd = message.content[len(self.cfg.general['cmd_op']):]

            # Get arguments as list
            args = await self.util.split_cmd_to_args_list(cmd)
            
            # Call module specified by first argument
            if args[0] in self.arg_mod_assoc.keys():       # If config contains module
                await self.call_module_function(args[0], 'run', args[1:], message)
                executed = True

            # Sends an error message if command is not in cmdList
            if not executed or not args[0]:
                await self.util.error_message(message.channel, "No module for \'" + args[0] + "\' was found or configured.")

        # elif: Actions for non-command messages


    # Calls the specified function in the specified module and passes args and optionally original message
    async def call_module_function(self, mod_arg, function, args, message=None):

        if (all(isinstance(i, str) for i in [mod_arg, function]) and 
                mod_arg in self.arg_mod_assoc.keys()):
            if message:
                return await getattr(self.arg_mod_assoc[mod_arg], function)(args, message)
            else:
                return await getattr(self.arg_mod_assoc[mod_arg], function)(args)