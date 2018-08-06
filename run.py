from res.bot import Bot
from res.config import _access

# Runs the bot
client = Bot()
client.run(_access.token)