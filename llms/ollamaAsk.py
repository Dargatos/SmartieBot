import requests
import json
import subprocess


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

    def setStandartModel(self,model :str):
        self.model_name = model

    def getList(self):
        return (self.installedModels)

    def generate_text(self, model, prompt):
        
        
        if model not in self.installedModels:
            return f"{model} is not installed. Type any of the following installed models to get a response {list(self.installedModels)} ."
        print(f"generating response with model {self.installedModels[model]}")

        model = self.installedModels[model]
        print(model, prompt)
        try:
            # Send the POST request
            response = requests.post(self.endpoint, json={"model": model, "messages": [{"role": "user", "content": prompt}]}, stream=False)
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
          
          


if __name__ == '__main__':
    clas = TextGenerator()        
    print(clas.generate_text("zephyr", "Tree ?"))
    #print(clas.generate_text(input(), input()))
    print(clas.getList())
