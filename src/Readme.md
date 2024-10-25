How to start the program:
1. run the server.py file and input a unused port number (the server uses local host for IP by defult)
2. run the client.py file to start a client session, input the port number for the server and follow instruction to start a chat.


extra content:
    How to chat with chatbot:

        Requirements: 
            The following lib are needed to run the chatbot server
                pip install google-generativeai
                pip install python-dotenv

            You need a google gemini API key. You can get it for free here: https://aistudio.google.com/app/apikey
            please save the API key in a .env file in the src dir in the following format: API_KEY = "Your API key"


        To chat with chatbot start the same as the normal chat program but run the chatbot_server.py for server instead.
        when selecting user to chat with, input name chatbot to chat with the chatbot.
