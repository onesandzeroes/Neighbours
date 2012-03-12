# CELEX.txt structure- word, total F, written F, spoken F
import csv
import string
import os

# In order to check for global variables in the way I've done,
# you need to initialize those variables as "None" first
allTheWords = None
sylDict = None
regularity = None
neighbourDatabase = None

def subtlexCheck():
    if not allTheWords:
        loadSUBTLEX()


def loadSUBTLEX(restrictLength=False):
    ''' Loads the list of words and frequency information from 
    SUBTLEXonlyfrequency.csv.
    restrictLength is an optional argument. Passing a number will load
    only words of that length. \n
    All functions that rely on this data currently check if it's loaded
    and load it if necessary, but if you want to use the restrictLength
    argument, you have to do it yourself, e.g. \n
    allTheWords = loadSUBTLEX(restrictLength=5)[0] \n
    freqDict = loadSUBTLEX(restrictLength=5)[0]'''
    global allTheWords
    global freqDict
    subtlexDatabase = open(os.path.dirname(__file__) +
                           '/SUBTLEXonlyfrequency.csv', 
                           'r')
    subtlexCSV = csv.reader(subtlexDatabase, dialect='excel')
    next(subtlexCSV)
    wordList = []
    frequencies = dict.fromkeys(string.ascii_lowercase, {})
    for line in subtlexCSV:
        eachWord = line[0].lower()
        if restrictLength:
            if len(eachWord) == int(restrictLength):
                wordList.append((len(eachWord), eachWord))
                frequencies[eachWord[0]][eachWord] = float(line[1])
        else:
            wordList.append((len(eachWord), eachWord))
            frequencies[eachWord[0]][eachWord] = float(line[1])
    subtlexDatabase.close()
    allTheWords = wordList
    freqDict = frequencies

def loadPronunciation():
    ''' Loads the pronunciation data from pron.vcb. At this point, it only '''
    '''grabs the number of syllables'''
    pron_data = open('C:/Python32/Lib/site-packages/Neighbours/pron.vcb', 'r')
    syllables = {}
    for line in pron_data:
        word = line.split()[0]
        pron = line.split()[1]
        syl = len(pron.split('-'))
        syllables[word] = syl
    return syllables
    

def loadRegularityInfo():
    ''' Loads the regularity info from REG.TXT'''
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
        return result
    except KeyError:
        subtlexCheck()
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
    subtlexCheck() 
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
    subtlexCheck()
    return freqDict[word[0]][word]

def sharedBodies(body):
    subtlexCheck()
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
    subtlexCheck() 
    tNeighbs = []
    for x in range(len(word) - 1):
        swapped = swap(word, x, x + 1)
        if swapped in freqDict[swapped[0]].keys():
            tNeighbs.append(swapped)
    return tNeighbs

    
def minimiseOverlap(word, candidates):
    ''' Takes a word and a list of prime words, and finds the candidate with'''
    ''' the lowest overlap. Returns list containing: \n '''
    ''' 0: the word with lowest overlap \n'''
    ''' 1: the number of shared letters '''
    ''' 2: the number of shared letters in the same position'''
    # Note: might not be working properly for words with repeated letters
    # because I've used sets
    wordLetters = list(word)
    bestCandidate = None
    bestNumShared = len(word)
    bestSamePosition = len(word)
    for cand in candidates:
        candidateLetters = list(cand)
        sharedLetters = set(wordLetters) & set(candidateLetters)
        if len(sharedLetters) < bestNumShared:
            bestCandidate = cand
            bestNumShared = len(sharedLetters)
            samePosition = len(sharedLetters)
            for shared in sharedLetters:
                if not word.find(shared) == cand.find(shared):
                    samePosition -= 1
            bestSamePosition = samePosition
        elif len(sharedLetters) == bestNumShared:
            samePosition = len(sharedLetters)
            for shared in sharedLetters:
                if not word.find(shared) == cand.find(shared):
                    samePosition -= 1
            if samePosition < bestSamePosition:
                bestSamePosition = samePosition
                bestCandidate = cand
    return [bestCandidate, bestNumShared, bestSamePosition]

