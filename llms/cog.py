import discord
from discord.ext import commands
from llms.ollamaAsk import TextGenerator
import json



class LLMs(commands.Cog):
    def __init__(self, bot, controller):
        self.bot = bot
        self.ollama = TextGenerator()
        self.controller = controller

    @discord.app_commands.command(name= "llm_list", description="All commands About Large Langiage Models aka Ki/Ai")
    async def llm_list(self, interaction: discord.Interaction):
        print (interaction.user.id)
        models = await self.ollama.getList()
        print(models)
        newlist = ', '.join(list(models))
        await interaction.response.send_message(newlist)

    @discord.app_commands.command(name= "llm_model", description="All commands About Large Langiage Models aka Ki/Ai")
    async def llm_model(self, interaction: discord.Interaction, model : str):
        await interaction.response.send_message("Anwers")

    @discord.app_commands.command(name= "dow_model", description="All commands About Large Langiage Models aka Ki/Ai")
    async def llm_model(self, interaction: discord.Interaction, modelname : str):
        await interaction.response.send_message("Downloaded model correctly")
    
    @discord.app_commands.command(name= "ask_llama", description="Ask an LLM a question or give an task")
    async def ask_llama(self, interaction: discord.Interaction, modelname : str, question : str):
        await interaction.response.defer()
        usercontx = f'(Discord username{interaction.user} Discord user id {interaction.user.id})'
        answer = await self.ollama.askllama(modelname, question, usercontx)
        print(answer)
        
        await interaction.followup.send(answer)

    @discord.app_commands.command(name= "change_llm", description="Changes the LLm used by asking Smartie")
    async def changeLLM(self, interaction: discord.Interaction, modelname : str):
        await self.controller.changeLLM(modelname)
        
    @discord.app_commands.command(name= "instruct", description="Adds a instruction to the Bot")
    async def changeLLM(self, interaction: discord.Interaction, modelname : str):
        await self.controller.changeLLM(modelname)
    
async def setup(bot):
    await bot.add_cog(LLMs(bot, bot.controller_llm))