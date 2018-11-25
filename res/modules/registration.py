from ..module import Module
import asyncio


# Gives user a role and sends a welcome message
# TODO: Ability to assign registration roles to other users with command
class Registration(Module):

    cmd_arg = 'register'
    
    channel_ids = ["497005261714620418"]
    roles = ['reg', 'reg2']

    delay = 3
    delay_msg_pre = "Welcome, the registration will finish soon."
    delay_msg_late = ""

    welcome_msg = "Welcome, "     # Is followed by a user-mention. and the about message.
    about_msg = "See <#497747060880048149> for information on the server."
    auto_delete_cmd = False


    async def run(self, args=None, message=None):

        if message:
            if args:
                self.bot.run_module('help', [self.cmd_arg], message)
            else:

                if message.channel.id in self.channel_ids:

                    user = message.author

                    # Check if user doesn't have any registration roles yet
                    if not set(self.roles).issubset([role.name for role in user.roles]):

                        # Process delay
                        if self.delay >= 0:

                            if self.delay_msg_pre:
                                await self.bot.send_message(message.channel, self.delay_msg_pre)
                            await asyncio.sleep(self.delay * 0.9)
                            
                            if self.delay_msg_late:
                                await self.bot.send_message(message.channel, self.delay_msg_late)
                            await asyncio.sleep(self.delay * 0.1)

                        # Proceed with registration
                        # Check if user is still member of the server and hasn't registration roles yet
                        if user in message.server.members and not set(self.roles).issubset([role.name for role in user.roles]):

                            # Add roles
                            try:
                                for role_name in self.roles:
                                    try:
                                        role = await self.bot.util.get_role_by_name(message.server, role_name)
                                        await self.bot.add_roles(user, role)
                                        await asyncio.sleep(0.5)
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
                                print(*self.roles, sep = ", ")
                                print(e)
                                await self.bot.util.send_error_message(message.channel, "Couldn't complete registration.")
                        else:
                            await self.bot.util.print("User " + user.name + " left the server " + message.server.name + " before the registration could be completed.")
                            
                    else:
                        await self.bot.send_message(message.channel, "You are already registered.")
                        await self.bot.util.print("User " + user.name + " is already registered on " + message.server.name)
                
                else:
                    await self.bot.util.print("Registration ignored because it is not in a specified channel.")


                # Delete command for this action
                if self.auto_delete_cmd:
                    await self.bot.run_module('mgmt', ['delete', 'last', '1', user.id, 'silent'], message)


    async def return_help(self, args=None):
        return "`" + self.cmd_arg + "`: Assigns the author the registration role(s)."