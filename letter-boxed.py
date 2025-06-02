#!/usr/bin/env python3

import itertools

print("Enter letters from today's puzzle.")
print("Letters from the same side must be grouped together.")
print("Sides may be entered in any order")
input_letters = input("letters> ")

if len(input_letters) != 12:
    print("Expected exactly 12 input letters")
    exit(1)

letter_groups = [input_letters[i:i+3] for i in range(0, 12, 3)]
print(f"Sides: {letter_groups}")

group_indices = {letter:index
                 for index, letters in enumerate(letter_groups)
                 for letter in letters}

def is_valid_word(word):
    if len(word) <= 1:
        return False
    group = group_indices.get(word[0])
    if group is not None:
        return is_valid_word_internal(word[1:], group)
    else:
        return False

def is_valid_word_internal(word, prev_group):
    if not word:
        return True
    group = group_indices.get(word[0])
    if group is not None and group != prev_group:
        return is_valid_word_internal(word[1:], group)
    else:
        return False

with open('/etc/dictionaries-common/words', 'r') as f:
    words = [line.strip() for line in f if is_valid_word(line.strip())]

words_by_first_letter = {first_letter:list(words)
    for first_letter, words in itertools.groupby(words, lambda word: word[0])}

NO_SOLUTION = ['no', 'solutions', 'for', 'these', 'input', 'letters']

def shortest(a, b):
    if len(a) < len(b):
        return a
    else:
        return b

def search_all():
    unused_letters = set(input_letters)
    best_solution = NO_SOLUTION
    for word in words:
        best_solution = shortest(
            search([word], unused_letters - set(word), best_solution),
            best_solution
        )
    return best_solution

def search(solution, unused_letters, best_solution):
    if not unused_letters:
        return solution
    if len(solution) >= len(best_solution):
        return best_solution
    last_letter_prev_word = solution[-1][-1]
    for word in words_by_first_letter[last_letter_prev_word]:
        new_unused_letters = unused_letters - set(word)
        if len(new_unused_letters) < len(unused_letters):
            best_solution = shortest(
                search(solution + [word], new_unused_letters, best_solution),
                best_solution
            )
    return best_solution

print(f"Answer: {search_all()}")
