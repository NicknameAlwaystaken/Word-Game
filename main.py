# Simple pygame program


# Import and initialize the pygame library

import pygame
import string
import random
import asyncio


class Game:
    def __init__(self):
        self.state = STATE_MENU
    
    def set_state(self, state):
        self.state = state
    
    def update(self):
        if self.state == STATE_PLAYING or self.state == STATE_SHOW_SOLUTION or self.state == STATE_GAME_WON:
            screen.fill(GAME_BACKGROUND_COLOR)
            for button in letter_buttons:
                button.draw()

            for item in ui_object_list[GAME_OBJECT]:
                object = ui_object_list[GAME_OBJECT][item]
                object_rect = object.get_rect()
                screen.blit(object.get_surface(), (object_rect.x, object_rect.y))
            
            if self.state == STATE_SHOW_SOLUTION or self.state == STATE_GAME_WON:
                for item in ui_object_list[GAME_END_OBJECT]:
                    object = ui_object_list[GAME_END_OBJECT][item]
                    if not object.is_hidden():
                        object_rect = object.get_rect()
                        screen.blit(object.get_surface(), (object_rect.x, object_rect.y))

        elif self.state == STATE_MENU:
            screen.fill(MENU_BACKGROUND_COLOR)
            for item in ui_object_list[MENU_OBJECT]:
                object = ui_object_list[MENU_OBJECT][item]
                if not object.is_hidden():
                    object_rect = object.get_rect()
                    screen.blit(object.get_surface(), (object_rect.x, object_rect.y))
        else:
            screen.fill(WHITE_COLOR)

class Interactive_Text:
    def __init__(self, text, color, font, custom_function = None, clickable = False):

        self.__clickable = clickable
        self.__custom_function = custom_function
        self.__hidden = False

        self.__font = font
        self.__default_font = font
        self.__previous_font = font

        self.__color = color
        self.__default_color = color
        self.__previous_color = color

        self.__text = text
        self.__default_text = text
        self.__previous_text = text

        surface = self.__font.render(self.__text, True, self.__color)
        self.__surface = surface
        self.__default_surface = surface
        self.__previous_surface = surface

        rect = surface.get_rect()
        self.__rect = rect
        self.__default_rect = rect
        self.__previous_rect = rect


    def clicked(self):
        if self.__clickable and self.__custom_function != None:
            self.__custom_function()

    def is_clickable(self):
        return self.__clickable
    
    def set_previous_font(self):
        self.__previous_font = self.__font
        self.__font = self.__previous_font
        self.__set_surface(self.__text, self.__color)
        
    def set_font(self, font):
        self.__previous_font = self.__font
        self.__font = font
        self.__set_surface(self.__text, self.__color)

    def reset_font(self):
        self.__previous_font = self.__font
        self.__font = self.__default_font
        self.__set_surface(self.__text, self.__color)

    def set_previous_color(self):
        self.__previous_color = self.__color
        self.__color = self.__previous_color
        self.__set_surface(self.__text, self.__color)
        
    def set_color(self, color):
        self.__previous_color = self.__color
        self.__color = color
        self.__set_surface(self.__text, self.__color)

    def reset_color(self):
        self.__previous_color = self.__color
        self.__color = self.__default_color
        self.__set_surface(self.text, self.color)

    def set_previous_text(self):
        self.__previous_text = self.__text
        self.__text = self.__previous_text
        self.__set_surface(self.__text, self.__color)
        
        
    def get_text(self):
        return self.__text
        
    def set_text(self, text, color = None):
        self.__previous_text = self.__text
        self.__text = text
        if color != None:
            self.set_color(color)
        else:
            self.__set_surface(self.__text, self.__color)

    def reset_text(self):
        self.__previous_text = self.__text
        self.__text = self.__default_text
        self.__set_surface(self.text, self.color)

    def update_surface(self):
        self.__set_surface(self.__text, self.__color)
        
    def __set_surface(self, text, color):
        self.__previous_surface = self.__surface
        self.__surface = self.__font.render(text, True, color)
        
    def get_surface(self):
        return self.__surface
        
    def set_previous_rect(self):
        self.__previous_rect = self.__rect
        self.__rect = self.__previous_rect
        
    def set_rect(self, rect):
        self.__previous_rect = self.__rect
        self.__rect = rect
        
    def get_rect(self):
        return self.__rect

    def reset_rect(self):
        self.__previous_rect = self.__ect
        self.__rect = self.__default_rect

    def hide(self, hide):
        if hide:
            self.__hidden = True
        elif not hide:
            self.__hidden = False

    def is_hidden(self):
        return self.__hidden

    def draw(self):
        if not self.__hidden:
            screen.blit(self.surface, (self.rect.x, self.rect.y))
    
    def custom_function(self):
        self.__custom_function()

