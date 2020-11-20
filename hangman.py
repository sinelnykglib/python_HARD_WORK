import random
import string

WORDLIST_FILENAME = "words.txt"
VOWELS = {"a", "e", "o", "i", "u"}
HINTS = "*"
UNKNOWN_LETTER = "_"


def load_words():
    """
        Returns a list of valid words. Words are strings of lowercase letters.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def choose_word(wordlist):
    """
        wordlist (list): list of words (strings)

        Returns a word from wordlist at random
    """
    return random.choice(wordlist)


wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
        secret_word: string, the word the user is guessing; assumes all letters are
          lowercase
        letters_guessed: list (of letters), which letters have been guessed so far;
          assumes that all letters are lowercase
        returns: boolean, True if all the letters of secret_word are in letters_guessed;
          False otherwise
    '''
    for i in range(len(secret_word)):
        if secret_word[i] not in letters_guessed:
            return False
    return True


def letter_error(warnings, attemps, letters_guessed):
    '''
    Letter_error: checks the input of letters and takes away attempts in case of entering not a letter or one that was
        already before
    warnings: have static number
    attemps: variables whose have static number
    returns: the number of these values
    '''
    # Make message about warnings when user use non letter or letter have been used early
    if warnings > 0:
        warnings -= 1
        print("Oops! That is not a valid letter. You have", warnings, "warnings left")
    else:
        attemps -= 1
        print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:",
              get_guessed_word(secret_word, letters_guessed))
    return warnings, attemps


def check_let(attemps, letter, letters_guessed):
    '''
    check_vowels_let: checks for the content of the vowel in the word
        if the letter is correctly guessed the issuance of the word with it
    attemps: variables whose have static number
    letter: the letter entered by the player
    returns: number of attemps and letter entered by the player
    '''
    # check letters in word
    splited_word = get_guessed_word(secret_word, letters_guessed)
    if letter not in secret_word:
        print('Oops! That letter is not in my word:', splited_word)
        # If letters was vowels remove 2 attemps, if not remove 1 attemps
        if letter in VOWELS:
            attemps -= 1
        attemps -= 1
    else:
        print('Good guess:', splited_word)
    return attemps, letter, letters_guessed


def get_guessed_word(secret_word, letters_guessed):
    '''
        secret_word: string, the word the user is guessing
        letters_guessed: list (of letters), which letters have been guessed so far
        returns: string, comprised of letters, underscores (_), and spaces that represents
          which letters in secret_word have been guessed so far.
    '''
    splited_word = list(secret_word)
    # Make from word string what consist lower space(UNKNOWN_LETTER)
    for i in range(len(secret_word)):
        if secret_word[i] not in letters_guessed:
            splited_word[i] = UNKNOWN_LETTER + " "
    return "".join(splited_word)


def get_available_letters(letters_guessed):
    '''
        letters_guessed: list (of letters), which letters have been guessed so far
        returns: string (of letters), comprised of letters that represents which letters have not
          yet been guessed.
    '''
    avaible_letters = string.ascii_lowercase
    # Find letters have been entered and deleted him from available_letters
    alphabet = filter(lambda letter: letter not in letters_guessed, string.ascii_lowercase)
    return ''.join(alphabet)


def hangman(secret_word, hints_enabled):
    '''
        secret_word: string, the secret word to guess.

        Starts up an interactive game of Hangman.
    '''
    # constant numbers
    warnings = 3
    attemps = 6
    letters_guessed = set()
    # Message with first information and input letters
    print(f'I am thinking of a word that is {len(secret_word)} letters long')
    print(f'Your have {warnings} warnings')
    while attemps > 0 and not is_word_guessed(secret_word, letters_guessed):
        print("-" * 13)
        print(f'You have  {attemps} guesses left.')
        print("Available letters: ", get_available_letters(letters_guessed))
        letter = input("enter letter: ").strip(' ').lower()
        # Check letters and make a solve right letter or not
        if hints_enabled and letter == HINTS:
            show_possible_matches(get_guessed_word(secret_word, letters_guessed).replace(" ", ""))
        elif not letter.isalpha() or letter in letters_guessed:
            warnings, attemps = letter_error(warnings, attemps, letters_guessed)
        else:
            letters_guessed.add(letter)
            attemps, letter, letters_guessed = check_let(attemps, letter, letters_guessed)
    if attemps <= 0:
        print(f'Sorry, you ran out of guesses. The word was {secret_word}')
    # Message about win and score
    else:
        points = int(attemps) * len(set(secret_word))
        print("Congratulations, you won! \nYour total score for this game is:", points)


def match_with_gaps(my_word, other_word):
    '''
        my_word: string with _ characters, current guess of secret word
        other_word: string, regular English word
        returns: boolean, True if all the actual letters of my_word match the
            corresponding letters of other_word, or the letter is the special symbol
            _ , and my_word and other_word are of the same length;
            False otherwise:
    '''
    # At first we go through my_word
    # After we are looking for lower space and check on letters which are already entered
    # And whether they are in our word we return value of function
    if len(my_word) == len(other_word):
        my_word_set = set(my_word)

        for i in range(len(my_word)):
            if my_word[i] == UNKNOWN_LETTER:
                if other_word[i] in my_word_set:
                    return False
            elif my_word[i] != other_word[i]:
                return False
        return True
    return False


def show_possible_matches(my_word):
    '''
        my_word: string with _ characters, current guess of secret word
        returns: nothing, but should print out every word in wordlist that matches my_word
    '''
    words = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            words.append(word)
    if len(words) == 0:
        print("No matches found!")
    else:
        print(*words)


if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman(secret_word, hints_enabled = HINTS)
