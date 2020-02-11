import pip, time, asyncio, datetime
from res.bot import Bot
from res.config import _access

# Install packages
# pip.main(['install', 'discord'])


reconnect_timeout = 5

# Run
while True:

    asyncio.set_event_loop(asyncio.new_event_loop())
    client = Bot()
    loop = asyncio.get_event_loop()

    try:
        # loop.run_until_complete(client.run(_access.token))
        # client.run(_access.token)
        
        try:
            loop.run_until_complete(client.start(_access.token))
        finally:
            loop.run_until_complete(client.logout())
            # cancel all tasks lingering
            loop.close()
        
    except Exception as e:
        print("Error", e)
        # client.close()

    now = datetime.datetime.now()
    print('[' + str(now.day) + '. ' + f"{now:%H}" + ':' + f"{now:%M}" + '] Loop lost.')
    
    time.sleep(reconnect_timeout)
    
    now = datetime.datetime.now()
    print('[' + str(now.day) + '. ' + f"{now:%H}" + ':' + f"{now:%M}" + '] Attempting to restart.')
