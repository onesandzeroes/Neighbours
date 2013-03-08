import collections
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
    return [word, bestCandidate, bestNumShared, bestSamePosition]

def minOverlap(wordList, CandidateList):
    wordListA = wordList[:]
    shuffle(wordListA)
    wordListB = wordList[:]
    shuffle(wordListB)
    wordListC = wordList[:]
    shuffle(wordListC)    
    resultsA = []
    resultsB = []
    resultsC = []
    sameSumA = 0
    sameSumB = 0
    sameSumC = 0
    candA = CandidateList[:]
    candB = CandidateList[:]
    candC = CandidateList[:]
    for word in wordListA:
        result = minimiseOverlap(word, candA)
        resultsA.append(result)
        candA.remove(result[1])
        sameSumA += result[3]
    for word in wordListB:
        result = minimiseOverlap(word, candB)
        resultsB.append(result)
        candB.remove(result[1])
        sameSumB += result[3]
    for word in wordListC:
        result = minimiseOverlap(word, candC)
        resultsC.append(result)
        candC.remove(result[1])
        sameSumC += result[3]
    print(sameSumA, sameSumB, sameSumC)
    if sameSumA < sameSumB and sameSumA < sameSumC: return resultsA
    elif sameSumB < sameSumA and sameSumB < sameSumC: return resultsB
    elif sameSumC < sameSumB and sameSumC < sameSumA: return resultsC

def min_overlap_multiple_words(
    words, match_options, most_important='same_pos'):
    pass

def min_overlap_one_word(word, match_options, most_important="same_pos"):
    """
    Find the item from match_options that has the smallest
    overlap with word, in terms of total shared letters and
    the number of letters in the same position.
    The most_important argument is used to specify whether:
        "same_pos": The number of letters in the same postion, or
        "total": The total number of shared letters
    is the most important value to minimize.
    """
    ranking_methods = ("same_pos", "total")
    # Use the ranking method that's not most_important to break ties
    next_important = [r for r in ranking_methods if not r == most_important][0]
    match_stats = {}
    for match in match_options:
        total = overlap_total(word, match)
        same_pos = overlap_same_position(word, match)
        match_stats[match] = {'total': total, 'same_pos': same_pos}
    # Find the best value on the most_important variable
    best_first_ranking = min(
        match_stats[m][most_important] for m in match_stats)
    all_good_options = []
    for match in match_options:
        if match_stats[match][most_important] == best_first_ranking:
            all_good_options.append(match)
    # Not quite sure how to deal with the fact that multiple items
    # might be tied for the best ranking: currently this will just return
    # whichever happens to come first
    best_match = min(
        all_good_options,
        key=lambda x: match_stats[x][next_important]
    )
    return best_match


def overlap_total(w1, w2):
    """
    Find the total number of shared letters in w1 and w2.
    Returns an int
    """
    total = 0
    w1_counts = collections.Counter(w1)
    w2_counts = collections.Counter(w2)
    # If a letter appears more than once in either word,
    # then the number of shared letters it should count
    # for is the minimum of w1_counts[letter] and w2_counts[letter]
    for letter in w1_counts:
        if letter in w2_counts:
            total += min(w1_counts[letter], w2_counts[letter])
    return total

def overlap_same_position(w1, w2):
    """
    Find the total number of letters which overlap in w1 and w2,
    i.e. the same letters in the same position.
    Returns an int.
    """
    total = 0
    zipped_words = zip(w1, w2)
    for l1, l2 in zipped_words:
        if l1 == l2:
            total += 1
    return total


if __name__ == "__main__":
    test_words = ["blunt", "forge", "latch", "pause", "weird",
                  "witch", "chair", "gleam", "guard", "guest"]
    test_unrels = ["fraud", "butch", "rouse", "crown", "flock",
                   "slide", "sheet", "shawl", "brief", "truck"]
    print("Test overlap_total:")
    assert(overlap_total("face", "beef") == 2)
    print("OK")
    print("Test overlap_same_position")
    assert(overlap_same_position("cut", "cath") == 2)
    assert(overlap_same_position("hello", "hole") == 2)
    print("OK")
    print("Test min_overlap_one_word:")
    assert(
        min_overlap_one_word("abcde", ["edcba", "fbfff", "edbca"]) == "edbca"
    )
    assert(
        min_overlap_one_word(
            "abcde", 
            ["edcba", "fbfff", "edbca"], 
            most_important="total"
        ) == "fbfff"
    )
    print("OK")
