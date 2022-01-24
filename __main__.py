from kakashi.bot import Kakashi
from os import getenv

if __name__ == "__main__":
    Kakashi(getenv("TOKEN")).run()
