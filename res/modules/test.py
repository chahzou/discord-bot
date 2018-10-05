import asyncio

from ..module import Module


class Test(Module):

    cmd_arg = 'test'


    # Performs different tests depending on argument
    async def run(self, args=None, message=None):

        if args:

            if args[0] == 'sleep':
                await asyncio.sleep(5)
                await self.bot.send_message(message.channel, 'Done sleeping :O')
            elif args[0] == 'error':
                await self.bot.util.error_message(message.channel, "Test-Error")
                
            # Add other test options here

        else:
            await self.bot.send_message(message.channel, "It worked.")
    

    async def return_help(self, args=None):
        return ("- `test`: Return test message."
        "\n- `test sleep`: Sleep for 5 seconds, then return test message."
        "\n- `test error`: Return a test-error.")
