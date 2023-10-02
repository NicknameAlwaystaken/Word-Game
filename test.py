# Simple pygame program


# Import and initialize the pygame library

import pygame
import pygame.freetype  # Import the freetype module.
import string
import random


pygame.init()
INIT_SCREEN_WIDTH = 800
INIT_SCREEN_HEIGHT = 600

RED_COLOR = (200, 50, 25)
GREEN_COLOR = (50, 200, 25)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

GUESS_FONT = pygame.freetype.Font("YoungSerif-Regular.ttf", 30)
SOLUTION_FONT = pygame.freetype.Font("YoungSerif-Regular.ttf", 40)
EVENT_FONT = pygame.freetype.Font("YoungSerif-Regular.ttf", 20)
BUTTON_FONT = pygame.freetype.Font("YoungSerif-Regular.ttf", 50)
GUESSES_LEFT_FONT = pygame.freetype.Font("YoungSerif-Regular.ttf", 20)

screen = pygame.display.set_mode((INIT_SCREEN_WIDTH, INIT_SCREEN_HEIGHT), pygame.RESIZABLE)
screen_size_x, screen_size_y = screen.get_size()


answer = ""
guessed_letters = []
letter_buttons = []
solution_text = len(answer) * "_"
event_text = ""
event_text_surface, event_text_rect = EVENT_FONT.render(event_text, BLACK_COLOR)
wrong_guess_amount = 0
max_wrong_guesses = 5
guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."
random.seed()

def get_new_word():
    list_of_answers = ["televisio"]
    #random_int = random.randrange(0, len(list_of_answers) - 1)
    random_int = 0
    return list_of_answers[random_int]

def reset_game():
    global answer, guessed_letters, solution_text, event_text, wrong_guess_amount, max_wrong_guesses, letter_buttons
    answer = get_new_word()
    guessed_letters = []
    solution_text = len(answer) * "_"
    event_text = ""
    wrong_guess_amount = 0
    max_wrong_guesses = 5
    setup_buttons()
    update_solution()

def is_solved():
    if(solution_text == answer):
        print("You got it. Well done!")
        return True
    return False

def update_solution():
    global solution_text
    solution = ""
    for letter in answer:
        if letter.upper() in guessed_letters:
            solution += letter
        else:
            solution += "_"

    solution_text = solution

def check_letter(letter_guessed, button):
    global wrong_guess_amount, event_text, answer, guesses_left_text, event_text_surface, event_text_rect
    if letter_guessed in guessed_letters:
        event_text = f"You already guessed character '{letter_guessed}'"
        return
    
    guessed_letters.append(letter_guessed)

    if letter_guessed in answer.upper():
        event_text = f"Correct!"
        event_text_surface, event_text_rect = EVENT_FONT.render(event_text, GREEN_COLOR)
        button.change_color(True)
        

    elif letter_guessed not in answer.upper():
        event_text = f"Character not in word"
        event_text_surface, event_text_rect = EVENT_FONT.render(event_text, RED_COLOR)
        wrong_guess_amount += 1
        guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."
        button.change_color(False)
    
    update_solution()
    if(is_solved()):
        reset_game()
    elif wrong_guess_amount == max_wrong_guesses:
        event_text = f"Too many wrong guesses!"
        reset_game()

#button class
class Button():
    def __init__(self, x, y, letter):
        self.text_surface, self.rect = BUTTON_FONT.render(letter, BLACK_COLOR)
        self.rect.topleft = (x,y)
        self.letter = letter
        self.clicked = False
        self.correct_letter = None

    def change_color(self, correct_letter):
        if correct_letter:
            self.text_surface,_ = BUTTON_FONT.render(self.letter, GREEN_COLOR)
        elif not correct_letter:
            self.text_surface,_ = BUTTON_FONT.render(self.letter, RED_COLOR)
            self.text_surface.set_alpha(100)
    
    def draw(self):

        #get mouse position
        pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.clicked = False

        #check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            #print(f'Hovering on {self.letter}')
            if event.type == pygame.MOUSEBUTTONDOWN and not self.clicked:
                if event.button == 1:
                    self.clicked = True
                    check_letter(self.letter, self)
                    
        screen.blit(self.text_surface, (self.rect.x, self.rect.y))


def setup_buttons():
    global letter_buttons, screen_size_x, screen_size_y
    letter_buttons = []
    default_spacing = 70
    button_columns = int(screen_size_x / default_spacing)
    button_rows = int((screen_size_y / 2) / default_spacing)
    print(f"columns: {button_columns} rows: {button_rows} space: {button_columns * button_rows} required: {len(string.ascii_uppercase)}")
    while button_columns * button_rows <= len(string.ascii_uppercase):
        button_columns += 1
        
    print(f"columns: {button_columns} rows: {button_rows} space: {button_columns * button_rows} required: {len(string.ascii_uppercase)}")

    index_x = 1
    index_y = 1
    for letter in string.ascii_uppercase:
        letter_buttons.append(Button(int(screen_size_x/button_columns) * index_x, ((int((screen_size_y/2)/button_rows * index_y) + int(screen_size_y/2)) - 50), letter))
        index_x += 1
        if index_x >= button_columns:
            index_x = 1
            index_y += 1

running =  True

reset_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen_size_x, screen_size_y = screen.get_size()
            setup_buttons()

    screen.fill((255,255,255))
    for button in letter_buttons:
        button.draw()

    solution_text_surface, solution_text_rect = SOLUTION_FONT.render(solution_text, BLACK_COLOR)
    solution_text_rect.x = ((screen_size_x - solution_text_surface.get_rect()[2]) / 2)
    solution_text_rect.y = (((screen_size_y / 2) - solution_text_surface.get_rect()[3]) / 2) + 50
    screen.blit(solution_text_surface, (solution_text_rect.x, solution_text_rect.y))

    event_text_rect.x = ((screen_size_x - event_text_surface.get_rect()[2]) / 2)
    event_text_rect.y = (((screen_size_y / 2) - event_text_surface.get_rect()[3]) / 2) - 50
    screen.blit(event_text_surface, (event_text_rect.x, event_text_rect.y))

    empty_string = ""
    guessed_text_surface, guessed_text_rect = GUESS_FONT.render(empty_string.join(guessed_letters), BLACK_COLOR)
    guessed_text_rect.x = ((screen_size_x - guessed_text_surface.get_rect()[2]) / 2)
    guessed_text_rect.y = (((screen_size_y / 2) - guessed_text_surface.get_rect()[3]) / 2)
    screen.blit(guessed_text_surface, (guessed_text_rect.x, guessed_text_rect.y))
    
    guesses_left_text_surface, guesses_left_text_rect = GUESSES_LEFT_FONT.render(empty_string.join(guesses_left_text), BLACK_COLOR)
    guesses_left_text_rect.x = 5
    guesses_left_text_rect.y = 10
    screen.blit(guesses_left_text_surface, (guesses_left_text_rect.x, guesses_left_text_rect.y))

    pygame.display.flip()

pygame.quit()