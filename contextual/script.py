import json
import random
import string
from difflib import SequenceMatcher

questions = ["Have you had a good day $name", "how is the weather in $location", "does it feel good to be $age"]

def appendToFile(filename, appendText):
    with open(filename, "a") as myfile:
        myfile.write(appendText)

def updateFile(filename, data):
    stringOfData = json.dumps(data)
    with open(filename, "w") as myfile:
        myfile.write(stringOfData) 

def updateUserContext(thisContext, value):
    with open('userContext.json') as json_file:
        data = json.load(json_file)
        data[thisContext] = value
        return data

def formatInput(userInput):
    # make the input conform to the response file
    userInput = userInput.lower()
    # remove any punctuation
    userInput = userInput.translate(None, string.punctuation)
    return userInput

def checkResponse(inputResponse):
    # see if there are any context pointers that need replacing
    if '$' in inputResponse:
        contextType = inputResponse.split("$")[1] 
        with open('userContext.json') as json_file:
            data = json.load(json_file)
            contextText = data[contextType]
            if contextText == "":
                if contextType == "name":
                    newResponse = "Chatbot: what is your name?"
                elif contextType == "location":
                    newResponse = "Chatbot: where abouts are you from?"
                elif contextType == "age":
                    newResponse = "Chatbot: I don't mean to be rude, but how old are you?"
            else:
                newResponse = inputResponse.split("$")[0] + contextText
            return newResponse
    else:
        return inputResponse

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def checkForLocation(inputWords):
    with open('locations.json') as json_file:
        data = json.load(json_file)
        mostSimilar = {
            "place": "",
            "inputWord": "",
            "similarity": 0
        }
        # match the input words, for words stored in the location file
        # this gives us the most probable 
        for thisWord in inputWords:
            for thisLocation in data['place']:
                thisSimilarity = similar(thisWord, thisLocation)
                if thisSimilarity > mostSimilar['similarity']:
                    mostSimilar['place'] = thisLocation
                    mostSimilar['inputWord'] = thisWord
                    mostSimilar['similarity'] = thisSimilarity
        if mostSimilar['similarity'] > 0.79:
            return mostSimilar['place']
        elif mostSimilar['similarity'] > 0.5: 
            return mostSimilar['inputWord']
        else:
            return ""

def checkForUserContext(userInput):
    with open('inputMatches.json') as json_file:  
        data = json.load(json_file)
        for thisMatch in data:
            if thisMatch in userInput:
                inputWords = userInput.split(" ")
                if data[thisMatch] == "name":
                    # uses the last word of the input as the name. 
                    # This could be more sophisticated. i.e. pattern matching against known names
                    newJSON = updateUserContext("name", inputWords[len(inputWords)-1])
                    updateFile("userContext.json", newJSON)
                elif data[thisMatch] == "location":
                    # check against the location file
                    location = checkForLocation(inputWords)
                    if location != "":
                        newJSON = updateUserContext("location", location)
                        updateFile("userContext.json", newJSON)
                elif data[thisMatch] == "age":
                    # get a string with a number in it (written as a number or text)
                    nums = [int(word) for word in inputWords if word.isdigit()]
                    if len(nums) == 1:
                        newJSON = updateUserContext("age", str(nums[0]))
                        updateFile("userContext.json", newJSON)

def processInput(userInput):
    formattedInput = formatInput(userInput)
    checkForUserContext(formattedInput)
    with open('responses.json') as json_file:
        data = json.load(json_file)
        matchFound = 0
        # pattern match the input so exact matches aren't needed
        for thisMatch in data:   
            if thisMatch in formattedInput:
                matchFound = 1
                # make a response variable to check for context
                if len(data[thisMatch]) == 1:
                    response = "Chatbot: " + data[thisMatch][0]
                else:
                    randRespNum = random.randint(0, len(data[thisMatch])-1)
                    response = "Chatbot: " + data[thisMatch][randRespNum]
        if matchFound == 0:
            # append unanswered input to a file for later modifications
            appendToFile("unansweredInput.txt", userInput)
            # check if its an end of a conversation or a response is expected
            if userInput.endswith('?'):
                response = "Chatbot: Sorry, I don't understand"
            else:
                # ask a question to keep conversation going
                randRespNum = random.randint(0, len(questions)-1)
                response = "Chatbot: " + questions[randRespNum]
        # check if anything needs to happen to the response
        response = checkResponse(response)
        print(response)


print('Welcome to this chatbot, type something to begin...')
userInput = ''
while userInput != 'bye':
    userInput = raw_input("You: ")
    processInput(userInput)