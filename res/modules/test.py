import re, asyncio, discord

from ..module import Module


class Test(Module):
    
    # Performs different tests depending on argument
    async def run(self, message=None):

        if message.content:
            arg = await self.util.get_content_part(message.content, 2, 1)

            if arg == 'sleep':
                await asyncio.sleep(5)
                await self.bot.send_message(message.channel, 'Done sleeping :O')
            elif arg == 'error':
                await self.util.error_message(message.channel, "Test-Error")
            elif arg == 'role-order':
                for role in message.server.roles:
                    print(role.name, role.position)
                await self.bot.send_message(message.channel, 'Printed the roles on the console.')

            # Add other test options here

            else:
                await self.bot.send_message(message.channel, "It worked.")