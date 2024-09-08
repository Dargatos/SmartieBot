import os
import pathlib
from dotenv import load_dotenv

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", 0))

BASE_DIR = pathlib.Path(__file__).parent