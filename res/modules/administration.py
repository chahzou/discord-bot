from ..module import Module


# TODO: Method to delete messages from all channels at once
class Administration(Module):

    cmd_arg = 'mgmt'
    deleted_messages = []   # Temporary storage of deleted messages


    async def run(self, args=None, message=None):

        arg_fct_assoc = {
            'delete':       'delete_action',
            'dump_deleted': 'dump_delete_messages',
        }

        # Call function associated with second argument
        if message and args:
            if args[0] in arg_fct_assoc.keys():
                if args[1] and not isinstance(args, str):
                    await getattr(self, arg_fct_assoc[args[0]])(args[1:], message)
                else:
                    await getattr(self, arg_fct_assoc[args[0]])(message)
        else:
            await self.bot.run_module('help', [self.cmd_arg])


    async def return_help(self, args=None):
        return ("- `delete last [n(max=200)] [optional: user(user#1234)]`: Deletes the last n messages by anyone or an optional user."
            "\n- `count-down [ss/mm:ss/hh:mm:ss] [optional: event name]`")


    # Executes different delete functions depending on third argument
    async def delete(self, args, message):

        arg_fct_assoc = {
            'last': 'delete_last_messages'
        }

        if args[0] in arg_fct_assoc.keys():    # If command is registered
            if args[1] and not isinstance(args, str):
                await getattr(self, arg_fct_assoc[args[0]])(args[1:], message)
        else:
            await self.bot.run_module('help', [self.cmd_arg])



    # Deletes a specific number of messages, optionally by specific user
    #   1: limit, 2: user
    async def delete_last_messages(self, args, message):

        global deleted_messages
        max = 200

        limit = args[0]

        if message.author.server_permissions.manage_messages:
            if limit and limit.isdigit():

                limit = int(limit)
                if limit > max:
                    limit = max

                user = args[1]

                if user:

                    def is_user(m):
                        return str(user) is str(m.author)
                    
                    deleted_messages = await self.bot.purge_from(message.channel, limit=limit, check=is_user)
                    # TODO: Counter is wrong! Maybe write with own counter and not purge_from!
                    
                else:
                    deleted_messages = await self.bot.purge_from(message.channel, limit=limit)
                    self.dump_deleted_messages()    # TODO: Remove as it is debugging
            
        # else:
        #     await self.bot.util.send_help_message(self.bot.cfg. delete', message)


    async def dump_deleted_messages(self):
        print("Deleted messages: " + deleted_messages)


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
    