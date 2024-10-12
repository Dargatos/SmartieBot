from ollama import AsyncClient
import json
import asyncio
import json
import os
import ollama

class TextGenerator:
    def __init__(self):
        self.installedModels = {}
        self.model_name = "llama"
        self.ollama = ollama.AsyncClient(host = "http://localhost:11434")

        self.models = ollama.list()["models"]

        #for model in self.models:
        #    print(f"Available models are {model["name"]}")
        
    async def downloadModel(self, model):
        print("trying to download new model")
        try: 
            await self.ollama.pull(model)
            return f"{model} succesfully downloaded"
        except:
            return "Model not found check https://ollama.com/library for usable models"


    async def getList(self):
        modellist = []
        for model in self.models:
            modellist.append(model["name"])

        return (modellist)
    
    async def getInfo(self):
        # should return all info of a give model
        ...

    async def generateOllama(self,model,prompt, contx:str, ):

        response = self.ollama.generate(model = model,prompt="Hi how are u",)
        return response


    async def chatOllama(self,model,prompt, contx:str = {"No Context"}):
        print("got chat request")
        data = [
            {
                'role': 'system',
                'content': 
                "You are a Discord bot named Smartie. "
                "Your goal is to provide helpful and concise responses."
                "Do not decilne a response if its about opinion."
                "Answer like a human make jokes act cheecky, compassionate aso. and reference the people that are referenced in the conversation with their tag or name"
                "You usually dont have to introduce ur self"
                "Engage with users in a friendly and light-hearted manner, making jokes occasionally, but always stay respectful and appropriate. "
                "You are allowed to ping users using their user ID in the format <@userid>, but only when it makes sense in context and should never be excessive. "
                "Always look for ways to be helpful, and try not to respond with 'no' unless absolutely necessary. "
                "If the user asks for something you're unsure about, offer alternatives or suggestions instead of declining outright. "
                "U can expect that persons that are referrenced also see ur response so u can address them directly"
                f"Here is some context about the user who sent the message: {contx}."
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]

        if await self.checkModel(model):
            if model == "Moo:latest" or model == "llama_Un:latest" or model == "sunapi386/llama-3-lexi-uncensored:8b":
                print("Hallo ich heiße Mooritadsa")
                response = await self.ollama.chat(model = model,messages= [{'role': 'user','content':prompt}],stream=True )

            else:
                print("Not uncensored")
                response = await self.ollama.chat(model = model,messages=data,stream=True)

            final_response = ""
            async for chunk in response:
                final_response += chunk["message"]["content"]
                await self.saveJson(final_response)
                if chunk["done"] == True:
                    print("Sending")
                    return final_response
                    
    async def collectStreamResponse(self, response):
        final_response = ""
        async for chunk in response:
            final_response += chunk["message"]["content"]
            await self.saveJson(final_response)
            if chunk["done"] == True:
                print("Sending")
                return final_response


    #Save data in a json file
    async def saveJson(self,content):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'data.json')
        with open(file_path, 'w') as file:
            json.dump(content, file, indent=4)



    # Checks the list of all installed models and if the given one is Availabel
    async def checkModel(self, model):
        print(f"Cheking with model {model}")

        #Iterates through all models and comapres to the given one
        for installedmodel in self.models:
            if installedmodel["name"] == model:
                return	True
            
        print (f"{model} is not installed. Type any of the following installed models to get a response {await self.getList()} .")
        return False


async def testLLM():
    clas = TextGenerator()       
    result = await  clas.chatOllama("qwen:latest", "Hi")
    print(await clas.getList())
    print(f"Ai answer with :{result}")
    #print(clas.generate_text(input(), input()))
    #print(clas.getList())

if __name__ == '__main__':
    clas = TextGenerator()        
    asyncio.run(testLLM())
    