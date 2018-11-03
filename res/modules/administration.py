from ..module import Module


# TODO: Method to delete messages from all channels at once
class Administration(Module):

    cmd_arg = 'mgmt'

    ready_msg_toggle = True
    ready_msg = "Now online."
    
    # Clears messages (unless protected) in channels when the bot starts
    auto_clear_channel_ids = ['497005261714620418', '497747060880048149']
    auto_clear_protected_msg_ids = ['498792207562571787']

    # Deletes new messages in channels delayed (unless protected)
    auto_delete_msgs_channel_ids = ['497005261714620418', '497747060880048149']
    auto_delete_delay_s = 10
    auto_delete_protected_msg_ids = ['498792207562571787']

    leave_msg_toggle = True
    leave_msg_required_role = 'reg'
    leave_msg = " left the server."    # Preceded by the user who left the server.


    async def on_ready(self):
        
        # Clear channels
        for channel_id in self.auto_clear_channel_ids:
            channel = self.bot.get_channel(channel_id)
            await self.clear_channel(channel)

        def_channel = await self.bot.util.get_default_channel()

        # Send ready message
        if self.ready_msg_toggle:
            # Delete last ready message within 10 messages
            await self.delete_message_by_content(def_channel, self.ready_msg, 10, self.bot.user)

            await self.bot.send_message(def_channel, self.ready_msg)
    

    async def on_member_remove(self, member):
        await self.send_leave_message(member)
    

    async def on_message(self, message):
        
        # Auto-delete messages in specified channels
        if message.channel.id in self.auto_delete_msgs_channel_ids:
            if message.id in self.auto_delete_protected_msg_ids:
                pass
            else:
                await self.bot.util.delete_message_delayed(message, self.auto_delete_delay_s)
    

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
                    await self.bot.send_message(message.channel, "Command `" + args[0] + "` isn't available.")
                    await self.bot.run_module('help', [self.cmd_arg], message)
            else:
                await self.bot.run_module('help', [self.cmd_arg], message)
        else:
            await self.bot.run_module('help', [self.cmd_arg])


    async def return_help(self, args=None):
        return ("- `delete last [n (max=200)] [optional: user-id] [optional: 'silent']`: Deletes the last n messages, optionally by a user, if the author has the required rights. (The user-id can be copied by right-clicking on a user when in dev mode.)"
            "")


    # Executes different delete functions depending on third argument
    async def delete(self, args=None, message=None):

        arg_fct_assoc = {
            'last': 'delete_last_messages'
        }

        if args and message and len(args) >= 2 and not isinstance(args, str):
            if args[0] in arg_fct_assoc.keys():    # If command is registered
                await getattr(self, arg_fct_assoc[args[0]])(args[1:], message)
            else:
                await self.bot.send_message(message.channel, "Command `" + args[0] + "` isn't available.")
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

        # server_wide = False
        # server_wide_arg = 'global'

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
            # if (server_wide_arg in i for i in args):
            #     server_wide = True
        
        # Delete messages
        if message.author.server_permissions.manage_messages or message.author.id == user_id:
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
                        tmp_deleted_messages = await self.bot.purge_from(message.channel, limit=tmp_limit, check=is_user)
                        
                        deleted_messages += tmp_deleted_messages

                        amount_skipped = tmp_limit - len(tmp_deleted_messages)
                        tmp_limit = amount_skipped + limit - len(deleted_messages)

                    if send_response:
                        await self.bot.send_message(message.channel, "Deleted " + str(len(deleted_messages)) + " message(s) by " + user_id + ".")

                    if len(deleted_messages) > 0:
                        await self.bot.util.dump_messages(deleted_messages)
                
                # Too many arguments
                elif len(args) > 2:
                    await self.bot.send_message("Too many arguments. Make sure to use the user-id, not the name of the user.")
                    await self.bot.run_module('help', self.cmd_arg)
                
                # By anyone
                else:
                    deleted_messages = await self.bot.purge_from(message.channel, limit=limit)

                    if send_response:
                        await self.bot.send_message(message.channel, "Deleted " + str(len(deleted_messages)) + " message(s).")

                    await self.bot.util.print("Deleted " + str(len(deleted_messages)) + " message(s) in " + message.channel.name + ".")
                    await self.bot.util.dump_messages(deleted_messages)

            else:
                await self.bot.send_message(message.channel, "This command requires a limit.")
                await self.bot.run_module('help', self.cmd_arg)
        else: 
            await self.bot.send_message(message.channel, "User doesn't have permission to delete these messages.")
            await self.bot.run_module('help', [self.cmd_arg])


    # Prune members who did not write a message in a specified number of days
    # TODO: Implement
    async def prune(self, args, message):

        # Check user rights: Kick Members
        if message.author.server_permissions.kick_members:

            days_inactive = None
            silent = False

            if args:
                if isinstance(args, str):
                    days_inactive = args
                elif isinstance(args, list) and args[0]:
                    days_inactive = args[0]

                if not isinstance(args, str) and args[1]:
                    if args[1] == 'silent':
                        silent = True
            
            # Check inactive days for all users
            if days_inactive:
                count = 0
                for member in message.server.members:
                    # Get latest message
                    
                    pass

            else:
                await self.bot.run_module('help', [self.cmd_arg])

        else:
            await self.bot.util.send_message(message.channel, "User doesn't have permission to kick members.")


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
    

    # Delete message by content
    async def delete_message_by_content(self, channel, content, search_limit=10, user=None):
        log = self.bot.logs_from(channel, limit=search_limit)
        async for msg in log:
            if msg.content == content:
                if user:
                    if msg.author == user:
                        await self.bot.delete_message(msg)
                else:
                    await self.bot.delete_message(msg)
                break
    

    async def send_leave_message(self, member):
        if self.leave_msg_toggle:

            def_channel = await self.bot.util.get_default_channel()

            # Check required role
            if self.leave_msg_required_role:
                # role = await self.bot.util.get_role_by_name(member.server, self.leave_msg_required_role)
                for role in member.roles:
                    if role.name == self.leave_msg_required_role:
                        await self.bot.send_message(def_channel, member.mention + self.leave_msg)
                        await self.bot.util.print(member.name + " left the server.")
            else:
                await self.bot.send_message(def_channel, member.mention + self.leave_msg)
                await self.bot.util.print(member.name + " left the server.")
    