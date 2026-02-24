'''
    Created By : Christian Merriman
    Date : 2/2026

    Purpose : To save json data for our server
'''
import json
import os

class SentinelAI:
    def __init__(self, history_file="chat_history.json"):
        self.history_file = history_file

    def save_chat(self, chat_history):
        """Saves the current chat list to a JSON file."""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(chat_history, f, indent=4)
            return True
        except Exception as e:
            print(f"Failed to save history: {e}")
            return False

    def load_chat(self):
        """Loads chat history from the JSON file. Returns empty list if not found."""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load history: {e}")
                return []
        return []