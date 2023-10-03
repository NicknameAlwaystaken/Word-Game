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

DEFAULT_BUTTON_FONT_SIZE = 50

GUESS_FONT = pygame.freetype.Font("YoungSerif-Regular.ttf", 30)
SOLUTION_FONT = pygame.freetype.Font("YoungSerif-Regular.ttf", 40)
EVENT_FONT = pygame.freetype.Font("YoungSerif-Regular.ttf", 20)
BUTTON_FONT = pygame.freetype.Font("YoungSerif-Regular.ttf", DEFAULT_BUTTON_FONT_SIZE)
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

def initialize_game():
    global letter_buttons
    random.seed()
    letter_buttons = []
    for letter in string.ascii_uppercase:
        letter_buttons.append(Button(0, 0, letter))
    read_wordlist()
    fit_buttons()

def read_wordlist():
    global list_of_answers
    list_of_answers = []
    with open("wordlist.txt", "r") as openfile:
        for line in openfile:
            word = line.strip()
            list_of_answers.append(word)

def get_new_word():
    global list_of_answers
    random_int = random.randrange(0, len(list_of_answers))
    return list_of_answers[random_int]

def reset_game():
    global answer, guessed_letters, solution_text, event_text, wrong_guess_amount
    global max_wrong_guesses, letter_buttons

    answer = get_new_word()
    guessed_letters = []


    event_text = ""
    wrong_guess_amount = 0
    max_wrong_guesses = 8

    reset_buttons()
    update_solution()
    init_ui_text()
    fit_ui_text()

def init_ui_text():
    global answer, guesses_left_text_surface, guesses_left_text_rect, solution_text_surface, solution_text_rect, guessed_text_surface, guessed_text_rect
    empty_string = ""

    solution_text_surface, solution_text_rect = SOLUTION_FONT.render(solution_text, BLACK_COLOR)
    
    guessed_text_surface, guessed_text_rect = GUESS_FONT.render(empty_string.join(guessed_letters), BLACK_COLOR)
    guessed_text_rect.x = ((screen_size_x - guessed_text_surface.get_rect()[2]) / 2)
    guessed_text_rect.y = (((screen_size_y / 2) - guessed_text_surface.get_rect()[3]) / 2)

    guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."
    guesses_left_text_surface, guesses_left_text_rect = GUESSES_LEFT_FONT.render(guesses_left_text, BLACK_COLOR)
    guesses_left_text_rect.x = 5
    guesses_left_text_rect.y = 10

def reset_buttons():
    global letter_buttons
    for button in letter_buttons:
        button.change_color(BLACK_COLOR)

def is_solved():
    if(solution_text == answer):
        print("You got it. Well done!")
        return True
    return False

def update_solution():
    global solution_text, solution_text_surface
    solution = ""
    for letter in answer:
        if letter.upper() in guessed_letters or letter in string.punctuation:
            solution += letter
        else:
            solution += "_"

    solution_text = solution
    solution_text_surface,_ = SOLUTION_FONT.render(solution_text, BLACK_COLOR)

def check_letter(letter_guessed, button):
    global wrong_guess_amount, event_text, answer, guesses_left_text, event_text_surface, event_text_rect, guesses_left_text_surface
    if letter_guessed in guessed_letters:
        display_event_text(f"You already guessed character '{letter_guessed}'", BLACK_COLOR)
        return
    
    guessed_letters.append(letter_guessed)

    if letter_guessed in answer.upper():
        display_event_text("Correct!", GREEN_COLOR)
        button.change_color(GREEN_COLOR)
        

    elif letter_guessed not in answer.upper():
        display_event_text("Character not in word", RED_COLOR)
        wrong_guess_amount += 1
        guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."
        guesses_left_text_surface,_ = GUESSES_LEFT_FONT.render(guesses_left_text, BLACK_COLOR)
        button.change_color(RED_COLOR)
    
    update_solution()

    if(is_solved()):
        display_event_text("You won!", GREEN_COLOR)
        reset_game()
    elif wrong_guess_amount == max_wrong_guesses:
        display_event_text("Too many wrong guesses!", RED_COLOR)
        reset_game()

def display_event_text(text, color):
    global event_text_rect, event_text_surface
    event_text = text
    event_text_surface,_ = EVENT_FONT.render(event_text, color)
    event_text_rect.x = ((screen_size_x - event_text_surface.get_rect()[2]) / 2)
    event_text_rect.y = (((screen_size_y / 2) - event_text_surface.get_rect()[3]) / 2) - 50

