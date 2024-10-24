import google.generativeai as genai
import os
from dotenv import load_dotenv

class chatbot:
    def __init__(self):
        load_dotenv()
        genai.configure(api_key=os.environ["API_KEY"])
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        start_prompt = "You are a chatbot to have a conversation with. Please have a conversation with me."
        self.chat_session = self.model.start_chat()
        self.chat_session.send_message(start_prompt)
    
    def get_response(self, message):
        response = self.chat_session.send_message(message)
        return response.text