class Utility:
    
    def __init__(self, bot):
        self.bot = bot


    async def is_command(self, msg_content):
        if msg_content.startswith(self.bot.cfg.general['cmd_op']):
            return True


    # Returns list of space-seperated arguments in string
    async def split_cmd_to_args_list(self, string):
        return string.split(' ', self.bot.cfg.other['max_args'])

    

    # Send info message
    async def info_message(self, channel, content):
        await self.bot.send_message(
            channel,
            "Info: " + content
        )


    # Sends an error message
    async def error_message(self, channel, content):
        await self.bot.send_message(
            channel, 
            "Error: " + content + "\nType `!help [command]` to list all possible commands or add a command to get more information."
        )


    # Returns module name associated with argument in cfg
    async def return_mod_for_arg(self, arg):
        return self.bot.cfg.arg_mod_assoc[arg]


    async def call_module_help(self, mod_arg):
        await self.bot.call_module_function('run', ['help', mod_arg])



    # Sends different help messages depending on second argument
    '''async def help_message(self, channel, cmd=None):

        out = ""

        if cmd is None:                    # If the help command is not specified, output a list of all possible commands.

            out += "Help menu: List of all possible commands: \n"

            counter = 0
            for key in self.bot.cfg.cmd_fct.keys():               # Iteration through all keys, adding them to output string
                out += "`!" + key + "`"
                if counter < len(self.bot.cfg.cmd_fct) - 1:         # Adds comma when not last element
                    out += ", "
                counter += 1

            out += "\nSpecify by typing `!help [command]`."

        # displays help for specific command if it is in cmd_list
        elif cmd in self.bot.cfg.cmd_fct:

            if cmd in self.bot.cfg.cmd_info:
                if self.bot.cfg.cmd_info[cmd] is not None and self.bot.cfg.cmd_info[cmd] != '':
                    out += "Help menu for `!" + cmd + "`:\n"
                    out += self.bot.cfg.cmd_info[cmd] + "\n"
            else:
                out += "Help menu for `!" + cmd + "`:\nSorry, there's no help available for this command yet."

        # Default if command is not found
        else:
            out += "Command `!" + cmd + "` does not exist."

        await self.bot.send_message(channel, out)'''