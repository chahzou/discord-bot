import sys, re, discord, asyncio

from .util.util import Utility
from .config import config

from .modules.info import Info
from .modules.test import Test
from .modules.help import Help
from .modules.administration import Administration
from .modules.registration import Registration
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

# ??? If an argument list is passed with only one string, it is no longer a list and just a string.
#   If the nth item of the argument list is read out it is therefor a single letter, not the whole string
#   Consequently the argument list has to be checked to not be an instance of string before accessing via iterator.


class Bot(discord.Client):

    async def on_ready(self):

        self.cfg = config
        self.util = Utility(self)

        await self.load_modules()

        print('Ready! (Logged in as {0}'.format(self.user) + ")")
        await self.send_message(self.get_channel(self.cfg.general['def_channel_id']), "Now online.")


    # Automatically creates instances of all modules which are configured in config and imported
    # Also creates dictionary for association of modules with their command argument
    # TODO: Check safety
    # TODO: Automate import
    # TODO: Maybe only pass utility instance to modules (to restrict access to bot)
    # TODO: Automatic execution of commands in intervals. Possibly through module and configurable through commands.
    async def load_modules(self):

        self.arg_mod_assoc = {}

        regex_arg = re.compile('^[A-Za-z0-9_]+$')

        # Create instances of all modules, get their command arguments and save them to dictionary
        count = 0
        for mod_class_name in self.cfg.modules:
            if regex_arg.match(mod_class_name):
                
                # Create instance
                mod_cl = globals()[mod_class_name]
                mod_inst = mod_cl(self)

                # Save to dictionary with command argument
                self.arg_mod_assoc[mod_inst.cmd_arg] = mod_inst
                count += 1

        print("Initialized " + str(count) + " modules.")


    # Runs "run" method in specified module
    async def on_message(self, message):

        if len(message.content) <= self.cfg.other['max_msg_len']:


            if await self.util.is_command(message.content):
                
                # Actions for command messages:

                executed = False

                cmd = message.content[len(self.cfg.general['cmd_op']):]     # Remove operator
                args = cmd.split(' ', self.cfg.other['max_args'])           # Split command into argument list
                
                # Call module specified by first argument
                if args[0] in self.arg_mod_assoc.keys():                    # If config contains module
                    try:
                        await self.run_module(args[0], args[1:], message)
                    except:
                        print('Unexpected Error.')
                    executed = True

                # Send error message if command is not in cmdList
                if not executed or not args[0]:
                    await self.util.send_error_message(message.channel, "No module for \'" + args[0] + "\' is configured.")


            # Actions for non-command messages:

            # Auto-delete messages in specified channels
            if message.channel.id in self.cfg.other['channel_ids_to_auto_delete_msgs']:
                await asyncio.sleep(self.cfg.other['auto_delete_delay_s'])
                await self.run_module('mgmt', ['delete', 'last', '1', message.author.id, 'silent'], message)


    # Call "run" function in specified module and pass message and args if available
    async def run_module(self, mod_arg, args=None, message=None):

        # print(mod_arg + " " + str(args))

        if isinstance(mod_arg, str) and mod_arg in self.arg_mod_assoc.keys():
            if args:
                if message:
                    return await getattr(self.arg_mod_assoc[mod_arg], 'run')(args, message)
                else:
                    return await getattr(self.arg_mod_assoc[mod_arg], 'run')(args)
            elif message:
                return await getattr(self.arg_mod_assoc[mod_arg], 'run')(None, message)
            else:
                return await getattr(self.arg_mod_assoc[mod_arg], 'run')()


    # Call "return_help" function in specified module and pass args if available
    async def return_module_help(self, mod_arg, args=None):

        if isinstance(mod_arg, str) and mod_arg in self.arg_mod_assoc.keys():
            if args:
                return await getattr(self.arg_mod_assoc[mod_arg], 'return_help')(args)
            else:
                return await getattr(self.arg_mod_assoc[mod_arg], 'return_help')()