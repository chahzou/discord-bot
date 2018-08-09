import asyncio

from ..module import Module


class Test(Module):

    cmd_arg = 'test'
    
    async def return_help(self, args):
        return ("`test`: Return test message."
        "\n`test sleep`: Sleep for 5 seconds, then return test message."
        "\n`test error`: Return a test-error.")


    # Performs different tests depending on argument
    async def run(self, args, message):

        if len(args) >= 2:

            if args[1] == 'sleep':
                await asyncio.sleep(5)
                await self.bot.send_message(message.channel, 'Done sleeping :O')
            elif args[1] == 'error':
                await self.bot.util.error_message(message.channel, "Test-Error")
                
            # Add other test options here

        else:
            await self.bot.send_message(message.channel, "It worked.")

