import discord
from discord.ext import commands
from llms.controller import LLMs

class LLamaBot(commands.Bot):
    llms : LLMs
    def initialise(self):
       self.llms = LLMs(self)
       

    async def process_message(self, message: discord.Message):
        await self.llms.process_message(message)

    async def Ki(self,Model):
        await self.llms.Ki(Model)

    