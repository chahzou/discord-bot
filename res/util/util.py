import re, datetime, asyncio


class Utility:
    
    def __init__(self, bot):
        self.bot = bot


    async def is_command(self, msg_content):
        if msg_content.startswith(self.bot.cfg.general['cmd_op']):
            return True

    
    # Send info message
    async def info_message(self, channel, content):
        await channel.send("Info: " + content)


    # Sends an error message
    async def send_error_message(self, channel, content):
        await channel.send(
            "Error: " + content + "\n" + 
                "Type `!help [command]` to list all possible commands or to get information on a particular command."
        )


    async def convert_camelcase_to_underscore(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    

    async def return_name_of_module(self, mod_arg):
        if isinstance(mod_arg, str):
            if self.bot.arg_mod_assoc[mod_arg]:
                return type(self.bot.arg_mod_assoc[mod_arg]).__name__
        return ''


    async def get_role_by_name(self, guild, role_name):
        for role in guild.roles:
            if role.name == role_name:
                return role


    async def get_channel(self, name):
        return self.bot.get_channel(self.bot.cfg.general['channels'][name])


    async def is_number(self, str):
        regex_arg = re.compile('^[0-9]+$')
        return regex_arg.match(str)


    async def print(self, text):
        now = datetime.datetime.now()
        print('[' + str(now.day) + '. ' + f"{now:%H}" + ':' + f"{now:%M}" + '] ' + text)
    

    async def delete_message_delayed(self, message, delay):
        msg_temp = message
        await asyncio.sleep(delay)
        await message.delete()
        await self.print("Deleted a message in channel " + msg_temp.channel.name)
        await self.dump_messages([msg_temp])


    async def dump_messages(self, messages):
        for msg in messages:
            name = str(msg.author)
            nick = ""
            try:
                nick = " (" + msg.author.nick + ")"
            except Exception:
                pass
            await self.bot.util.print("  " + name + nick + ": '" + msg.content + "'")


    async def print_console_error(self, type, content):
        print('(Error) ' + type + ': ' + content)
    

    # TODO
    async def get_latest_message_by_user(self, guild, user):

        pass


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

        await channel.send(out)'''
