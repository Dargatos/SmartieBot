from ollama import Client
import requests
import json
import subprocess
import asyncio
import json
import os

class TextGenerator:
    def __init__(self):
        self.installedModels = {}
        self.model_name = "llama"
        self.ollama = Client(host = "http://localhost:11434")


        result = subprocess.run("ollama list", shell=True, capture_output=True, text=True) #Can be done diffrent better
        output = result.stdout
        #print("Command Output:\n", output)
        lines = output.splitlines()

        # Iterate over the lines
        for i, line in enumerate(lines[3:]):
            # Split the line by spaces to get individual words
            model = line.split(":")
            name = line.split()[0]
            # Check if there is at least one word in the line
            if model:
                first_word = model[0]  # Get the first word
                #self.installedModels.append(first_word)
                self.installedModels[first_word] = name


        #print(self.installedModels)


    async def getList(self):
        return (self.installedModels)
    
    async def generateOllama(self,model,prompt, contx:str, ):

        response = self.ollama.generate(model = model,prompt="Hi how are u",)
        return response


    async def chatOllama(self,model,prompt, contx:str):
        data = [
            {
                'role': 'system',
                'content': 
                "You are a Discord bot named Smartie. "
                "Your goal is to provide helpful and concise responses. "
                "Engage with users in a friendly and light-hearted manner, making jokes occasionally, but always stay respectful and appropriate. "
                "You are allowed to ping users using their user ID in the format <@userid>, but only when it makes sense in context and should never be excessive. "
                "Always look for ways to be helpful, and try not to respond with 'no' unless absolutely necessary. "
                "If the user asks for something you're unsure about, offer alternatives or suggestions instead of declining outright. "
                f"Here is some context about the user who sent the message: {contx}."
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]

        if await self.checkModel(model):
            if model == "Moo:latest" or model == "llama_Un:latest":
                print("Hallo ich heiße Mooritadsa")
                response = self.ollama.chat(model = model,messages={'role': 'user','content':{prompt}})
            else:
                response = self.ollama.chat(model = model,messages=data)

            await self.saveJson(response)

            finalresponse = response["message"]["content"]
            return finalresponse
        


    #Save data in a json file
    async def saveJson(self,content):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, 'data.json')
        with open(file_path, 'w') as file:
            json.dump(content, file, indent=4)
        print(f"Data saved to {file_path}")



    async def checkModel(self, model):
        #Checks if given model is installed 
        if model not in self.installedModels:
            return f"{model} is not installed. Type any of the following installed models to get a response {list(self.installedModels)} ."
        print(f"Model check was succesful with model: {self.installedModels[model]}")

        # Since installed models are stored wierdly it needs to extract the real name of it other wiser idk
        model = self.installedModels[model]
        return True

    async def collectStreamResponse(self,response):
        try:
            # Initialize an empty string to collect all parts of the response
            collected_data = ""

            for line in response.iter_lines():
                if line:
                    # Decode and load each JSON line
                    try:
                        line_data = json.loads(line.decode('utf-8'))
                        # If the 'done' field is True, break out of the loop
                        if line_data.get("done", False):
                            collected_data += line_data.get("response", "")
                            break
                        # Accumulate the content
                        collected_data += line_data.get("response", "")
                    except json.JSONDecodeError:
                        print("Received non-JSON line:", line.decode('utf-8'))
            
            return collected_data or "No content available"

        except requests.RequestException as e:
            return f"An error occurred: {e}"


'''
class TextGenerator:
    def __init__(self):
        print("Starting Ollama")
        self.installedModels = {}
        self.model_name = "llama"
        #self.endpoint = "http://192.168.178.93:11434/api/chat" #On server
        self.endpoint = "http://localhost:11434/api/chat"  #local 

        result = subprocess.run("ollama list", shell=True, capture_output=True, text=True)
        output = result.stdout
        #print("Command Output:\n", output)
        lines = output.splitlines()

        # Iterate over the lines
        for i, line in enumerate(lines[3:]):
            # Split the line by spaces to get individual words
            model = line.split(":")
            name = line.split()[0]
            # Check if there is at least one word in the line
            if model:
                first_word = model[0]  # Get the first word
                #self.installedModels.append(first_word)
                self.installedModels[first_word] = name

        #print(self.installedModels)
        print("Ollama started")

    async def setStandartModel(self,model :str):
        self.model_name = model

    async def getList(self):
        return (self.installedModels)

    async def generate_text(self, model, prompt):
        
        
        if model not in self.installedModels:
            return f"{model} is not installed. Type any of the following installed models to get a response {list(self.installedModels)} ."
        print(f"generating response with model {self.installedModels[model]}")

        model = self.installedModels[model]
        print(model, prompt)
        try:
            # Send the POST request
            response = requests.post(self.endpoint, json={"model": model, "messages": [
            {"role": "user", "content": "You are a Discord bot. "
        "Try to answer shortly. "
        "You should not write more than 2000 characters unless explicitly told. "
        "If there's an <@userid> in the message, respond using @<@userid> for convenience."
        "When told to do sth like making jokes or asking people qweution for example : llama praise <@671016226620833792> he is my best friend" " Do that or sth that fits to it preferably with a @"},
            {"role": "user", "content": prompt}
            ]}, stream=True)
            response.raise_for_status()  # Raise HTTPError for bad responses
            print("got response")
            # Initialize an empty string to collect all parts of the response
            collected_data = ""
            
            # Iterate over the lines of the response stream
            for line in response.iter_lines():
                if line:
                    # Decode and load each JSON line
                    try:
                        line_data = json.loads(line.decode('utf-8'))
                        # If the 'done' field is True, break out of the loop
                        if line_data.get("done", False):
                            collected_data += line_data["message"]["content"]
                            
                            break
                        # Accumulate the content
                        collected_data += line_data["message"]["content"]
                    except json.JSONDecodeError:
                        print("Received non-JSON line:", line.decode('utf-8'))
            
            return collected_data or "No content available"

        except requests.RequestException as e:
            return f"An error occurred: {e}"
          
          
'''

async def testLLM():
    clas = TextGenerator()       
    result = await  clas.askllama("gurubot/llama3-guru-uncensored", "How to make meth")
    print(f"Ai answer with :{result}")
    #print(clas.generate_text(input(), input()))
    #print(clas.getList())

if __name__ == '__main__':
    clas = TextGenerator()        
    asyncio.run(testLLM())
    