#button class
class Button():
    def __init__(self, x, y, letter):
        self.text_surface, self.rect = BUTTON_FONT.render(letter, BLACK_COLOR)
        self.rect.topleft = (x,y)
        self.letter = letter
        self.clicked = False
        self.correct_letter = None
        self.color = BLACK_COLOR

    def change_color(self, color):
        self.text_surface, new_location = BUTTON_FONT.render(self.letter, color)
        self.color = color
        if color == RED_COLOR: 
            self.text_surface.set_alpha(100)
        else:
            self.text_surface.set_alpha(255)
    
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

    def change_location(self, x, y):
        self.rect.topleft = (x,y)
    
    def reset_size(self):
        self.text_surface,_ = BUTTON_FONT.render(self.letter, self.color)



def fit_buttons():
    global letter_buttons, screen_size_x, screen_size_y
    default_spacing = 70
    button_columns = int(screen_size_x / default_spacing)
    button_rows = int((screen_size_y / 2) / default_spacing)

    is_extra_space = True
    max_characters = len(string.ascii_uppercase)

    while button_columns * (button_rows - 1) > max_characters:
        button_columns -= 1
        if(max_characters / button_columns >= 4):
            break

    while button_columns * button_rows < max_characters:
        button_columns += 1
        is_extra_space = False

    index_x = 0
    index_y = 0
    row_padding = 0

    if is_extra_space:
        row_padding = (screen_size_x - (button_columns * (default_spacing + 1)) )

    BUTTON_FONT.size = DEFAULT_BUTTON_FONT_SIZE
    if(row_padding >= 200):
        BUTTON_FONT.size += int((row_padding - 200) / 10)
        if(BUTTON_FONT.size > 65):
            BUTTON_FONT.size = 65
    elif row_padding <= 0:
        BUTTON_FONT.size = 40

    button_layout_size_x = screen_size_x - row_padding
    button_layout_size_y = screen_size_y / 2
    print(f"button_columns {button_columns} BUTTON_FONT.size {BUTTON_FONT.size} row_padding {row_padding}")
    for button in letter_buttons:
        x_location = button_layout_size_x/button_columns * index_x + row_padding / 2
        y_location = (button_layout_size_y/button_rows * index_y) + button_layout_size_y

        button.change_location(int(x_location), int(y_location))
        button.reset_size()

        index_x += 1
        if index_x >= button_columns:
            index_x = 0
            index_y += 1
    
    print(f"columns: {button_columns} rows: {button_rows} space: {button_columns * button_rows} required: {max_characters}")

def fit_ui_text():
    global solution_text_rect, solution_text_surface, event_text_rect, event_text_surface, guessed_text_rect, guessed_text_surface, guesses_left_text_rect, guesses_left_text_surface

    solution_text_rect.x = ((screen_size_x - solution_text_surface.get_rect()[2]) / 2)
    solution_text_rect.y = (((screen_size_y / 2) - solution_text_surface.get_rect()[3]) / 2) + 50
    
    event_text_rect.x = ((screen_size_x - event_text_surface.get_rect()[2]) / 2)
    event_text_rect.y = (((screen_size_y / 2) - event_text_surface.get_rect()[3]) / 2) - 50
    
    guessed_text_rect.x = ((screen_size_x - guessed_text_surface.get_rect()[2]) / 2)
    guessed_text_rect.y = (((screen_size_y / 2) - guessed_text_surface.get_rect()[3]) / 2)
    
    guesses_left_text_rect.x = 5
    guesses_left_text_rect.y = 10

running =  True

initialize_game()
reset_game()

ui_text_list = [[solution_text_surface, solution_text_rect], [event_text_surface, event_text_rect],
                [guessed_text_surface, guessed_text_rect], [guesses_left_text_surface, guesses_left_text_rect]
                ]


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            screen_size_x, screen_size_y = screen.get_size()
            fit_buttons()
            fit_ui_text()

    screen.fill((255,255,255))
    for button in letter_buttons:
        button.draw()

    #for i in range(len(ui_text_list)):
        #screen.blit(ui_text_list[i][0], (ui_text_list[i][1].x, ui_text_list[i][1].y))

    screen.blit(solution_text_surface, solution_text_rect)
    screen.blit(event_text_surface, event_text_rect)
    screen.blit(guessed_text_surface, guessed_text_rect)
    screen.blit(guesses_left_text_surface, guesses_left_text_rect)
    

    pygame.display.flip()

pygame.quit()