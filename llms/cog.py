import discord
from discord.ext import commands
from llms.ollamaAsk import TextGenerator
import json
import random
from typing import Optional



class LLMs(commands.Cog):
    def __init__(self, bot, controller):
        self.bot = bot
        self.ollama = TextGenerator()
        self.controller = controller
        self.model_list = []
        

    async def loadmodellist(self):
        self.model_list = await self.ollama.getList()
        print(self.model_list)


    async def model_autocomplete(self, interaction: discord.Interaction, current: str):
        # Return the models that match the current input
        return [
            discord.app_commands.Choice(name=model, value=model)
            for model in self.model_list if current.lower() in model.lower()
        ]
        

    async def send_long_message(self, interaction, text):
        await interaction.followup.send("Answer is :")
        # Break the text into 2000 character chunks
        chunk_size = 2000
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        
        # Send each chunk
        for chunk in chunks:
            await interaction.channel.send(chunk)

    @discord.app_commands.command(name= "llm_list", description="All commands About Large Langiage Models aka Ki/Ai")
    async def llm_list(self, interaction: discord.Interaction):
        print (interaction.user.id)
        models = await self.ollama.getList()
        print(models)
        newlist = ', '.join(list(models))
        float = random.random()
        print (float)
        await interaction.response.send_message(newlist)

    @discord.app_commands.command(name= "llm_model", description="All commands About Large Langiage Models aka Ki/Ai")
    async def llm_model(self, interaction: discord.Interaction, model : str):
        await interaction.response.send_message("Anwers")


    @discord.app_commands.command(name="ask_llama", description="Ask an LLM a question or give it a task")
    @discord.app_commands.autocomplete(model=model_autocomplete)
    async def ask_llama(self, interaction: discord.Interaction, question: str, model: str = "llama:latest"):
        await interaction.response.defer()
        user_context = f'(Discord username: {interaction.user}, Discord user ID: {interaction.user.id})'
        answer = await self.ollama.chatOllama(model, question, user_context)
        print(answer)
        if answer == None: await interaction.followup.send("Idk sth bad happend f that shit")
        if len(answer) > 2000:
            await self.send_long_message(interaction, answer)
        else: 
            await interaction.followup.send(answer)

    @discord.app_commands.command(name= "change_llm", description="Changes the LLm used by asking Smartie")
    async def changeLLM(self, interaction: discord.Interaction, modelname : str):
        await self.controller.changeLLM(modelname)
        
    @discord.app_commands.command(name= "instruct", description="Adds a instruction to the Bot")
    async def instuct(self, interaction: discord.Interaction, modelname : str):
        await self.controller.changeLLM(modelname)
    
    @discord.app_commands.command(name= "downloadmodel", description="Downloads a given Model from Ollama")
    async def downloadModel(self, interaction: discord.Interaction, modelname : str):
        await interaction.response.defer()
        state = await self.ollama.downloadModel(modelname)
        await interaction.followup.send(state)



        
async def setup(bot):
    cog = LLMs(bot, bot.controller_llm)
    await cog.loadmodellist()  # Perform asynchronous initialization
    await bot.add_cog(cog)