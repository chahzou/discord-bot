from ..module import Module

class Help(Module):

    cmd_arg = 'help'
    
    async def run(self, args=None, message=None):

        help_str = ""

        # Create help for specific module
        if args:
            if not isinstance(args, str):
                help_str = await self.create_help_for_module(args[0], args[1:])
            else:
                help_str = await self.create_help_for_module(args[0])
        
        # Create general help
        else:
            help_str = await self.create_help_general()

        # Send help message
        if message:
            await self.bot.send_message(message.channel, help_str)
        else:
            await self.bot.send_message(self.bot.get_channel(self.bot.cfg.general['def_channel_id']), help_str)


    async def create_help_general(self):

        mod_args_str = ''
        for mod_arg in self.bot.arg_mod_assoc.keys():
            if not mod_args_str:
                mod_args_str += "`" + mod_arg + "`"
            else:
                mod_args_str += ", `" + mod_arg + "`"

        return ("The following modules can currently be accessed: " + mod_args_str + "\nUse `" 
            + self.bot.cfg.general['cmd_op'] + "help [module]` for more information on each module.")
    

    async def create_help_for_module(self, mod_arg, args=None):

        mod_help_str = ''

        if args:
            mod_help_str = await self.bot.return_module_help(mod_arg, args)
        else:
            mod_help_str = await self.bot.return_module_help(mod_arg)
        
        print(mod_arg)
        mod_name = await self.bot.util.return_name_of_module(mod_arg)

        if isinstance(mod_help_str, str):
            return ("Help for " + mod_name + " (`" + mod_arg + "`):\n" + mod_help_str)
        else:
            self.bot.util.print_console_error("Module-Error: ", "Module method 'return_help' in " + 
                mod_name + " didn't return a string.")
        
        pass


    async def return_help(self, args=None):
        pass
