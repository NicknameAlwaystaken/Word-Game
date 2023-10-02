import string
import time
import json
import random

def check_solution(answer, guessed_letters):
    solution = ""
    for letter in answer:
        if letter.upper() in guessed_letters:
            solution += letter
        else:
            solution += "_"

    return solution

def new_game(new_word):
    answer = new_word
    guessed_letters = []
    wrong_guess_amount = 0
    max_wrong_guesses = 5
    print()
    print("Here is a new word!")
    while wrong_guess_amount < max_wrong_guesses:
        print()
        print()
        empty_string = ""
        print(f"You have {max_wrong_guesses -  wrong_guess_amount} wrong guesses left! Guessed characters: {empty_string.join(guessed_letters)}")
        solution = check_solution(answer, guessed_letters)
        print(solution)
        if(solution == answer):
            print("You got it. Well done!")
            return

        print()
        letter_guessed = input("Give a new character: ").upper()

        if letter_guessed == "":
            continue

        if len(letter_guessed) >= 2:
            print("Too many characters!")
            continue

        if letter_guessed not in string.ascii_uppercase:
            print(f"'{letter_guessed}' is not part of valid characters!")
            continue

        if letter_guessed in guessed_letters:
            print(f"You already guessed character '{letter_guessed}'")
            continue

        guessed_letters.append(letter_guessed)
        if letter_guessed not in answer.upper():
            wrong_guess_amount += 1
            print("Wrong.")
            if(wrong_guess_amount == max_wrong_guesses):
                print("Too many wrong guesses!")
        else:
            print("Correct.")

list_of_answers = []

with open("answer_list.json", "r") as openfile:
    json_object = json.load(openfile)
    print(json_object)
    print(type(json_object))
    for key in json_object:
        print(json_object[key]["answer"])
        list_of_answers.append(json_object[key]["answer"])


list_of_answers = ["televisio", "KaHvIMuKi", "HashTag", "Mediocre", "WalaWoloWingWangWong"]

random.seed()

while True:
    index = random.randrange(0, len(list_of_answers) - 1)
    new_game(list_of_answers[index])
