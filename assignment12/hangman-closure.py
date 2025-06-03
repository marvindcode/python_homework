def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter)
        guess_word = "".join([c if c in guesses else "_" for c in secret_word])
        print(guess_word)
        return set(secret_word).issubset(guesses)
    
    return hangman_closure

if __name__ == "__main__":
    secret = input("secret word: ").lower()
    hangman = make_hangman(secret)

    while True:
        guess = input("Enter a letter: ").lower()
        if hangman(guess):
            print("You did it! Play again")
            break
