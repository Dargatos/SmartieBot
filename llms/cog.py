import discord
from discord.ext import commands
from llms.ollamaAsk import TextGenerator



class LLMs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ollama = TextGenerator()

    @discord.app_commands.command(name= "llm_list", description="All commands About Large Langiage Models aka Ki/Ai")
    async def llm_list(self, interaction: discord.Interaction):
        models = self.ollama.getList()
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
    async def ask_llama(self, interaction: discord.Interaction, modelname : str, question : str = "Describe what u are to an Discord user. [Context: U are an Bot, there are multiple diffrent models the discrod user can use, a insider is that everyones nickname on the server has somethi to do with tree]"):
        await interaction.response.defer()
        answer = self.ollama.generate_text(modelname, question)
        print(answer)
        
        await interaction.followup.send(answer)

    
async def setup(bot):
    await bot.add_cog(LLMs(bot))