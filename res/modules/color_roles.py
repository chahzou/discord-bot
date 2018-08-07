import re, asyncio, discord
from ..module import Module


class ColorRoles(Module):

    async def run(self):
        pass

    # TODO: Change get_content_part to args
    
    # Gives the author of the command a role with the given color
    async def set_color(self, message=None):

        regex = r"#[\dABCDEFabcdef]{6}"     # Allows only hashtag and 6 following hexadecimals

        if message is not None:
            member = message.author
            color_hex_input = await self.bot.get_content_part(message.content, 2, 2)

            if color_hex_input is not None:
                if re.match(regex, color_hex_input):      # check if given argument is hex code, otherwise send help message

                    color_hex = color_hex_input

                    for role in member.roles:                   # Uncheck other color roles with name "#hexcode"
                        if re.match(regex, role.name):
                            await self.bot.remove_roles(member, role)

                    color_hex_raw = int(color_hex[1:], 16)
                    role_to_assign = None
                    position = None

                    for role in message.server.roles:       # Iteration through server roles:

                        if role.name == 'bot':                  # Get "bot" role (for hierarchy reference)
                            if role.position > 1:
                                position = role.position
                            else:
                                position = 1

                        if role.name == color_hex:              # If existing use role with name of new color already exists
                            role_to_assign = role

                    if role_to_assign is None:                              # Otherwise create new role
                        role_to_assign = await self.bot.create_role(message.server, name=color_hex,
                                                                colour=discord.Colour(color_hex_raw))

                    # Use position beneath "bot" role position and add to message author
                    await self.bot.move_role(message.server, role_to_assign, position)

                    await self.bot.add_roles(member, role_to_assign)
                    await asyncio.sleep(1)                      # Wait 1 second to finish assigning role
                    # TODO: Guaranteed solution?

                    if role_to_assign in member.roles:

                        await self.bot.send_message(message.channel, "Color assigned: "+color_hex)
                        print("Color assigned in ", message.server.name)

                        await self.delete_unused_color_roles(message)
                else:
                    await self.bot.util.help_message(message.channel, 'color')
            else:
                await self.bot.util.help_message(message.channel, 'color')



    # Delete all roles with the name of a hexcode which are not assigned to a user
    async def delete_unused_color_roles(self, message=None):

        regex = r"#[\dABCDEFabcdef]{6}"

        if message:
            server = message.server

            for role in server.roles:
                if re.match(regex, role.name):              # If role name is hex code

                    used = False
                    for member in server.members:               # Iteration of members
                        for member_role in member.roles:            # Iteration of roles of each member
                            if member_role == role:
                                used = True                             # when a member has the role -> role is used

                    if used is False:
                        await self.bot.delete_role(message.server, role)      # delete the role if it's not used
    

    async def return_help(self):
        return "Use `color [hex-code]` to set your username color, for example #123456."