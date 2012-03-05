# CELEX.txt structure- word, total F, written F, spoken F
import csv
import string

# In order to check for global variables in the way I've done,
# you need to initialize those variables as "None" first
allTheWords = None
freqDict = None
sylDict = None
regularity = None
neighbourDatabase = None

def celexCheck():
    global allTheWords
    global freqDict
    if not allTheWords:
        allTheWords = loadCELEX()[0] 
        freqDict = loadCELEX()[1] 
    

def loadCELEX(restrictLength=False):
    celexDatabase = open('C:/Python32/Lib/site-packages/Neighbours/CELEX.txt', 
                         'r')
    allTheWords = []
    freqDict = {}
    for letter in string.ascii_lowercase:
        freqDict[letter] = {}
    for line in celexDatabase:
        eachWord = str(line.split()[0]).lower()        
        if restrictLength:
            if len(eachWord) == int(restrictLength):
                allTheWords.append((len(eachWord), eachWord))
                freqDict[eachWord.lower()[0]][eachWord] = float(line.split()[1])
        else:
            allTheWords.append((len(eachWord), eachWord))
            freqDict[eachWord.lower()[0]][eachWord] = float(line.split()[1])
    celexDatabase.close()
    return [allTheWords, freqDict]

def loadPronunciation():
    pron_data = open('C:/Python32/Lib/site-packages/Neighbours/pron.vcb', 'r')
    syllables = {}
    for line in pron_data:
        word = line.split()[0]
        pron = line.split()[1]
        syl = len(pron.split('-'))
        syllables[word] = syl
    return syllables
    

def loadRegularityInfo():
    reg_txt = open('C:/Python32/Lib/site-packages/Neighbours/REG.TXT', 'r')
    regDict = {}
    for line in reg_txt:
        regDict[line.split()[0]] = line.split()[1]
    return regDict


def numSyllables(word):
    global sylDict
    if not sylDict:
        sylDict = loadPronunciation()
    try: 
        return sylDict[word]
    except KeyError:
        return 'Unknown'

def findNeighbours(word, returnList=True):
    global neighbourDatabase
    if not neighbourDatabase:
        neighbourDatabase = {}
    try: 
        result = neighbourDatabase[word]
        return neighbour
    except KeyError:
        celexCheck()   
        neighbours = []
        numNeighbours = 0
        length = len(word)
        for x in allTheWords:
            if length == x[0]:
                diffCount = 0
                for y in range(length):
                    if diffCount == 2: break
                    if not word[y] == x[1][y]:
                        diffCount += 1
                if diffCount == 1:
                    numNeighbours += 1
                    if returnList:
                        neighbours.append(x[1])
        result = (numNeighbours, neighbours)                
        neighbourDatabase[word] = result
        return result
    
def onsetNeighbours(word, returnList=True):
    celexCheck() 
    neighbours = []
    numNeighbours = 0
    length = len(word)
    for x in allTheWords:
        if length == x[0]:
            diffCount = 0
            for y in range(length):
                if diffCount == 2: break
                if not word[y] == x[1][y]:
                    diffCount += 1
            if diffCount == 1:
                if not x[1][0] == word[0]:
                    numNeighbours += 1
                    if returnList:
                        neighbours.append(x[1])
    return (numNeighbours, neighbours)

def sharedNeighbours(word1, word2):
    word1 = str(word1)
    word2 = str(word2)
    word1N = findNeighbours(word1)[1]
    word2N = findNeighbours(word2)[1]
    shared = list(set(word1N) & set(word2N))
    #print("Number of shared neighbours: ",len(shared))
    return (len(shared),shared)

def getFrequency(word):
    celexCheck()
    return freqDict[word[0]][word]

def sharedBodies(body):
    celexCheck()
    shared = []
    bodyLength = len(body)
    for word in allTheWords:
        if word[1][-len(body):] == body:
            shared.append(word[1])
    return shared

def isRegular(word):
    global regularity
    if not regularity:
        regularity = loadRegularityInfo()
    try: regularity[word]
    except KeyError: return False
    if regularity[word] == '1':
        return True
    else: return False

def neighbourLocations(word):
    neighbours = findNeighbours(word)[1]
    nPositions = {}
    for x in range(len(word)):
        nPositions[str(x + 1)] = []
        for each in neighbours:
            if not word[x] == each[x]:
                nPositions[str(x + 1)].append(each)
        if len(nPositions[str(x +1 )]) == 0:
            nPositions[str(x + 1)] = None
    return nPositions

def swap(x, i, j):
    x = list(x)
    x[i], x[j] = x[j], x[i]
    return ''.join(x)
    
def transNeighbours(word):
    celexCheck() 
    tNeighbs = []
    for x in range(len(word) - 1):
        swapped = swap(word, x, x + 1)
        if swapped in freqDict[swapped[0]].keys():    
            tNeighbs.append(swapped)
    return tNeighbs