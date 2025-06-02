#!/usr/bin/env python3

import itertools

print('''Enter letters from today's puzzle.
Letters from the same side must be grouped together.
Sides may be entered in any order.''')
input_letters = input("letters> ")

if len(input_letters) != 12:
    print("Expected exactly 12 input letters")
    exit(1)

letter_sides = [input_letters[i:i+3] for i in range(0, 12, 3)]
print(f"Sides: {letter_sides}")

side_indices = {letter:index
                 for index, letters in enumerate(letter_sides)
                 for letter in letters}

def is_valid_word(word):
    # Since the next word begins with the same letter as the current word ends,
    # single letter words are not useful.
    if len(word) <= 1:
        return False
    return is_valid_word_recursive(word, None)

def is_valid_word_recursive(word, prev_side):
    if not word:
        return True
    # This letter must be a different side of the box than the previous letter
    group = side_indices.get(word[0])
    if group is not None and group != prev_side:
        return is_valid_word_recursive(word[1:], group)
    else:
        return False

# Get all words matching is_valid_word()
with open('/etc/dictionaries-common/words', 'r') as f:
    valid_words = [line.strip() for line in f if is_valid_word(line.strip())]

# Group words by first letter
words_by_first_letter = {first_letter:list(words)
    for first_letter, words in itertools.groupby(valid_words, lambda word: word[0])}

# Game wants a solution of five words or less
# Initial "best" solution is a human-readable error message with 6 words
NO_SOLUTION = ['no', 'solutions', 'for', 'these', 'input', 'letters']

def best(a, b):
    '''
    Returns the solution with fewer words.
    If the number of words matches, prefer solutions with fewer total characters.
    '''
    return min(a, b, key=lambda words: (len(words), sum([len(word) for word in words])))

def search_all(valid_words, input_letters):
    return search(
        candidate=[],
        words=valid_words,
        unused_letters=set(input_letters),
        best_solution=NO_SOLUTION,
    )

def search(candidate, words, unused_letters, best_solution):
    if not unused_letters:
        return candidate
    if len(candidate) >= len(best_solution):
        return best_solution
    for word in words:
        new_unused_letters = unused_letters - set(word)
        if len(new_unused_letters) < len(unused_letters):
            best_solution = best(
                search(
                    candidate=candidate + [word],
                    words=words_by_first_letter[word[-1]],
                    unused_letters=new_unused_letters,
                    best_solution=best_solution
                ),
                best_solution
            )
    return best_solution

print(f"Answer: {search_all(valid_words, input_letters)}")
