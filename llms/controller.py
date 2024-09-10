import discord
from pathlib import Path
import aiohttp
from llms.ollamaAsk import TextGenerator

class LLMs:
    def __init__(self, bot):
        self.Ollama = TextGenerator()
        self.bot = bot
        self.webhooks = {}
        self.standardLLM : str = "llama"
        self.currenLLM : str = self.standardLLM

    async def changeLLM(self, newllm):
        modellist = list(await self.Ollama.getList())
        if newllm in modellist:
            self.currenLLM = newllm
            print(f"Change LLM to {newllm}")

    async def process_message(self, message: discord.Message):


        if isinstance(message.channel, discord.DMChannel):
            if message.author == self.bot.user:
                return
            
            print("Text From DM detected")
            if message.content.startswith("LLm list"):
                modellist = await self.Ollama.getList()
                await message.reply(list(modellist))
            elif message.content.startswith("set LLM"):
                model = await self.ollamalistCheck(message)
                if model == False: await message.channel.send("Model doesnt exist")
                else:
                    self.currenLLM = model
                    print (f'Now Using {self.currenLLM} as LLM')
            else:
                usercontx = f'(Discord username{message.author} Discord user id {message.author.id})'
                response = await self.Ollama.askllama(self.currenLLM, message.content,usercontx)
                await message.channel.send(response)
                
            return

        if message.author.name == "zero_panda":
            await message.reply("Maul Lura")

        elif message.author.name == "rawaschuba":
            await message.reply("Rawa du süßer <3 U")


        if message.content == "Moin":
            await message.reply("Hoffe du hattest einen schlechten")

        elif message.content == "reset Avatar":
            await self.resetAvatar(message)

        elif message.content == "Moritz sag doch auch mal was":
            user_id = 528302192554147863
            avatar_url = await self.fetch_user_avatar(user_id)
            print(f"Fetched avatar URL: {avatar_url}")
            target_channel_id = message.channel.id
            await self.send_message_with_webhook(message,target_channel_id, "Ich bin ein Pinguin Quack Quack", "Moritz", avatar_url)

        

        if "Smartie" in message.content:
            usercontx = f'(Discord username{message.author} Discord user id {message.author.id})'
            text = await self.Ollama.askllama(self.currenLLM,message.content,usercontx)
            await message.reply(text)


        #await self.OllamaCheck(message)

    async def fetch_user_avatar(self, user_id):
        try:
            user = await self.bot.fetch_user(user_id)
            return user.avatar.url if user.avatar else None
        except discord.NotFound:
            print(f"User with ID {user_id} not found.")
            return None

    async def resetAvatar(self, message):
        current_dir = Path(__file__).parent
        parent_dir = current_dir.parent
        image_path = parent_dir / 'images' / 'Profile_picture.png'
        try:
            with open(image_path, 'rb') as avata:
                await self.bot.user.edit(avatar=avata.read())
                await message.channel.send("Avatar updated successfully!")
        except Exception as e:
            await message.channel.send(f"Failed to update avatar: {e}")

    async def delete_webhook(self,message, webhook_id: int):
        print("Deleting Webhook")
        channel_webhooks = await message.channel.webhooks() 
        for webhook in channel_webhooks: # iterate through the webhooks
            if webhook.name == "Moritz":
                await webhook.delete()
                break
        

    async def create_webhook(self,message, channel_id: int, name: str):
        channel_webhooks = await message.channel.webhooks() 
        for webhook in channel_webhooks: # iterate through the webhooks
            if webhook.name == "Moritz":
                print(f"Webhook names Moritz already created {webhook}")
                return webhook
            
        channel = self.bot.get_channel(channel_id)
        if not channel:
            print(f"Channel with ID {channel_id} not found.")
            return None

        try:
            print("Creating Webhook")
            webhook = await channel.create_webhook(name=name)
            print(f"Webhook created: {webhook.id}")
            return webhook
        except discord.HTTPException as e:
            print(f"Failed to create webhook in channel {channel_id}: {e}")
            return None

    async def send_message_with_webhook(self,message, channel_id: int, content: str, username: str, avatar_url: str):

        webhook = await self.create_webhook(message, channel_id, username)
        if webhook:
            self.webhooks[channel_id] = webhook.id
            webhook_url = f"https://discord.com/api/webhooks/{webhook.id}/{webhook.token}"

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(
                        webhook_url,
                        json={
                            "content": content,
                            "username": username,
                            "avatar_url": avatar_url
                        }
                    ) as resp:
                        if resp.status == 204:
                            print("Message sent successfully")
                        else:
                            print(f"Failed to send message, status code: {resp.status}")
                except Exception as e:
                    print(f"An error occurred while sending the message: {e}")

            #await self.delete_webhook(message, channel_id)



    # Checks if in the message was a LLM name and if sends a message if the corresponfings models ansewer
    async def OllamaCheck(self, message):
        model = await self.ollamalistCheck(message)
        if model:
            text = await self.Ollama.askllama(model,message.content)
            await message.reply(text)

    async def ollamalistCheck(self, message):
        text = message.content
        s = text.split(" ")
        
        modellist = list(await self.Ollama.getList())
        for i in s:
            if (i in modellist):
                print("Recognized Model")
                return i
        return False