class Letter_Button():

    def __init__(self, x, y, letter):
        self.text_surface = BUTTON_FONT.render(letter, True, BLACK_COLOR)
        self.rect = self.text_surface.get_rect()
        self.rect.topleft = (x,y)
        self.letter = letter
        self.is_clicked = False
        self.correct_letter = None
        self.color = BLACK_COLOR

    def change_color(self, color):
        self.text_surface = BUTTON_FONT.render(self.letter, True, color)
        self.color = color
        if color == RED_COLOR: 
            self.text_surface.set_alpha(100)
        else:
            self.text_surface.set_alpha(255)
    
    def draw(self):
        screen.blit(self.text_surface, (self.rect.x, self.rect.y))
    
    def clicked(self):
        self.is_clicked = True
        check_letter(self.letter, self)
    
    def not_clicked(self):
        self.is_clicked = False

    def change_location(self, x, y):
        self.rect.topleft = (x,y)
    
    def reset_size(self):
        self.text_surface = BUTTON_FONT.render(self.letter, True, self.color)

    def get_rect(self):
        return self.rect


def initialize_game():
    global letter_buttons, ui_object_list
    random.seed()
    letter_buttons = []
    for letter in string.ascii_uppercase:
        letter_buttons.append(Letter_Button(0, 0, letter))
    read_wordlist()
    fit_letter_buttons()
    init_ui_text(ui_object_list)

def read_wordlist():
    global list_of_answers
    list_of_answers = []
    with open("wordlist.txt", "r") as openfile:
        for line in openfile:
            word = line.rstrip()
            list_of_answers.append(word)

def get_new_word():
    global list_of_answers
    random_int = random.randrange(0, len(list_of_answers))
    return list_of_answers[random_int]

def go_to_main_menu():
    reset_game()
    game.set_state(STATE_MENU)

def new_round():
    reset_game()
    game.set_state(STATE_PLAYING)

def reset_game():
    global answer, wrong_guess_amount, max_wrong_guesses

    answer = get_new_word()

    wrong_guess_amount = 0

    reset_ui_text()
    reset_buttons()
    check_solution(answer)
    fit_ui_text()

def reset_ui_text():
    global wrong_guess_amount, max_wrong_guesses

    event_text = ""
    event_text_object = ui_object_list[GAME_OBJECT][GUESSED_LETTERS_TEXT]
    event_text_object.set_text(event_text)
    
    guesses_left = ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT]
    increment = int((COLOR_MAX_VALUE - INITIAL_DANGER_COLOR[0]) / max_wrong_guesses)
    new_color = ((INITIAL_DANGER_COLOR[0] + increment * wrong_guess_amount), INITIAL_DANGER_COLOR[1], INITIAL_DANGER_COLOR[2])
    guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."
    guesses_left.set_text(guesses_left_text, new_color)

def start_game():
    reset_game()
    game.set_state(STATE_PLAYING)

