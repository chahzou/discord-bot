import pip, time, asyncio
from res.bot import Bot
from res.config import _access

# Install packages
# pip.main(['install', 'discord'])


# Run
def run_client(client, token):
    loop = asyncio.get_event_loop()
    while True:
        try:
            loop.run_until_complete(client.start(token))
        except Exception as e:
            print("Error", e)
        time.sleep(30)
        print("Attempting to restart.")

client = Bot()
run_client(client, _access.token)
