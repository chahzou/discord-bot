from ..module import Module

class Help(Module):

    cmd_arg = 'help'
    
    async def run(self, args, message=None):
        await self.send_help(args, message)


    # Send help message, optionally for module
    async def send_help(self, args, message=None):

        help_str = ""

        # Create help for specific module
        if args[1]:
            mod_help_str = await self.bot.call_module_function(args[0], 'return_help', args[1:])
            if isinstance(mod_help_str, str):
                help_str += "Help for `" + args[1] + "`:\n" + mod_help_str
            else:
                self.bot.util.error_message(message.channel, "Module-Error: Module method 'return_help' didn't return a string.")
        
        # Create general help
        else:
            mod_args_str = ''
            for mod_arg in self.bot.arg_mod_assoc.keys():
                if not mod_args_str:
                    mod_args_str += "`" + mod_arg + "`"
                else:
                    mod_args_str += ", `" + mod_arg + "`"

            help_str += ("The following modules can currently be accessed: " + mod_args_str + "\nUse `" 
                + self.bot.cfg.general['cmd_op'] + "help [module]` for more information on each module.")

        # Send help message
        await self.bot.send_message(message.channel, help_str)
    

    async def return_help(self, args):
        pass
