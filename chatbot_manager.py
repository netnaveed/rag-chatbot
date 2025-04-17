from chatbot import Chatbot

class ChatbotManager:
    def __init__(self):
        self.chatbot = Chatbot()

    def reload_chatbot(self):
        self.chatbot = Chatbot()

    def get_chatbot(self):
        return self.chatbot