# Por Luis Gustavo Diniz 16/05/2025
import discord
import os
from discord import app_commands
from commands import setup_command

class RogersBot(discord.Client):
    
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="$",
            intents=intents
        )
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await setup_command(self)
        await self.tree.sync()

    async def on_ready(self):
        print(f"{self.user} está decolando! 🚀🚀")

bot = RogersBot()

TOKEN = os.getenv("BOT_TOKEN") # TOKEN DISCORD
bot.run(TOKEN)
