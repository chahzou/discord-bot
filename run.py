import pip, time, asyncio
from res.bot import Bot
from res.config import _access

# Install packages
# pip.main(['install', 'discord'])


# Run
while True:

    asyncio.set_event_loop(asyncio.new_event_loop())
    client = Bot()
    # loop = asyncio.get_event_loop()

    try:
        # loop.run_until_complete(client.run(_access.token))
        client.run(_access.token)
        
    except Exception as e:
        print("Error", e)
        client.close()

    time.sleep(5)
    print("Attempting to restart.")

