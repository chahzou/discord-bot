import asyncio

from ..module import Module


class Test(Module):

    cmd_arg = 'test'


    # Performs different tests depending on argument
    async def run(self, args=None, message=None):

        if args:

            if args[0] == 'sleep':
                await asyncio.sleep(5)
                await message.channel.send('Done sleeping :O')
            elif args[0] == 'error':
                await self.bot.util.send_error_message(message.channel, "Test-Error")
                
            # Add other test options here

        else:
            await message.channel.send("It worked.")
    

    async def return_help(self, args=None):
        return ("- `test`: Return test message."
        "\n- `test sleep`: Sleep for 5 seconds, then return test message."
        "\n- `test error`: Return a test-error.")



    '''# Counts all messages in the channel the command was sent in
    async def count_messages(self, message=None):
        counter = 0
        tmp = await message.channel.send('Calculating messages...')
        async for log in client.logs_from(message.channel, limit=1000):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))



    # Display a countdown with an optional event field
    # - `count-down [ss/mm:ss/hh:mm:ss] [optional: event name]`
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
                msg = await message.channel.send('Counting: ')
                counter = time

                while counter > 0:
                    await self.bot.util.edit_message(msg, "Counting: " + await time_sec_to_str(counter) + event_name_until)
                    await asyncio.sleep(1)
                    counter -= 1

                await self.bot.util.edit_message(msg, 'Now! ' + event_name)

            else:
                await self.bot.util.help_message(message.channel, 'count-down')'''