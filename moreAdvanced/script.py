import json
import random
import string

questions = ["Have you had a good day?", "tell me a little more about you", "where are you from?", "what is your favourite film?"]

def appendToFile(filename, appendText):
    with open(filename, "a") as myfile:
        myfile.write(appendText)

def formatInput(userInput):
    # make the input conform to the response file
    userInput = userInput.lower()
    # remove any punctuation
    userInput = userInput.translate(None, string.punctuation)
    return userInput

def processInput(userInput):
    formattedInput = formatInput(userInput)
    with open('responses.json') as json_file:
        data = json.load(json_file)
        matchFound = 0
        # pattern match the input so exact matches aren't needed
        for thisMatch in data:   
            if thisMatch in formattedInput:
                matchFound = 1
                if len(data[thisMatch]) == 1:
                    print("Chatbot: " + data[thisMatch][0])
                else:
                    randRespNum = random.randint(0, len(data[thisMatch])-1)
                    print("Chatbot: " + data[thisMatch][randRespNum])
        if matchFound == 0:
            # append unanswered input to a file for later modifications
            appendToFile("unansweredInput.txt", userInput)
            # check if its an end of a conversation or a response is expected
            if userInput.endswith('?'):
                print("Chatbot: Sorry, I don't understand")
            else:
                # ask a question to keep conversation going
                randRespNum = random.randint(0, len(questions)-1)
                print("Chatbot: " + questions[randRespNum])


print('Welcome to this chatbot, type something to begin...')
userInput = ''
while userInput != 'bye':
    userInput = raw_input("You: ")
    processInput(userInput)