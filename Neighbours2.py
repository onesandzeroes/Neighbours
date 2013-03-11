#! /usr/bin/env python3
import collections
import random


def min_overlap_multiple_words(words,
                               match_options,
                               most_important='same_position',
                               iterations=10):
    """
    Takes a list of words and a list of options to be matched up to them,
    so that each word has the minimum amount of overlap with its match.
    The algorithm used is fairly simple- it just shuffles both lists and
    then looks for the best match for each word in the shuffled list. Since
    the good matches will probably tend to get used up by the end of the list,
    the matching isn't always great- to minimize this problem, the process is
    iterated and the matches with the lowest overall overlap are returned.

    Returns a dictionary mapping from each word in words to its matched word
    """
    best_match_stat = None
    best_matches = None
    for i in range(iterations):
        current_matches = {}
        current_stat = 0
        shuffled_options = match_options[:]
        random.shuffle(shuffled_options)
        # Need to shuffle the words so that the first word in the
        # list doesn't always get the ideal matches, and the last
        # word the leftovers
        shuffled_words = words[:]
        random.shuffle(shuffled_words)
        for word in shuffled_words:
            match = min_overlap_one_word(
                word, shuffled_options, most_important)
            current_matches[word] = match
            shuffled_options.remove(match)
            current_stat += overlap(word, match, method=most_important)
        # On the first iteration, the current set of matches will
        # always be the best
        if best_match_stat is None:
            best_match_stat = current_stat
            best_matches = current_matches
        else:
            if current_stat < best_match_stat:
                best_match_stat = current_stat
                best_matches = current_matches
    return best_matches


def min_overlap_one_word(word, match_options, most_important="same_position"):
    """
    Find the item from match_options that has the smallest
    overlap with word, in terms of total shared letters and
    the number of letters in the same position.
    The most_important argument is used to specify whether:
        "same_position": The number of letters in the same postion, or
        "total": The total number of shared letters
    is the most important value to minimize.
    """
    # Use the ranking method that's not most_important to break ties
    other_method = {"same_position": "total", "total": "same_position"}
    next_important = other_method[most_important]
    match_stats = {}
    for match in match_options:
        match_stats[match] = {
            'total': overlap(word, match, "total"),
            'same_position': overlap(word, match, "same_position")
        }
    # Find the best value on the most_important variable
    best_first_ranking = min(
        match_stats[m][most_important] for m in match_stats)
    # Find all the match options that take that value
    all_good_options = []
    for match in match_options:
        if match_stats[match][most_important] == best_first_ranking:
            all_good_options.append(match)
    # Break ties using the next most important overlap measure
    # Not quite sure how to deal with the fact that multiple items
    # might be tied for the best ranking: currently this will just return
    # whichever happens to come first
    best_match = min(
        all_good_options,
        key=lambda x: match_stats[x][next_important]
    )
    return best_match


def overlap(w1, w2, method='same_position'):
    """
    Convenience function to make it easy to call either overlap_total
    or overlap_same_position by passing either "same_position" or
    "total" as the method.
    The individual functions can still be used directly, this
    just makes it easier to call them in code that might use one or the
    other at different times
    """
    if method == 'same_position':
        return overlap_same_position(w1, w2)
    elif method == 'total':
        return overlap_total(w1, w2)


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
    print("Test min_overlap_multiple_words:")
    test_words = ["abcde", "fghij", "klmno"]
    test_matches = ["bfzzz", "glzzz", "dmzzz"]
    assert(
        min_overlap_multiple_words(test_words, test_matches, "total") == {
            "abcde": "glzzz",
            "fghij": "dmzzz",
            "klmno": "bfzzz"
        }
    )
    print("OK")
