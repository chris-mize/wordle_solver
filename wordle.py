from nltk.corpus import brown
from typing import Set, List, Tuple
import random


def load_five_char_eng_words(char_set: str) -> Set[str]:
    word_list = []
    for word in brown.words():
        if len(word) == 5:
            add = True
            for letter in word:
                if letter not in char_set:
                    add = False
            
            if add:
                word_list.append(word.lower())
    return set(word_list)


def check_valid(guess: str, wordset: Set[str], charset: str) -> bool:
    if len(guess) != 5:
        raise ValueError("Word length must be 5.")
    if bool([True for char in guess if char not in charset]):
        raise TypeError("Only alphabetical characters allowed.")
    if guess not in wordset:
        raise ValueError("Word not found in dictionary")
    if guess in wordset:
        return True


def check_correct(guess: str, answer: str) -> bool:
    return guess.lower() == answer.lower()


def get_letter_freq(char: str, wordset: Set[str]) -> int:
    counts = [word.count(char) for word in wordset]
    return sum(counts)


def get_count_letter_freq(characters_string: str, wordset: Set[str]) -> dict:
    counts_dict = {}
    for letter in characters_string:
        counts_dict[letter] = get_letter_freq(letter, wordset)
    return counts_dict


def get_word_value(word: str, letter_freq_dict: dict) -> int:
    word_val = 0
    for char in set(word):
        word_val += letter_freq_dict[char]
    return word_val


def get_wordset_values(wordset: Set[str], letter_freq_dict: dict) -> list:
    wordset_dict = dict.fromkeys(wordset)
    for word in wordset:
        wordset_dict[word] = get_word_value(word, letter_freq_dict)
    word_vals_list = sorted(wordset_dict.items(), key=lambda x: x[1], reverse=True)
    return word_vals_list


def compare_words(guess: str, answer: str) -> List[Tuple]:
    # Check first for exact positional matches
    guess_list = []
    for index, (guess_char, answer_char) in enumerate(zip(guess, answer)):
        if guess_char == answer_char:
            matchtype = "G"
        elif guess_char != answer_char:
            # Then check whether the guess letter is in the answer
            if guess_char in answer:
                matchtype = "Y"
            else:
                matchtype = "B"
        guess_list.append((guess_char, index, matchtype))
    return guess_list


def get_new_words(wordlist: List[Tuple[str, int]], 
                  compare_list: List[Tuple[str, int, str]]):
    locked_positions = []
    open_positions = []
    for letter_tuple in compare_list:
        letter, index, matchtype = letter_tuple
        if matchtype == 'G':
            locked_positions.append(index)
        else:
            open_positions.append(index)
    
    remove_these = []
    
    for letter_tuple in compare_list:
        letter, index, matchtype = letter_tuple
        if matchtype == 'G':
            for word, value in wordlist:
                if word[index]!=letter:
                    remove_these.append((word, value))

        if matchtype == 'Y':
            for word, value in wordlist:
                other_letters = ''
                for position in open_positions:
                    other_letters+=word[position]
                if letter not in other_letters:
                    remove_these.append((word, value))
                if word[index]==letter:
                    remove_these.append((word, value))

        if matchtype == 'B':
            for word, value in wordlist:
                if word.find(letter)!=-1:
                    remove_these.append((word, value))
 
    for item in list(set(remove_these)):
        wordlist.remove(item)
                    
    return wordlist

def play_inline(override:str):
    characters = "abcdefghijklmnopqrstuvwxyz"
    five_cha_eng_words = load_five_char_eng_words(characters)
    letter_freq_dict = get_count_letter_freq(characters, five_cha_eng_words)
    wordset_vals = get_wordset_values(five_cha_eng_words, letter_freq_dict)

    answer_word = random.choice(list(five_cha_eng_words))
    if override:
        answer_word = override
    print("Answer word: ", answer_word)

    guess_num = 1
    best_guesses_list = wordset_vals
    while guess_num < 7:
        suggested_guess = best_guesses_list[0][0]
        user_guess = suggested_guess
        print(f"Guess {guess_num}: {user_guess}")
        if user_guess == "x":
            break
        try:
            check_valid(user_guess, five_cha_eng_words, characters)
            is_correct = check_correct(user_guess, answer_word)
            if is_correct:
                print(f"Puzzle finished in {guess_num} guesses.")
                break
            else:
                print("Not correct, new guess...")
                comp_list = compare_words(user_guess, answer_word)
                print(comp_list)
                best_guesses_list = get_new_words(best_guesses_list, comp_list)
            guess_num += 1
        except Exception as err:
            print(err)

if __name__ == "__main__":
    characters = "abcdefghijklmnopqrstuvwxyz"
    five_cha_eng_words = load_five_char_eng_words(characters)
    letter_freq_dict = get_count_letter_freq(characters, five_cha_eng_words)
    wordset_vals = get_wordset_values(five_cha_eng_words, letter_freq_dict)
    
    guess_num = 0
    while guess_num < 7:
        print("\nTry:\n", wordset_vals[0:50])
        user_guess = input("Enter your guess. x to exit: ").lower()
        if user_guess == 'x':
            break
        feedback = input("Enter your feedback (B=not in word, G=Exact, Y=Positional):").upper()
        comp_list = []
        for i in range(5):
            comp_list.append((user_guess[i], i, feedback[i]))
        print("Encoded Feedback: ", comp_list)
        wordset_vals = get_new_words(wordset_vals, comp_list)