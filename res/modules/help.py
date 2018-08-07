from ..module import Module

class Help(Module):
    
    async def run(self, args, message=None):
        mod_arg = None
        if len(args) >= 2:
            mod_arg = args[1]
        await self.send_help(mod_arg, message)


    # Send help message, optionally for module
    async def send_help(self, mod_arg=None, message=None):

        help_str = ""

        # Create help for specific module
        if mod_arg:
            mod_help_str = await self.bot.call_module_function('return_help', [mod_arg])
            if isinstance(mod_help_str, str):
                help_str += "Help for `" + mod_arg + "`:\n" + mod_help_str
            else:
                self.bot.util.error_message(message.channel, "Module-Error: Module method 'return_help' didn't return a string.")
        
        # Create general help
        else:
            mod_args_str = ''
            for arg in self.bot.config.arg_mod_assoc.values():
                if not mod_args_str:
                    mod_args_str += "`" + arg + "`"
                else:
                    mod_args_str += ", `" + arg + "`"

            help_str += ("The following modules can currently be accessed: " + mod_args_str + "\nUse `" 
                + self.bot.config.general['cmd_op'] + "help [module]` for more information on each module.")

        # Send help message
        await self.bot.send_message(message.channel, help_str)
    

    async def return_help(self):
        pass
