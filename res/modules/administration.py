from ..module import Module


# TODO: Method to delete messages from all channels at once
class Administration(Module):

    cmd_arg = 'mgmt'
    deleted_messages = []   # Temporary storage of deleted messages


    async def run(self, args=None, message=None):

        arg_fct_assoc = {
            'delete':       'delete',
            'dump_deleted': 'dump_delete_messages',
        }

        # Call function associated with second argument
        if message and args:
            if args[0] in arg_fct_assoc.keys():
                if len(args) >= 2 and not isinstance(args, str):
                    await getattr(self, arg_fct_assoc[args[0]])(args[1:], message)
                else:
                    await getattr(self, arg_fct_assoc[args[0]])(None, message)
        else:
            await self.bot.run_module('help', [self.cmd_arg])


    async def return_help(self, args=None):
        return ("- `delete last [n(max=200)] [optional: user-id]`: Deletes the last n messages by anyone or optionally a user."
            "\n- `count-down [ss/mm:ss/hh:mm:ss] [optional: event name]`")


    # Executes different delete functions depending on third argument
    async def delete(self, args=None, message=None):

        arg_fct_assoc = {
            'last': 'delete_last_messages'
        }

        if args and message and len(args) >= 2 and not isinstance(args, str):
            if args[0] in arg_fct_assoc.keys():    # If command is registered
                await getattr(self, arg_fct_assoc[args[0]])(args[1:], message)
        else:
            await self.bot.run_module('help', [self.cmd_arg])



    # Deletes a specific number of messages, optionally by specific user
    #   1: limit, 2: user
    # TODO: Limit-counter may be wrong, alternatively write own counter and not purge_from
    # TODO: Delete from all channels if additional argument 'global' is given
    async def delete_last_messages(self, args, message):

        limit = None
        user_id = None
        
        max_limit = 200

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
            user_id = args[1]

        # Delete messages
        if message.author.server_permissions.manage_messages:
            if limit:
                
                # By user
                if user_id:
                    def is_user(m):
                        return str(user_id) == str(m.author.id)
                    
                    self.deleted_messages = await self.bot.purge_from(message.channel, limit=limit, check=is_user)
                    await self.bot.send_message(message.channel, "Deleted " + str(limit) + " messages by " + user_id + ".")
                    await self.dump_deleted_messages()
                
                # Too many arguments
                elif len(args) > 2:
                    await self.bot.run_module('help', self.cmd_arg)
                
                # By anyone
                else:
                    self.deleted_messages = await self.bot.purge_from(message.channel, limit=limit)
                    await self.bot.send_message(message.channel, "Deleted " + str(limit) + " messages.")
                    await self.dump_deleted_messages()

            else:
                await self.bot.run_module('help', self.cmd_arg)
        # TODO: 
        # else: 
        #   User doesn't have permission: Help message?


    async def dump_deleted_messages(self):
        print("Last deleted messages: ")
        for msg in self.deleted_messages:
            print(str(msg.author) + " (" + str(msg.author.nick) + ")" + ": " + str(msg.content))


    '''# Counts all messages in the channel the command was sent in
    async def count_messages(self, message=None):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=1000):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))



    # Display a countdown with an optional event field
    async def count_down(self, message=None):

        if message is not None:

            time_str = await self.bot.util.get_content_part(message.content, 2, 2)

            event_name = await self.bot.util.get_content_part(message.content, 3, 100)
            if event_name is None:
                event_name = ""
                event_name_until = ""
            else:
                event_name = "**"+event_name+"**"
                event_name_until = " until "+event_name

            time = await self.bot.util.time_str_to_sec(time_str)
            if time is not None:
                msg = await self.bot.util.send_message(message.channel, 'Counting: ')
                counter = time

                while counter > 0:
                    await self.bot.util.edit_message(msg, "Counting: " + await time_sec_to_str(counter) + event_name_until)
                    await asyncio.sleep(1)
                    counter -= 1

                await self.bot.util.edit_message(msg, 'Now! ' + event_name)

            else:
                await self.bot.util.help_message(message.channel, 'count-down')'''
    