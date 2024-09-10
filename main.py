import discord
from discord.ext import commands

from llms.controller import LLMs as ControllerLLMs
from baseclasses.bot import LLamaBot
import settings

def run():
    intents = discord.Intents.all()
    intents.message_content = True

    bot = LLamaBot(command_prefix="/", intents=intents)
    bot.initialise()


    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')

        controller_llm = ControllerLLMs(bot)
        bot.controller_llm = controller_llm

        await bot.load_extension("llms.cog")



    @bot.event
    async def on_message(message: discord.Message):
        await bot.controller_llm.process_message(message)

        await bot.process_commands(message)




    @discord.app_commands.command(name= "hello", description="Fuck u")
    async def hello(interaction: discord.Interaction, arg1 : str):
        print(arg1)
        await interaction.response.send_message(arg1)



    @discord.app_commands.command(name='sync', description='Owner only')
    async def sync(interaction: discord.Interaction):
        
        await interaction.response.defer()
        print("GooD")
        # Sync application (slash) commands
        try:
            guild = discord.Object(id=753254997591851118)
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} commands globally.")
        except Exception as e:
            print(f"Failed to sync commands: {e}")

    @discord.app_commands.command(name="be_nice_to_lura", description="Secret")
    async def be_nice(interaction: discord.Interaction):
        await interaction.response.send_message(" toggled to stop Bully Lura")

    bot.tree.add_command(be_nice)
    bot.tree.add_command(sync)
    bot.tree.add_command(hello)

    bot.run(settings.DISCORD_TOKEN)



if __name__ == "__main__":
    run()