def init_ui_text(ui_object_list):
    empty_string = ""
    
    #Main menu ui text
    ui_object_list[MENU_OBJECT] = {}

    # Menu items go from bottom to top as order
    select_theme_text = f"Selected theme: {THEME_ALL}"
    ui_object_list[MENU_OBJECT][SELECT_THEME_BUTTON] = Interactive_Text(select_theme_text, DARK_BLUE_COLOR, SELECT_THEME_FONT)
    
    start_game_text = f"Start hangman!"
    ui_object_list[MENU_OBJECT][START_GAME_BUTTON] = Interactive_Text(start_game_text, DARK_GREEN_COLOR, START_GAME_FONT, start_game, True)
    

    #Playing state ui text
    ui_object_list[GAME_OBJECT] = {}

    # Menu items go from bottom to top as order

    ui_object_list[GAME_OBJECT][SOLUTION_TEXT] = Interactive_Text(solution_text, BLACK_COLOR, SOLUTION_FONT)

    event_text = ""
    ui_object_list[GAME_OBJECT][EVENT_TEXT] = Interactive_Text(event_text, BLACK_COLOR, EVENT_FONT)
    
    ui_object_list[GAME_OBJECT][GUESSED_LETTERS_TEXT] = Interactive_Text(empty_string, BLACK_COLOR, GUESS_FONT)
    

    guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."
    new_color = (((COLOR_MAX_VALUE - INITIAL_DANGER_COLOR[0] / max_wrong_guesses) * wrong_guess_amount), INITIAL_DANGER_COLOR[1], INITIAL_DANGER_COLOR[2])
    ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT] = Interactive_Text(guesses_left_text, new_color, GUESSES_LEFT_FONT)

    #Post game ui text
    ui_object_list[GAME_END_OBJECT] = {}
    
    continue_text = f"Click here to continue!"
    ui_object_list[GAME_END_OBJECT][CONTINUE_TEXT] = Interactive_Text(continue_text, DARK_BLUE_COLOR, CONTINUE_FONT, new_round, True)

    fit_ui_text()


def reset_buttons():
    global letter_buttons
    for button in letter_buttons:
        button.change_color(BLACK_COLOR)

def game_won(answer):
    global guesses_left_text_surface

    guesses_left_text = f""
    ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT].set_text(guesses_left_text)

    ui_object_list[GAME_OBJECT][SOLUTION_TEXT].set_text(answer, SOLVED_COLOR)

def solve_word(answer):
    global guesses_left_text, guesses_left_text_surface

    guesses_left_text = f""
    ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT].set_text(guesses_left_text)

    ui_object_list[GAME_OBJECT][SOLUTION_TEXT].set_text(answer, UNSOLVED_COLOR)

def check_solution(answer):
    solution = ""
    guessed_letters_object = ui_object_list[GAME_OBJECT][GUESSED_LETTERS_TEXT]
    guessed_letters = guessed_letters_object.get_text()

    for letter in answer:
        if letter.upper() in guessed_letters or letter.upper() not in string.ascii_uppercase:
            solution += letter
        else:
            solution += "_"
    
    ui_object_list[GAME_OBJECT][SOLUTION_TEXT].set_text(solution, BLACK_COLOR)

    if answer == solution:
        return True
    return False


