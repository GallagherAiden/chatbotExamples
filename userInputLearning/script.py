import json
import random
import string

def updateFile(filename, data):
    stringOfData = json.dumps(data)
    with open(filename, "w") as myfile:
        myfile.write(stringOfData)

def formatInput(userInput):
    # make the input conform to the response file
    userInput = userInput.lower()
    # remove any punctuation
    userInput = userInput.translate(None, string.punctuation)
    return userInput

def addInputAsResponse(chatbotInput, userResponse):
    if chatbotInput == "":
        return
    newInput = {
        "word": userResponse,
        "frequency": 0
    }
    with open('responses.json') as json_file:
        data = json.load(json_file)
        if chatbotInput in data:
            wordCounter = 0
            wordFound = 0
            for thisData in data[chatbotInput]:
                if userResponse == thisData['word']:
                    data[chatbotInput][wordCounter]['frequency'] += 1
                    wordFound = 1
                wordCounter += 1
            if wordFound == 0:
                data[chatbotInput].append(newInput)
        else:
            data[chatbotInput] = []
            data[chatbotInput].append(newInput)
        updateFile("responses.json", data)

def getResponseWithNoData():
    with open('responses.json') as json_file:
        emptyResponses = []
        otherResponses = []
        data = json.load(json_file)
        for thisMatch in data:
            if len(data[thisMatch]) == 0:
                emptyResponses.append(thisMatch)
            else:
                otherResponses.append(thisMatch)
        if len(emptyResponses) > 0:
            selector = random.randint(0, 1)
            if selector == 0:
                randRespNum = random.randint(0, len(emptyResponses)-1)
                return emptyResponses[randRespNum]
            else:
                randRespNum = random.randint(0, len(otherResponses)-1)
                return otherResponses[randRespNum]
        else:
            randRespNum = random.randint(0, len(otherResponses)-1)
            return otherResponses[randRespNum]

def processResponse(thisInput):
    with open('responses.json') as json_file:
        data = json.load(json_file)
        matchFound = 0
        # pattern match the input so exact matches aren't needed
        for thisMatch in data:
            if thisMatch in thisInput:
                if len(data[thisMatch]) > 0:
                    matchFound = 1
                    if len(data[thisMatch]) == 1:
                        return data[thisMatch][0]["word"]
                    else:
                        randRespNum = random.randint(0, len(data[thisMatch])-1)
                        return data[thisMatch][randRespNum]["word"]
        if matchFound == 0:
            # add the input into the responses JSON file with an empty array
            data[thisInput] = []
            updateFile("responses.json", data)
            # ask a random unanswered question from 'responses'
            return getResponseWithNoData()

def processInput(userInput, lastResponse):
    formattedInput = formatInput(userInput)
    addInputAsResponse(lastResponse, formattedInput)
    response = processResponse(formattedInput)
    print("Chatbot: " + response)
    return response

print('Welcome to this chatbot, type something to begin...')
lastResponse = ''
userInput = ''
while userInput != 'bye':
    userInput = raw_input("You: ")
    lastResponse = processInput(userInput, lastResponse)