from core import bot
from os import getenv

if __name__ == '__main__':
    bot.Kakashi().run(getenv('TOKEN'))