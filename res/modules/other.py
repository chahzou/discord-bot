# Temporary storage of deleted messages (useful?)
deleted_messages = []


# Performs different tests depending on second argument
async def test(message=None):
    if message is not None:
        arg = await get_content_part(message.content, 2, 2)

        if arg == 'sleep':
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Done sleeping :O')
        elif arg == 'error':
            await error_message(message.channel, "Test-Error")
        elif arg == 'role-order':
            for role in message.server.roles:
                print(role.name, role.position)

        # Other test options here.

        elif arg is not None:     # If second argument is not recognized
            await client.send_message(message.channel, "It worked. Now the other stuff you wrote: `"+arg+"`")
        else:
            await client.send_message(message.channel, "It worked.")



# Help command
async def help_command(message):
    cmd = await get_content_part(message.content, 2, 2)

    await help_message(message.channel, cmd)







# Executes different delete functions depending on second argument
async def delete(message=None):
    if message is not None:

        cmd = await get_content_part(message.content, 2, 2)

        if cmd in config.cmd_fct.keys():    # If command is in dictionary
            await getattr(this_module, '%s' % config.cmd_fct[cmd])(message)
        else:
            await help_message(message.channel, 'delete')



# Deletes a specific number of messages, optionally by specific user
async def delete_last_messages(message=None):

    global deleted_messages

    if message is not None:
        num = await get_content_part(message.content, 3, 3)
        user = await get_content_part(message.content, 4, 4)

        def num_isvalid(num_check):
            if num_check is not None:
                if num_check.isdigit():
                    if int(num_check) <= 200:
                        return True

        if num_isvalid(num):
            num = int(num)
            if user is None:
                if message.author.server_permissions.manage_messages:
                    deleted_messages = await client.purge_from(message.channel, limit=num)
                    print(deleted_messages)
            else:
                if message.author.server_permissions.manage_messages:

                    def is_user(m):
                        return str(m.author) == str(user)

                    deleted_messages = await client.purge_from(message.channel, limit=num, check=is_user)

                    # TODO: Counter is wrong! Wright with own counter and not purge_from!

                    print("Deleted messages: "+deleted_messages)
        else:
            await help_message(message.channel, 'delete')



# Counts all messages in the channel the command was sent in
async def count_messages(message=None):
    counter = 0
    tmp = await client.send_message(message.channel, 'Calculating messages...')
    async for log in client.logs_from(message.channel, limit=1000):
        if log.author == message.author:
            counter += 1

    await client.edit_message(tmp, 'You have {} messages.'.format(counter))



# Display a countdown with an optional event field
async def count_down(message=None):

    if message is not None:

        time_str = await get_content_part(message.content, 2, 2)

        event_name = await get_content_part(message.content, 3, 100)
        if event_name is None:
            event_name = ""
            event_name_until = ""
        else:
            event_name = "**"+event_name+"**"
            event_name_until = " until "+event_name

        time = await time_str_to_sec(time_str)
        if time is not None:
            msg = await client.send_message(message.channel, 'Counting: ')
            counter = time

            while counter > 0:
                await client.edit_message(msg, "Counting: " + await time_sec_to_str(counter) + event_name_until)
                await asyncio.sleep(1)
                counter -= 1

            await client.edit_message(msg, 'Now! ' + event_name)

        else:
            await help_message(message.channel, 'count-down')