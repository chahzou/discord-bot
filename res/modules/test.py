import re, asyncio, discord

from ..module import Module


class Test(Module):
    
    async def return_help(self):
        return ("`test`: Return test message."
        "\n`test sleep`: Sleep for 5 seconds, then return test message."
        "\n`test error`: Return a test-error.")


    # Performs different tests depending on argument
    async def run(self, message):

        if message.content:
            arg = await self.util.get_content_part(message.content, 2, 1)

            if arg == 'sleep':
                await asyncio.sleep(5)
                await self.bot.send_message(message.channel, 'Done sleeping :O')
            elif arg == 'error':
                await self.util.error_message(message.channel, "Test-Error")
                
            # Add other test options here

            else:
                await self.bot.send_message(message.channel, "It worked.")