def check_letter(letter_guessed, button):
    global wrong_guess_amount, answer, ui_object_list
    event_text_object = ui_object_list[GAME_OBJECT][EVENT_TEXT]
    guessed_letters_object = ui_object_list[GAME_OBJECT][GUESSED_LETTERS_TEXT]
    guessed_letters = guessed_letters_object.get_text()
    if letter_guessed in guessed_letters:
        event_text_object.set_text(f"You already guessed character '{letter_guessed}'", BLACK_COLOR)
        place_event_text(event_text_object)
        return
    
    new_solution = guessed_letters + letter_guessed
    guessed_letters_object.set_text(''.join(sorted(new_solution)))
    place_guessed_letters_text(guessed_letters_object)

    if letter_guessed in answer.upper():
        event_text_object.set_text(f"Correct!", GREEN_COLOR)
        place_event_text(event_text_object)
        button.change_color(GREEN_COLOR)

    elif letter_guessed not in answer.upper():
        event_text_object.set_text(f"Character '{letter_guessed}' not in word", RED_COLOR)
        place_event_text(event_text_object)
        wrong_guess_amount += 1

        guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."

        guesses_left = ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT]
        increment = int((COLOR_MAX_VALUE - INITIAL_DANGER_COLOR[0]) / max_wrong_guesses)
        new_color = ((INITIAL_DANGER_COLOR[0] + increment * wrong_guess_amount), INITIAL_DANGER_COLOR[1], INITIAL_DANGER_COLOR[2])
        guesses_left.set_text(guesses_left_text, new_color)

        button.change_color(RED_COLOR)
    
    

    if(check_solution(answer)):
        event_text_object.set_text(f"You won!", BLACK_COLOR)
        place_event_text(event_text_object)
        guesses_left = ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT]
        guesses_left.set_text("")
        game.set_state(STATE_GAME_WON)
        game_won(answer)

    elif wrong_guess_amount == max_wrong_guesses:
        event_text_object.set_text(f"Too many wrong guesses!", BLACK_COLOR)
        place_event_text(event_text_object)
        guesses_left = ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT]
        guesses_left.set_text("")
        game.set_state(STATE_SHOW_SOLUTION)
        solve_word(answer)

def place_guessed_letters_text(guessed_letters_object):
    guessed_letters = guessed_letters_object
    guessed_text_rect = guessed_letters.get_rect()
    guessed_text_rect.x = ((screen_size_x - guessed_letters.get_surface().get_rect()[2]) / 2)
    guessed_text_rect.y = (((screen_size_y / 2) - guessed_letters.get_surface().get_rect()[3]) / 2)
    guessed_letters.set_rect(guessed_text_rect)

def place_event_text(event_text_object):
    event_text_rect = event_text_object.get_rect()
    event_text_rect.x = ((screen_size_x - event_text_object.get_surface().get_rect()[2]) / 2)
    event_text_rect.y = (((screen_size_y / 2) - event_text_object.get_surface().get_rect()[3]) / 2) - 50
    event_text_object.set_rect(event_text_rect)


def fit_letter_buttons():
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

    button_layout_size_x = screen_size_x - row_padding
    button_layout_size_y = screen_size_y / 2
    for button in letter_buttons:
        x_location = button_layout_size_x/button_columns * index_x + row_padding / 2
        y_location = (button_layout_size_y/button_rows * index_y) + button_layout_size_y

        button.change_location(int(x_location), int(y_location))
        button.reset_size()

        index_x += 1
        if index_x >= button_columns:
            index_x = 0
            index_y += 1

