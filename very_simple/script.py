import json
import random

def processInput(text):
    with open('responses.json') as json_file:
        data = json.load(json_file)
        if data.get(text) == None:
            print("Chatbot: Sorry, I don't understand")
        elif len(data[text]) == 1:
            print(data[text][0])
        else:
            randRespNum = random.randint(0, len(data[text])-1)
            print("Chatbot: " + data[text][randRespNum])

print('Welcome to this chatbot, type something to begin...')
text = ''
while text != 'bye':
    text = raw_input("You: ")
    processInput(text)