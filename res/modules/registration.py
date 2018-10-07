from ..module import Module

# Gives user a role and sends a welcome message
# TODO: Ability to assign registration roles to other users with command
class Registration(Module):

    cmd_arg = 'board'
    registration_roles = ['registered']
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
                    # Add roles
                    for role_name in self.registration_roles:
                        try:
                            role = await self.bot.util.get_role_by_name(message.server, role_name)
                            await self.bot.add_roles(user, role)
                        except Exception as e:
                            print("Couldn't give " + user.name + " the role " + role_name + " for registration.")
                            print(e)
                        
                    await self.bot.util.print("User " + user.name + " was registered on " + message.server.name)

                    # Assemble and send welcome message
                    def_channel = await self.bot.util.get_default_channel()
                    msg = self.welcome_msg + user.mention + ". " + self.about_msg
                    await self.bot.send_message(def_channel, msg)

                except Exception as e:
                    print("Couldn't complete registration. Check the permissions of the bot and registration roles: ")
                    print(*self.registration_roles, sep = ", ")
                    print(e)
                    await self.bot.util.send_error_message(message.channel, "Couldn't complete registration.")

                # Delete command for this action
                if self.auto_delete_cmd:
                    await self.bot.run_module('mgmt', ['delete', 'last', '1', user.id, 'silent'], message)


    async def return_help(self, args=None):
        return "`" + self.cmd_arg + "`: Assigns the author the registration role(s)."