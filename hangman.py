import os

# global dictionary that holds the picture of the hangman for every state of the game. 
HANGMAN_PHOTOS = {
    0:"""    x-------x""", 
    1:"""    x-------x
    |
    |
    |
    |
    |""", 
    2:"""    x-------x
    |       |
    |       0
    |
    |
    |""", 
    3:"""    x-------x
    |       |
    |       0
    |       |
    |
    |""", 
    4:"""    x-------x
    |       |
    |       0
    |      /|\\
    |
    |""", 
    5:"""    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |""", 
    6:"""    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |"""
}

def show_start_screen():
    """
    function for displaying the starting screen of the game,
    prints the start messege and the game logo

    :return: nothing
    :rtype: None type
    """

    print ("Welcome to the game Hangman.")
    print ("""     _    _                                         
    | |  | |                                        
    | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
    |  __  |/ _` | '_ \\ / _` | '_ ` _ \\ / _` | '_ \\ 
    | |  | | (_| | | | | (_| | | | | | | (_| | | | |
    |_|  |_|\\__,_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_|
                        __/ |                      
                        |___/
        """)

def check_valid_input(letter_guessed: str, old_letters_guessed: list[str]) -> bool:
    """
    checks if the string entered is valid: only one letter from the alphabet and not already guessed
    :param letter_guessed: string to check if valid
    :type letter_guessed: str
    :param old_letters_guessed: list containing all past guesses
    :type old_letters_guessed: list
    :return: boolean that says if the letter is valid
    :rtype: bool
    """
    if len(letter_guessed) == 1 and letter_guessed.isalpha() and letter_guessed.lower() not in old_letters_guessed:
        return True
    return False

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    function that checks if the guessed letter is valid, if it is, it adds it
    to the list containing all past guesses.
    if not it prints X, and all of the passt letters.
    
    :param letter_guessed: string to check if valid
    :type letter_guessed: str
    :param old_letters_guessed: list containing all past guesses
    :type old_letters_guessed: list
    :return: boolean that say if the letter is valid
    :rtype: bool
    """
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        return True
    print("X\n" + "->".join(old_letters_guessed))
    return False

def show_hidden_word(secret_word, old_letters_guessed):
    """
    this function is used to generate the string of the hidden word
    every undiscovered letter will be "_"
    :param secret_word: the word the user needs to find
    :type secret_word: str
    :param old_letters_guessed: list of all the already guessed letters
    :type old_letters_guessed: list
    :return: string that represents the hidden word
    :rtype: str
    """

    result_str = ""
    for chr in secret_word:
        if chr in old_letters_guessed:
            result_str += chr + " "
        else:
            result_str += "_ "
    return result_str

def check_win(secret_word, old_letters_guessed):
    """
    checks if win, all the letters in secret_word are in old_letter_guessed.
    :param secret_word: the word the user needs to find
    :type secret_word: str
    :param old_letters_guessed: list of all the already guessed letters
    :type old_letters_guessed: list
    :return: retuns a boolean that represents if the user won the game
    :rtype: bool
    """
    for chr in secret_word:
        if chr not in old_letters_guessed:
            return False
    return True

def print_hangman(num_of_tries: int):
    """
    prints the correct picture given the number of tries done
    :param num_of_tries: the number of tries left
    :type num_of_tries: int
    :return: nothing
    :rtype: None type
    """
    print(HANGMAN_PHOTOS[num_of_tries])

def choose_word(file_path, index):
    """
    returns the word at the index given from the file given
    :param file_path: path to the file
    :type file_path: str

    :param index: index of the word in the file
    :type index: int

    :return: the word at the index given, from the file given
    :rtype: tuple
    """
    index -= 1
    with open(file_path, "r") as f:
        word_list = f.read().split(" ")
    return word_list[index % len(word_list)]

def main():
    secret_word = ""
    old_letters_guessed = []
    MAX_TRIES = 6
    num_of_tries = 0

    # start of the game! showing the start screen
    show_start_screen()

    # get path to the file containing the words, continue asking for a path if the path entered does not exist
    file_path = input("Enter path to word file: ")
    while not os.path.exists(file_path):
        file_path = input("File not found, enter enother path: ")

    # get an index to choos the word from the file
    word_index = input("Enter number of words to guess: ")
    while not (word_index.isdigit() or (word_index[0] == "-" and word_index[1:].isdigit())):
        word_index = input("Input not valid, Enter number of words to guess: ")
    word_index = int(word_index)

    # get the word from the file
    secret_word = choose_word(file_path, word_index).lower()

    # show the start of the game
    print_hangman(num_of_tries)
    print(show_hidden_word(secret_word, old_letters_guessed))

    # main game loop, continue asking for a letter if not exeded number of tries and not won the game
    while(num_of_tries < MAX_TRIES and not check_win(secret_word, old_letters_guessed)):
        # get letter from user
        letter_guessed = input("Guess a letter: ").lower()
        # if letter is valid add it to the old_letters
        if try_update_letter_guessed(letter_guessed, old_letters_guessed):
            # if letter valid but not correct enlarge the number of tries and print the new state of the game
            if letter_guessed not in secret_word:
                num_of_tries +=1
                print(":(")
                # print the hangman pic
                print_hangman(num_of_tries)
            # show the word with the missing letters as '_'
            print(show_hidden_word(secret_word, old_letters_guessed))
    
    # print a messege corresponding to the game result
    if check_win(secret_word, old_letters_guessed):
        print("WIN")
    else:
        print("LOSE")


if __name__ == "__main__":
    main()
    







