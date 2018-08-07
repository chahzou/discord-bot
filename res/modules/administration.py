from ..module import Module


class Administration(Module):


    # Temporary storage of deleted messages (useful?)
    deleted_messages = []

    arg2_fct_assoc = {
        'delete': 'delete_action',
    }

    # TODO: Change get_content_part and message to args

    async def run(self, args, message=None):
        
        if message:
            arg2 = await self.bot.util.get_content_part(message.content, 2, 1)

            # Call function associated with second argument
            if arg2 in self.arg2_fct_assoc:
                await getattr(self, '%s' % self.arg2_fct_assoc[arg2])(message)


    async def return_help(self):
        return ("`delete last [number] [optional: user]` - Deletes the last x(max=200) messages by anyone or an optional user."
            "\n`count-down [ss/mm:ss/hh:mm:ss] [optional: event name]`")


    # Executes different delete functions depending on third argument
    async def delete(self, message=None):

        arg3_fct_assoc = {
            'last': 'delete_last_messages'
        }

        if message:

            arg3 = await self.bot.util.get_content_part(message.content, 3, 1)

            if arg3 in self.bot.config.cmd_fct.keys():    # If command is in dictionary
                await getattr(self, '%s' % arg3_fct_assoc[arg3])(message)
            else:
                await self.bot.util.help_message(message.channel, 'delete')



    # Deletes a specific number of messages, optionally by specific user
    async def delete_last_messages(self, message=None):

        global deleted_messages

        if message is not None:
            num = await self.bot.util.get_content_part(message.content, 4, 1)
            user = await self.bot.util.get_content_part(message.content, 5, 1)

            def num_isvalid(num_check):
                if num_check is not None:
                    if num_check.isdigit():
                        if int(num_check) <= 200:
                            return True

            if num_isvalid(num):
                num = int(num)
                if user is None:
                    if message.author.server_permissions.manage_messages:
                        deleted_messages = await self.bot.purge_from(message.channel, limit=num)
                        print(deleted_messages)
                else:
                    if message.author.server_permissions.manage_messages:

                        def is_user(m):
                            return str(m.author) == str(user)

                        deleted_messages = await self.bot.purge_from(message.channel, limit=num, check=is_user)

                        # TODO: Counter is wrong! Wright with own counter and not purge_from!

                        print("Deleted messages: "+deleted_messages)
            # else:
            #     await self.bot.util.send_help_message(self.bot.config. delete', message)



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
    