def fit_ui_text():
    #Start menu ui text
    start_menu_layout_size_y = screen_size_y / 2
    start_menu_layout_padding_y = (start_menu_layout_size_y / 2) + DEFAULT_FONT_SIZE

    menu_button_amount = len(ui_object_list[MENU_OBJECT])
    menu_order = 0
    
    for item in ui_object_list[MENU_OBJECT]:
        object = ui_object_list[MENU_OBJECT][item]
        object_rect = object.get_rect()
        object_rect.x = ((screen_size_x - object.get_rect()[2]) / 2)
        object_rect.y = screen_size_y - (((start_menu_layout_size_y / menu_button_amount) / 2 * (menu_order * 2 + 1)) + start_menu_layout_padding_y)
        object.set_rect(object_rect)
        object.update_surface()

        menu_order += 1


    #Playing state ui text
    solution_text = ui_object_list[GAME_OBJECT][SOLUTION_TEXT]
    solution_text_rect = solution_text.get_rect()
    solution_text_rect.x = ((screen_size_x - solution_text.get_surface().get_rect()[2]) / 2)
    solution_text_rect.y = (((screen_size_y / 2) - solution_text_rect[3]) / 2) + 50
    solution_text.set_rect(solution_text_rect)
    
    event_text = ui_object_list[GAME_OBJECT][EVENT_TEXT]
    event_text_rect = event_text.get_rect()
    event_text_rect.x = ((screen_size_x - event_text.get_surface().get_rect()[2]) / 2)
    event_text_rect.y = (((screen_size_y / 2) - event_text.get_surface().get_rect()[3]) / 2) - 50
    event_text.set_rect(event_text_rect)
    
    
    guessed_letters = ui_object_list[GAME_OBJECT][GUESSED_LETTERS_TEXT]
    guessed_text_rect = guessed_letters.get_rect()
    guessed_text_rect.x = ((screen_size_x - guessed_letters.get_surface().get_rect()[2]) / 2)
    guessed_text_rect.y = (((screen_size_y / 2) - guessed_letters.get_surface().get_rect()[3]) / 2)
    guessed_letters.set_rect(guessed_text_rect)
    
    guesses_left = ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT]
    guesses_left_text_rect = guesses_left.get_rect()
    guesses_left_text_rect.x = 5
    guesses_left_text_rect.y = 10
    guesses_left.set_rect(guesses_left_text_rect)


    #Post game ui text
    continue_text = ui_object_list[GAME_END_OBJECT][CONTINUE_TEXT]
    continue_text_rect = continue_text.get_rect()
    continue_text_rect.x = 5
    continue_text_rect.y = 10
    continue_text.set_rect(continue_text_rect)


pygame.init()

INIT_SCREEN_WIDTH = 800
INIT_SCREEN_HEIGHT = 600

RED_COLOR = (200, 50, 25)
GREEN_COLOR = (16, 200, 40)
DARK_GREEN_COLOR = (8, 130, 20)
DARK_BLUE_COLOR = (50, 50, 150)
LIGHT_BLUE_COLOR = (138, 160, 242)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

COLOR_MAX_VALUE = 255

INITIAL_DANGER_COLOR = (0, 0, 0)

SOLVED_COLOR = GREEN_COLOR
UNSOLVED_COLOR = RED_COLOR

TEMP_COLOR_HOLDER = (174, 199, 245)

MENU_BACKGROUND_COLOR = TEMP_COLOR_HOLDER
GAME_BACKGROUND_COLOR = TEMP_COLOR_HOLDER

#Theme names
THEME_ALL = "ALL"
THEME_GAMING = "GAMING"

DEFAULT_BUTTON_FONT_SIZE = 50
DEFAULT_FONT_SIZE = 50

FONT_FILE_NAME = "YoungSerif-Regular.ttf"

GUESS_FONT = pygame.font.Font(FONT_FILE_NAME, 30)
SOLUTION_FONT = pygame.font.Font(FONT_FILE_NAME, 40)
EVENT_FONT = pygame.font.Font(FONT_FILE_NAME, 20)
BUTTON_FONT = pygame.font.Font(FONT_FILE_NAME, DEFAULT_BUTTON_FONT_SIZE)
GUESSES_LEFT_FONT = pygame.font.Font(FONT_FILE_NAME, 25)
START_GAME_FONT = pygame.font.Font(FONT_FILE_NAME, 70)
SELECT_THEME_FONT = pygame.font.Font(FONT_FILE_NAME, 50)
CONTINUE_FONT = pygame.font.Font(FONT_FILE_NAME, 30)

