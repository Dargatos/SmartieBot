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
        


    async def chatOllama(self,model,prompt, contx:str):
        template = (
            "You are a Discord bot named Smartie"
        ).format(contx=contx, Message=prompt)
        headers = {
            "Content-Type": "application/json"
        }

        user = {"The Users name is Mio"}
        data = [
            {
                'role': 'system',
                'content': 'You are DiscordBot named Smartie.'
                'Provide short answers.'
                'Since you are sending messages into a discord channel and can so ping certain members<@userid> or even <@everyone> so use that functionallity but not abusivley'
                'tagging(@) only work like that <@userid>'
                'You are supposed  to assist the user of the Discord Server but also act like a friend make jokes be funny just remeber to keep it light'
                'Try <@userid> but not abuse it only if it fits to context'
                f'Context about the Discord user who sent the request/message {contx}'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]

        response = self.ollama.chat(
            model = model,
            messages=data,
        )

        return response

    async def askllama(self, model, prompt,usercontx:str = "Discord username Dargatos Discord user id 124151234"):
        #Checks if given model is installed 
        if model not in self.installedModels:
            return f"{model} is not installed. Type any of the following installed models to get a response {list(self.installedModels)} ."
        print(f"generating response with model {self.installedModels[model]}")

        # Since installed models are stored wierdly it needs to extract the real name of it other wiser idk
        model = self.installedModels[model]

        print(f"Sending to {model} with prompt {prompt}")
        try:
            # Send the POST request
            response = await self.chatOllama(model ,prompt, usercontx)
            print(response)
            print("got response")

            
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, 'data.json')
            with open(file_path, 'w') as file:
                json.dump(response, file, indent=4)
            print(f"Data saved to {file_path}")
            
            # Initialize an empty string to collect all parts of the response
            collected_data = ""
            finalresponse = response["message"]["content"]
            return finalresponse
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
    result = await  clas.api_generate("llama", "Hi What color is the sky in the evening also pls @ me so i get pinged")
    print(f"Ai answer with :{result}")
    #print(clas.generate_text(input(), input()))
    #print(clas.getList())

if __name__ == '__main__':
    clas = TextGenerator()        
    asyncio.run(testLLM())
    