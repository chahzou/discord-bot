from ..module import Module

class Help(Module):
    
    async def run(self, message):

        mod_arg = await self.util.get_content_part(message.content, 2, 1)

        help_str = ""

        if mod_arg:
            help = await self.bot.call_module_function(mod_arg, 'return_help')
            if isinstance(help, str):
                help_str += "Help for `" + mod_arg + "`:\n" + help
            else:
                self.util.error_message(message.channel, "Module-Error: Module method 'return_help' didn't return a string.")

        else:
            mod_args = ''
            for arg in self.bot.config.arg_mod_assoc.values():
                if not mod_args:
                    mod_args += "`" + arg + "`"
                else:
                    mod_args += ", `" + arg + "`"

            help_str += ("The following modules can currently be accessed: " + mod_args + "\nUse `" 
                + self.bot.config.general['cmd_op'] + "help [module]` for more information on each module.")

        await self.bot.send_message(message.channel, help_str)


    async def return_help(self):
        pass