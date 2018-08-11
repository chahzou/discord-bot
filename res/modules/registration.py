from ..module import Module


# Gives user a role and sends a welcome message
class Registration(Module):

    cmd_arg = 'stay'
    registration_role = 'staying'


    async def run(self, args=None, message=None):

        if message:
            if args:
                self.bot.run_module('help', [self.cmd_arg], message)
                # TODO: Ability to assign registration role to other users
            else:
                user = message.author
                # user_name = str(user.name) + "#" + str(user.discriminator)
                role = await self.bot.util.get_role_by_name(message.server, self.registration_role)
                def_channel = await self.bot.util.get_default_channel()

                await self.bot.add_roles(user, role)    # Add role
                await self.bot.send_message(def_channel, "Welcome " + user.mention + ".")   # Send welcome message
                await self.bot.run_module('mgmt', ['delete', 'last', '1', user.id], message)   # Delete command for this action


    async def return_help(self, args=None):
        return "- `" + self.cmd_arg + "`: Assigns the author the registration role."