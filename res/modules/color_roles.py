import re, asyncio, discord
from ..module import Module


# TODO: Fix/Update
# TODO: Method to sort colour-roles by name
class ColorRoles(Module):

    cmd_arg = 'color'
    regex_hex = r"#[\dABCDEFabcdef]{6}"     # Allows only a hashtag and 6 following hexadecimals


    async def run(self, args=None, message=None):

        if message:
            if args:
                if isinstance(args, str):       # Only one argument (list sometimes becomes string when passed as argument)
                    await self.set_color(args, message)
                elif len(args) == 1:
                    await self.set_color(args[0], message)
                else:
                    await self.bot.send_message(message.channel, "Too many arguments.")
                    await self.bot.run_module('help', self.cmd_arg, message)
            else:
                await self.bot.send_message(message.channel, "No arguments given.")
                await self.bot.run_module('help', self.cmd_arg, message)
        

    async def return_help(self, args=None):
        return ("- `!color [hex-code]` Use a hexadecimal code to set your username color (e.g. `!color #123456`). "
            "(Note: #000000 is Discord's default color, which varies depending on theme.)")
    
    
    # Gives the author of the command a role with the given color
    async def set_color(self, colour_arg, message):

        user = message.author
        colour = None
        colour_hex_name = None
        role_to_assign = None
        assigned = False


        # Set variables
        if isinstance(colour_arg, str):
            if re.match(self.regex_hex, colour_arg):     # Check if given argument is hex code, otherwise send help message
                colour = discord.Colour(int(colour_arg[1:], 16))
                if colour.value == 0:
                    await self.bot.send_message(message.channel, "Note: #000000 is Discord's default color, which varies depending on theme.")
                colour_hex_name = colour_arg

            else:
                await self.bot.send_message(message.channel, "Argument isn't a hexadecimal code.")
                await self.bot.run_module('help', self.cmd_arg, message)

        else:
            await self.bot.run_module('help', self.cmd_arg, message)


        # Check if user already has the colour and unassign other colour-roles
        for role in user.roles:
            if re.match(self.regex_hex, role.name):      # If role is a colour-role
                if role.name == colour_hex_name:                # If user already has the colour
                    await self.bot.send_message(message.channel, "The color " + colour_hex_name + " was already assigned.")
                    assigned = True
                else:
                    await self.bot.remove_roles(user, role)     # Unassign other colours


        if not assigned:
            for role in message.server.roles:           # Check if colour-role already exists
                if role.name == colour_hex_name:
                    role_to_assign = role

            if role_to_assign == None:                  # Otherwise create new role
                role_to_assign = await self.bot.create_role(message.server, name=colour_hex_name, colour=colour)
                # await self.bot.move_role(message.server, role_to_assign, len(message.server.roles) - 1)     # TODO: Check position
        
            # Assign the role
            await self.bot.add_roles(user, role_to_assign)
            await asyncio.sleep(1)                      # Wait 1 second to finish assigning role; TODO: Check if guaranteed solution


        # Check if role has been assigned
        if role_to_assign in user.roles:
            await self.bot.send_message(message.channel, "The color " + colour_hex_name + " was assigned.")
        
        await self.delete_unused_color_roles(message.server)


        # Original role position assignment:
        #   Use position beneath "bot" role position and add to message author
        '''for role in message.server.roles:       # Iteration through server roles:

            if role.name == 'bot':                  # Get "bot" role (for hierarchy reference)
                if role.position > 1:
                    position = role.position
                else:
                    position = 1'''


    # Delete all roles with the name of a hexcode which are not assigned to a user
    async def delete_unused_color_roles(self, server):

        for role in server.roles:
            if re.match(self.regex_hex, role.name):              # If role name is hex code

                used = False

                for member in server.members:               # Iteration of members
                    for member_role in member.roles:            # Iteration of roles of each member
                        if member_role == role:
                            used = True                             # when a member has the role -> role is used

                if not used:
                    await self.bot.delete_role(server, role)      # delete the role if it's not used
    