screen = pygame.display.set_mode((INIT_SCREEN_WIDTH, INIT_SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.RESIZABLE)
screen_size_x, screen_size_y = screen.get_size()


answer = ""
letter_buttons = []
solution_text = len(answer) * "_"
event_text = ""
event_text_surface = EVENT_FONT.render(event_text, True, BLACK_COLOR)
wrong_guess_amount = 0
max_wrong_guesses = 8

guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."

clock = pygame.time.Clock()

STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_SHOW_SOLUTION = "SHOW_SOLUTION"
STATE_GAME_WON = "GAME_WON"

game = Game()

#end of game related objects
GAME_END_OBJECT = "GAME_END_OBJECT"

CONTINUE_TEXT = "CONTINUE_TEXT"


# game related objects
GAME_OBJECT = "GAME_OBJECT"
SOLUTION_TEXT = "SOLUTION_TEXT"
EVENT_TEXT = "EVENT_TEXT"
GUESSED_LETTERS_TEXT = "GUESSED_LETTERS_TEXT"
GUESSES_LEFT_TEXT = "GUESSES_LEFT_TEXT"

# menu related objects
MENU_OBJECT = "MENU_OBJECT"

START_GAME_BUTTON = "START_GAME_BUTTON"
SELECT_THEME_BUTTON = "SELECT_THEME_BUTTON"

ui_object_list = {}


async def main():
    global screen_size_x, screen_size_y

    initialize_game()
    reset_game()

    running =  True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                screen_size_x, screen_size_y = screen.get_size()
                fit_letter_buttons()
                fit_ui_text()

            if(game.state == STATE_MENU): # Main menu
                object_list_index = MENU_OBJECT
                #Keyboard events
                if(event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_RETURN:
                        start_game()
                        game.set_state(STATE_PLAYING)

                #Mouse events
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    if event.button == 1: # 1 = left click
                        mouse_left_click_event(object_list_index)

                #Touch screen finger events
                if(event.type == pygame.FINGERDOWN):
                    finger_tap_event(event, object_list_index)

            elif(game.state == STATE_PLAYING): # playing state
                #Keyboard events
                if(event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_ESCAPE:
                        go_to_main_menu()
                    else:
                        for button in letter_buttons:
                            try:
                                if chr(event.key).upper() == button.letter:
                                    button.clicked()
                                else:
                                    button.not_clicked()
                            except:
                                continue
                #Mouse events
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    if event.button == 1: # 1 = left click
                        mouse_pos = pygame.mouse.get_pos()
                        for button in letter_buttons:
                            button_rect = button.get_rect()
                            if button_rect.collidepoint(mouse_pos):
                                button.clicked()
                            else:
                                button.not_clicked()
                            
                #Touch screen finger events
                if(event.type == pygame.FINGERDOWN):
                    fingers = get_fingers(event)
                    for finger, finger_pos in fingers.items():
                        if button_rect.collidepoint(finger_pos):
                            button.clicked()
                        else:
                            button.not_clicked()

            elif(game.state == STATE_SHOW_SOLUTION or game.state == STATE_GAME_WON): #Game/round ended
                object_list_index = GAME_END_OBJECT
                #Keyboard events
                if(event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_RETURN:
                        new_round()
                    elif event.key == pygame.K_ESCAPE:
                        go_to_main_menu()

                #Mouse events
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    if event.button == 1: # 1 = left click
                        mouse_left_click_event(object_list_index)

                #Touch screen finger events
                elif(event.type == pygame.FINGERDOWN):
                    finger_tap_event(event, object_list_index)
            


        game.update()
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

def mouse_left_click_event(object_list_index):
    mouse_pos = pygame.mouse.get_pos()
    for item in ui_object_list[object_list_index]:
        object = ui_object_list[object_list_index][item]
        if object.get_rect().collidepoint(mouse_pos):
            if object.is_clickable():
                object.custom_function()

def finger_tap_event(event, object_list_index):
    fingers = get_fingers(event)
    for finger, finger_pos in fingers.items():
        for item in ui_object_list[object_list_index]:
            object = ui_object_list[object_list_index][item]
            if object.get_rect().collidepoint(finger_pos):
                if object.is_clickable():
                    object.custom_function()

def get_fingers(event):
    fingers = {}
    x = event.x * screen.get_height()
    y = event.y * screen.get_width()
    fingers[event.finger_id] = x, y
    return fingers

asyncio.run(main())