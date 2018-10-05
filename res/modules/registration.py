from ..module import Module

# Gives user a role and sends a welcome message
# TODO: Ability to assign registration roles to other users with command
class Registration(Module):

    cmd_arg = 'board'
    registration_roles = ['on-board', 'passengers']
    welcome_msg = "Welcome, "     # Is followed by a user-mention. and the about message.
    about_msg = "See <#497747060880048149> for information on the server."
    auto_delete_cmd = False     # Deactivated because auto-delete is already channel-wide

    async def run(self, args=None, message=None):

        if message:
            if args:
                self.bot.run_module('help', [self.cmd_arg], message)
            else:
                user = message.author

                try:
                    for registration_role in self.registration_roles:
                        role = await self.bot.util.get_role_by_name(message.server, registration_role)
                        def_channel = await self.bot.util.get_default_channel()
                        await self.bot.add_roles(user, role)    # Add role
                        
                    await self.bot.util.print(user.name + " has been registered.")

                    # Assemble and send welcome message
                    msg = self.welcome_msg + user.mention + ". " + self.about_msg
                    await self.bot.send_message(def_channel, msg)

                except Exception as e:
                    print("Couldn't finish registration. Registration roles: ")
                    print(*self.registration_roles, sep = ", ")
                    print(e)
                    await self.bot.util.send_error_message(message.channel, "Couldn't complete registration.")

                if self.auto_delete_cmd:
                    await self.bot.run_module('mgmt', ['delete', 'last', '1', user.id, 'silent'], message)   # Delete command for this action


    async def return_help(self, args=None):
        return "`" + self.cmd_arg + "`: Assigns the author the registration role(s)."