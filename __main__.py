from kakashi.core import bot
from os import getenv

if __name__ == "__main__":
    kakashi = bot.Kakashi()
    kakashi.run(getenv("TOKEN"))
