'''
    Created By : Christian Merriman

    Updated : 2/2026

    Purpose : To connect to local Ollama server, to use LLM.
'''
import requests

#stores local models to use
ollama_crew = "ollama/llama3.1:8b"
ollama_normal = "llama3.1:8b"
gemma = "gemma3:12b"
deepseek_uncensored_crew = "ollama/huihui_ai/deepseek-r1-abliterated:14b"
deepseek_uncensored_normal = "huihui_ai/deepseek-r1-abliterated:14b"
gpt_local = "gpt-oss:20b"

model_used_crew = ollama_crew
model_used_normal = ollama_normal

import random

class Ask_Model():
    def __init__(self):
        pass

    def close_model(self):
        response = Ask_Model().ask_model("hi", keep_alive=0)

    def ask_model_with_chat_history(self, prompt, chat_history, temperature=0.8, keep_alive = 0, system_instructions = ""):

        if not chat_history:
            chat_history.append({"role": "system", "content": system_instructions})

        # 1. Add the newest message to our 'long term' history
        chat_history.append({"role": "user", "content": prompt})

        # 2. CREATE A SLICE (The 'Short Term' Memory)
        # We always keep the first message (The System Instructions)
        # Plus the last 6 messages (3 questions, 3 answers)
        context_window = [chat_history[0]] + chat_history[-6:]

        # 3. Setup data and send to local LLM
        url = "http://localhost:11434/api/chat"
        data = {
            "model": ollama_normal,
            "messages": context_window,
            "stream": False,
            "keep_alive" : keep_alive,
            #"options": {
            #    "temperature": temperature  # Added this so your variable actually gets used!
            #}
        }

        try:
            response = requests.post(url, json=data)
            ai_reply = response.json()['message']['content']
        except Exception as e:
            ai_reply = f"Error: {str(e)}"

        # 4. Add to the list
        chat_history.append({"role": "assistant", "content": ai_reply})

        #return response and the chat history
        return ai_reply, chat_history

    def ask_model(self, prompt, temperature=0.8, keep_alive = 0, system_instructions = ""):

        # Set your preferred values for the randomness
        random_temperature = 1.15
        random_top_k = 0
        random_top_p = 0.95
        random_repeat_penalty = 1.15

        # 1. Generate a large, random integer for the seed
        # Using a 64-bit integer range (up to 2^64) is usually safe for LLM seeds
        random_seed = random.randint(1, 18446744073709551615)

        url = "http://localhost:11434/api/generate"
        data = {
            "model": ollama_normal,
            "prompt": prompt,
            "system" : system_instructions,
            "stream": False,
            "keep_alive" : keep_alive,
            #// --- CORRECTED SECTION: ALL SAMPLING PARAMETERS ARE INSIDE 'options' ---
            "options": {
                #// NOTE: temperature should also be nested for maximum compatibility
                "temperature": random_temperature, 
                "seed" : random_seed,
                #"top_k": random_top_k, 
                #"top_p": random_top_p,
                "repeat_penalty": random_repeat_penalty 
            }
        }

        response = requests.post(url, json=data)

        #self.unload_model()

        return response.json()['response']
    

    def ask_model1(self, prompt, temperature=0.8, keep_alive = 0):

        # Set your preferred values for the randomness
        random_temperature = 1.15
        random_top_k = 0
        random_top_p = 0.95
        random_repeat_penalty = 1.15

        # 1. Generate a large, random integer for the seed
        # Using a 64-bit integer range (up to 2^64) is usually safe for LLM seeds
        random_seed = random.randint(1, 18446744073709551615)

        url = "http://localhost:11434/api/generate"
        data = {
            "model": ollama_normal, # "llama3.1:8b",
            "prompt": prompt,
            "stream": False,
            "temperature": temperature,
            "seed" : random_seed,
            "top_k": random_top_k, 
            "top_p": random_top_p,
            "repeat_penalty": random_repeat_penalty,
            "keep_alive" : keep_alive, #    "keep_alive": "0"  # Ensures the model is unloaded immediately after the response
            # --- ADDED SECTION FOR VRAM CLEARING ---
  
        }

        response = requests.post(url, json=data)

        #self.unload_model()

        return response.json()['response']
    
    def unload_model(self):
        url = f"""http://localhost:11434/api/generate -d '{{"{ollama_normal}": "MODELNAME", "keep_alive": 0}}'"""

        response = requests.post(url)

    

    def ask_model_GPT(self, prompt):

        url = "http://localhost:11434/api/generate"
        data = {
            "model": gpt_local, # 
            "messages": [
                {
                    "role": "user",
                    "content": (
                        {prompt}
                    ),
                },
            ],
            # Tell the model to produce a JSON object
            "response_format": {"type": "json_object"},
        }

        response = requests.post(url, json=data)
        return response.json()['response']