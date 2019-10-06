from ..module import Module
from datetime import datetime, timedelta
import discord


class Administration(Module):

    cmd_arg = 'mgmt'

    ready_msg_toggle = True
    ready_msg = "Now online."
    
    # Channels to clear messages (unless protected) when the bot starts
    auto_clear_channel_ids = [497747060880048149, 497005261714620418]
    auto_clear_protected_msg_ids = [498792207562571787]

    # Channels to auto delete messages delayed (unless protected)
    auto_delete_msgs_channel_ids = [497747060880048149, 497005261714620418]
    auto_delete_delay_s = 10
    auto_delete_protected_msg_ids = [498792207562571787]

    leave_msg_toggle = True
    leave_msg_required_role = 'reg'
    leave_msg = " left the guild."    # Preceeded by the user who left the guild.


    async def on_ready(self):
        await self.clear_channels()
        await self.send_ready_message()


    async def on_member_remove(self, member):
        await self.send_leave_message(member)
    

    async def on_message(self, message):
        await self.auto_delete_messages(message)

    
    async def run(self, args=None, message=None):

        arg_fct_assoc = {
            'delete':       'delete',
            'prune':        'prune',
        }

        # Call function associated with second argument
        if message:
            if args:
                if args[0] in arg_fct_assoc.keys():
                    if len(args) >= 2 and not isinstance(args, str):
                        await getattr(self, arg_fct_assoc[args[0]])(args[1:], message)
                    else:
                        await getattr(self, arg_fct_assoc[args[0]])(None, message)
                else:
                    await message.channel.send("Command `" + args[0] + "` isn't available.")
                    await self.bot.run_module('help', [self.cmd_arg], message)
            else:
                await self.bot.run_module('help', [self.cmd_arg], message)
        else:
            await self.bot.run_module('help', [self.cmd_arg])


    async def return_help(self, args=None):
        return ("- `delete last [n (max=200)] [optional: user-id] [optional: 'silent']`: Deletes the last n messages in a channel (optionally by a user) if the author has the required rights. (The user-id can be copied by right-clicking on a user when in dev mode.)\n"
            "- `prune [type (message/login)] [days] [check/warn/proceed]`: Displays or kicks users who have been inactive (depending on type) for a specified amount of time."
            "")


    # Clear channels
    async def clear_channels(self):

        for channel_id in self.auto_clear_channel_ids:

            channel = self.bot.get_channel(channel_id)
            
            def not_protected(m):
                return not m.id in self.auto_clear_protected_msg_ids

            await channel.purge(limit=1000, check=not_protected)


    # Send ready message and delete last ready message
    async def send_ready_message(self):

        def_channel = await self.bot.util.get_channel('default')
        
        if self.ready_msg_toggle:
            def is_ready_msg(m):
                return m.content == self.ready_msg

            await def_channel.purge(limit=10, check=is_ready_msg)

            await def_channel.send(self.ready_msg)


    # Auto-delete messages in specified channels
    async def auto_delete_messages(self, message):

        if message.channel.id in self.auto_delete_msgs_channel_ids:
            if message.id in self.auto_delete_protected_msg_ids:
                pass
            else:
                await self.bot.util.delete_message_delayed(message, self.auto_delete_delay_s)


    # Executes different delete functions depending on third argument
    async def delete(self, args=None, message=None):

        arg_fct_assoc = {
            'last': 'delete_last_messages'
        }

        if args and message and len(args) >= 2 and not isinstance(args, str):
            if args[0] in arg_fct_assoc.keys():    # If command is registered
                await getattr(self, arg_fct_assoc[args[0]])(args[1:], message)
            else:
                await message.channel.send("Command `" + args[0] + "` isn't available.")
                await self.bot.run_module('help', [self.cmd_arg], message)
        else:
            await self.bot.run_module('help', [self.cmd_arg])


    # Deletes a specific number of messages, optionally by specific user
    #   1: limit, 2: user, 3: silent
    # TODO: Delete from all channels if additional argument 'global' is given (difficult)
    async def delete_last_messages(self, args, message):

        max_limit = 200

        limit = None
        user_id = None

        send_response = True
        silent_arg = 'silent'

        # guild_wide = False
        # guild_wide_arg = 'global'

        # Get arguments
        if isinstance(args, str):
            tmp_limit = args
        else:
            tmp_limit = args[0]

        if tmp_limit:
            tmp_limit = int(tmp_limit)
            if tmp_limit > max_limit:
                tmp_limit = max_limit
            limit = tmp_limit
        
        if not isinstance(args, str) and len(args) >= 2:

            if await self.bot.util.is_number(args[1]):
                user_id = args[1]

            if (silent_arg in i for i in args):
                send_response = False
            # if (guild_wide_arg in i for i in args):
            #     guild_wide = True
        
        # Delete messages
        if message.author.guild_permissions.manage_messages or message.author.id == user_id:
            if limit:

                deleted_messages = []
                
                # By user
                if user_id:

                    tmp_limit = limit

                    def is_user(m):
                        return str(user_id) == str(m.author.id)

                    # Limit for purge function only applies to amount of messages checked, not deleted (TODO: Could be a bug that got fixed!)
                    # This loop repeats the purge function while increasing the amount of messages checked depending on how many messages were skipped
                    while len(deleted_messages) < limit and tmp_limit <= max_limit:
                        tmp_deleted_messages = await message.channel.purge(limit=tmp_limit, check=is_user)
                        
                        deleted_messages += tmp_deleted_messages

                        amount_skipped = tmp_limit - len(tmp_deleted_messages)
                        tmp_limit = amount_skipped + limit - len(deleted_messages)

                    if send_response:
                        await message.channel.send("Deleted " + str(len(deleted_messages)) + " message(s) by " + user_id + ".")

                    if len(deleted_messages) > 0:
                        await self.bot.util.dump_messages(deleted_messages)
                
                # Too many arguments
                elif len(args) > 2:
                    await message.channel.send("Too many arguments. Make sure to use the user-id, not the name of the user.")
                    await self.bot.run_module('help', self.cmd_arg)
                
                # By anyone
                else:
                    deleted_messages = await message.channel.purge(limit=limit)

                    if send_response:
                        await message.channel.send("Deleted " + str(len(deleted_messages)) + " message(s).")

                    await self.bot.util.print("Deleted " + str(len(deleted_messages)) + " message(s) in " + message.channel.name + ".")
                    await self.bot.util.dump_messages(deleted_messages)

            else:
                await message.channel.send("This command requires a limit.")
                await self.bot.run_module('help', self.cmd_arg)
        else: 
            await message.channel.send("User doesn't have permission to delete these messages.")
            await self.bot.run_module('help', [self.cmd_arg])


    # Prune members who did not write a message in a specified number of days
    async def prune(self, args, message):

        # Check user rights: Kick Members
        if message.author.guild_permissions.kick_members:
            
            arg_fct_assoc = {
                'login':    'prune_by_login',
                'message':  'prune_by_message',
            }

            if args and not isinstance(args, str):
                if args[0] in arg_fct_assoc.keys():
                    if len(args) >= 2:
                        await getattr(self, arg_fct_assoc[args[0]])(args[1:], message)
                    else:
                        await getattr(self, arg_fct_assoc[args[0]])(None, message)
                else:
                    await self.bot.run_module('help', [self.cmd_arg])
            else:
                await self.bot.run_module('help', [self.cmd_arg])

        else:
            await message.channel.send("No permission to kick members.")


    async def prune_by_login(self, args, message):

        days_inactive = None
        check = False
        warn = False
        proceed = False

        if args:
            if not isinstance(args, str) and isinstance(args, list) and len(args) == 2:
                if args[0]:
                    days_inactive = int(args[0])
                if args[1]:
                    if args[1] == 'proceed':
                        proceed = True
                    elif args[1] == 'warn':
                        warn = True
                    elif args[1] == 'check':
                        check = True
            else:
                await self.bot.run_module('help', [self.cmd_arg])
        else:
            await self.bot.run_module('help', [self.cmd_arg])

        if days_inactive:

            # Log user count to prune
            if check:
                await message.guild.estimate_pruned_members(days=days_inactive)

            # Warn users who would be pruned
            elif warn:
                pass

            # Kick users
            elif proceed:
                await message.guild.prune_members(days=days_inactive)


    async def prune_by_message(self, args, message):
        
        days_inactive = None
        check = False
        warn = False
        proceed = False

        if args:
            if not isinstance(args, str) and isinstance(args, list) and len(args) >= 2:
                if args[0]:
                    days_inactive = int(args[0])
                if args[1]:
                    if args[1] == 'proceed':
                        proceed = True
                    elif args[1] == 'warn':
                        warn = True
                    elif args[1] == 'check':
                        check = True
            else:
                await self.bot.run_module('help', [self.cmd_arg])
        else:
            await self.bot.run_module('help', [self.cmd_arg])

        if days_inactive:
            # Check inactive days for all users

            active_members = []
            inactive_members = []
            now = datetime.now()
            earliest_date = now - timedelta(days=days_inactive)
            
            # Get active members
            for channel in message.guild.channels:
                if type(channel) is discord.channel.TextChannel:
                    async for m in channel.history(limit=None, after=earliest_date):
                        if not m.author in active_members:
                            active_members.append(m.author)
            
            # Subtract active members from all members and exclude those registrated within the timeframe
            for member in message.guild.members:
                if not member in active_members:
                    if member.joined_at < earliest_date:
                        inactive_members.append(member)

            if inactive_members:

                # Log inactive and active users
                if check:
                    print("Inactive members:")
                    for member in inactive_members:
                        print(" " + member.name)

                    print("Active members:")
                    for member in active_members:
                        print(" " + member.name)

                # Warn members who would be kicked
                elif warn:
                    warn_str = "The following members will be pruned due to inactivity for " + str(days_inactive) + " days: "
                    warn_str += inactive_members[0].mention
                    for member in inactive_members[1:]:
                        warn_str += ", " + member.mention
                    warn_str += "\nYou can simply send a message to avoid this."
                    await message.channel.send(warn_str)

                # Kick inactive users
                elif proceed:
                    for member in inactive_members:
                        await member.kick(reason="Inactivity for " + str(days_inactive) + " days.")
                        print("Kicked " + member.name)
            else:
                print("No inactive members found.")


    # Deletes all messages within a channel
    # TODO: Check for more than 200 messages
    async def clear_channel(self, channel):

        # Check if message is not protected
        def msg_not_protected(m):
            if m.id in self.auto_clear_protected_msg_ids: 
                return False
            else: 
                return True

        deleted_messages = await self.bot.purge_from(channel, limit=200, check=msg_not_protected)

        if len(deleted_messages) > 0:
            await self.bot.util.print("Deleted " + str(len(deleted_messages)) + " message(s) in " + channel.name + ".")
            await self.bot.util.dump_messages(deleted_messages)
    

    async def send_leave_message(self, member):
        if self.leave_msg_toggle:

            leave_channel = await self.bot.util.get_channel('leave')

            # Check required role
            if self.leave_msg_required_role:
                # role = await self.bot.util.get_role_by_name(member.guild, self.leave_msg_required_role)
                for role in member.roles:
                    if role.name == self.leave_msg_required_role:
                        await leave_channel.send(member.mention + self.leave_msg)
                        await self.bot.util.print(member.name + " left the guild " + member.guild.name + ".")
            else:
                await leave_channel.send(member.mention + self.leave_msg)
                await self.bot.util.print(member.name + " left the guild " + member.guild.name + ".")
    