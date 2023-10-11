# Simple pygame program


# Import and initialize the pygame library

import pygame
import string
import random
import asyncio
from pygame import gfxdraw


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
                object.draw()
                #object_rect = object.get_rect()
                #screen.blit(object.get_surface(), (object_rect.x, object_rect.y))
            
            if self.state == STATE_SHOW_SOLUTION or self.state == STATE_GAME_WON:
                for item in ui_object_list[GAME_END_OBJECT]:
                    object = ui_object_list[GAME_END_OBJECT][item]
                    object.draw()
                    #if not object.is_hidden():
                        #object_rect = object.get_rect()
                        #screen.blit(object.get_surface(), (object_rect.x, object_rect.y))

        elif self.state == STATE_MENU:
            screen.fill(MENU_BACKGROUND_COLOR)
            for item in ui_object_list[MENU_OBJECT]:
                object = ui_object_list[MENU_OBJECT][item]
                object.draw()
                #if not object.is_hidden():
                    #object_rect = object.get_rect()
                    #screen.blit(object.get_surface(), (object_rect.x, object_rect.y))
        else:
            screen.fill(WHITE_COLOR)

class Interactive_Text:
    def __init__(self, text: string, color: pygame.color.Color, font: pygame.font.Font, custom_function = None, clickable: bool = False):

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

        self.__animation_step = 0
        self.__is_animating = False
        self.__animation = "NONE"


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
        
        
    def set_rect_center(self, rect):
        self.__previous_rect = self.__rect
        self.__rect.center = rect
        
    def get_rect_center(self):
        return self.__rect.center
        
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
    
    def set_animation(self, animation):
        self.__animation = animation
        self.__is_animating = True

    def stop_animation(self):
        self.__is_animating = False
        
    def get_animation_step(self):
        return self.__animation_step
    
    def set_animation_step(self, step):
        self.__animation_step = step

    def draw(self):
        if self.__is_animating:
            if self.__animation == ANIMATION_RESET:
                half_steps = int(ANIMATION_RESET_FRAMES / 2)
                max_scale = ANIMATION_RESET_SCALE
                scaling_up = True
                scale_animation(self, half_steps, max_scale, scaling_up, ANIMATION_RESET_FRAMES)

            if self.__animation == ANIMATION_SHAKE:
                half_steps = int(ANIMATION_SHAKE_FRAMES / 2)
                strength = ANIMATION_SHAKE_STRENGTH
                style = ANIMATION_SHAKE_RANDOM
                shake_animation(self, half_steps, strength, style, ANIMATION_SHAKE_FRAMES)
        else:
            if not self.__hidden:
                screen.blit(self.__surface, (self.__rect.x, self.__rect.y))
                
    
    def custom_function(self):
        self.__custom_function()

class Letter_Button():

    def __init__(self, x, y, letter):
        self.__font = BUTTON_FONT
        self.__surface = self.__font.render(letter, True, BLACK_COLOR)
        self.__x_center = x
        self.__y_center = y
        self.__rect = self.__surface.get_rect()
        self.__rect.center = (self.__x_center, self.__y_center)
        self.letter = letter
        self.is_clicked = False
        self.correct_letter = None
        self.color = BLACK_COLOR
        self.__animation_step = 0
        self.__is_animating = False
        self.__animation = "NONE"

    def change_color(self, color):
        self.__surface = self.__font.render(self.letter, True, color)
        self.color = color

    def change_alpha(self, alpha):
        self.__surface.set_alpha(alpha)

    
    def draw(self):
        if self.is_clicked:
            self.__is_animating = True
            self.__animation = ANIMATION_CLICKED
            if self.__animation_step == -1:
                self.__animation_step = 0

        if self.__is_animating:
            if self.__animation == ANIMATION_CLICKED:
                half_steps = int(ANIMATION_CLICKED_FRAMES / 2)
                max_scale = ANIMATION_CLICKED_SCALE
                scaling_up = False
                scale_animation(self, half_steps, max_scale, scaling_up, ANIMATION_CLICKED_FRAMES)

            elif self.__animation == ANIMATION_RESET:
                half_steps = int(ANIMATION_LETTER_BUTTON_RESET_FRAMES / 2)
                max_scale = ANIMATION_LETTER_BUTTON_RESET_SCALE
                scaling_up = True
                scale_animation(self, half_steps, max_scale, scaling_up, ANIMATION_LETTER_BUTTON_RESET_FRAMES)
        else:
            screen.blit(self.__surface, self.__rect)
    
    def clicked(self):
        self.is_clicked = True
        check_letter(self.letter, self)
    
    def not_clicked(self):
        self.is_clicked = False
        
    def set_animation(self, animation):
        self.__animation = animation
        self.__is_animating = True

    def stop_animation(self):
        self.__is_animating = False

    def set_rect(self, rect):
        self.__rect = rect

    def set_rect_center(self, rect):
        self.__rect.center = rect
        self.__x_center, self.__y_center = rect
        
    def get_rect_center(self):
        return self.__rect.center
    
    def reset_size(self):
        self.__surface = BUTTON_FONT.render(self.letter, True, self.color)
        self.__rect = self.__surface.get_rect()

    def get_rect(self):
        return self.__rect
    
    def get_surface(self):
        return self.__surface
    
    def get_animation_step(self):
        return self.__animation_step
    
    def set_animation_step(self, step):
        self.__animation_step = step

def shake_animation(self, half_steps, strength, style, animation_frames):
    current_step = self.get_animation_step()
    new_surface = self.get_surface()
    
    new_rect = new_surface.get_rect()
    new_rect.center = self.get_rect_center()

    rand_x = random.randrange(-strength, strength)
    rand_y = random.randrange(-strength, strength)

    new_rect.center = (new_rect.center[0] + rand_x, new_rect.center[1] + rand_y)

    screen.blit(new_surface, new_rect)

    self.set_animation_step(current_step + 1)
    if current_step + 1 > animation_frames:
        self.set_animation_step(-1)
        self.stop_animation()

def scale_animation(self, half_steps, max_scale, scaling_up, animation_frames):
    current_step = self.get_animation_step()
    current_scale = max_scale / half_steps * current_step

    if current_step >= half_steps and current_scale >= max_scale:
        current_scale = max(max_scale - (current_scale - max_scale), 0)
    if not scaling_up:
        new_surface = pygame.transform.scale_by(self.get_surface(), 1.0 - current_scale)
    if scaling_up:
        new_surface = pygame.transform.scale_by(self.get_surface(), 1.0 + current_scale)
    new_rect = new_surface.get_rect()
    new_rect.center = self.get_rect_center()
    screen.blit(new_surface, new_rect)

    self.set_animation_step(current_step + 1)
    if current_step + 1 > animation_frames:
        self.set_animation_step(-1)
        self.stop_animation()

def initialize_game():
    global letter_buttons, ui_object_list, object_list_index
    random.seed()
    letter_buttons = []
    for letter in string.ascii_uppercase:
        letter_buttons.append(Letter_Button(0, 0, letter))
    
    object_list_index = MENU_OBJECT

    fit_letter_buttons()
    init_ui_text(ui_object_list)

def read_wordlist():
    global list_of_answers, theme_list, difficulty_list, theme_index, difficulty_index
    list_of_answers = []
    file_name = "theme" + theme_list[theme_index] + difficulty_list[difficulty_index] + "wordlist.txt"
    with open(file_name, "r") as openfile:
        for line in openfile:
            word = line.rstrip()
            list_of_answers.append(word)

def get_new_word():
    global list_of_answers
    random_int = random.randrange(0, len(list_of_answers))
    return list_of_answers[random_int]

def go_to_main_menu():
    game.set_state(STATE_MENU)

def cycle_themes():
    global theme_list, theme_index
    theme_index += 1
    if theme_index >= len(theme_list):
        theme_index = 0
    
    text = f"Selected theme: {theme_list[theme_index]}"
    ui_object_list[MENU_OBJECT][SELECT_THEME_BUTTON].set_text(text)
    fit_ui_text()
    
def cycle_difficulty():
    global difficulty_list, difficulty_index
    difficulty_index += 1
    if difficulty_index >= len(difficulty_list):
        difficulty_index = 0
    
    text = f"Selected difficulty: {difficulty_list[difficulty_index]}"
    ui_object_list[MENU_OBJECT][SELECT_DIFFICULTY_BUTTON].set_text(text)
    fit_ui_text()

def new_round():
    reset_game()
    game.set_state(STATE_PLAYING)

def reset_game():
    global answer, wrong_guess_amount, max_wrong_guesses

    read_wordlist()
    answer = get_new_word()

    wrong_guess_amount = 0

    reset_ui_text()
    reset_buttons()
    check_solution(answer)
    fit_ui_text()

def reset_ui_text():
    global wrong_guess_amount, max_wrong_guesses

    event_text = ""
    event_text_object = ui_object_list[GAME_OBJECT][EVENT_TEXT]
    event_text_object.set_text(event_text)
    
    guessed_text = ""
    guessed_text_object = ui_object_list[GAME_OBJECT][GUESSED_LETTERS_TEXT]
    guessed_text_object.set_text(guessed_text)
    
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

    # Menu items
    start_game_text = f"Start hangman!"
    ui_object_list[MENU_OBJECT][START_GAME_BUTTON] = Interactive_Text(start_game_text, DARK_GREEN_COLOR, START_GAME_FONT, start_game, True)
    
    select_difficulty_text = f"Selected difficulty: {difficulty_list[difficulty_index]}"
    ui_object_list[MENU_OBJECT][SELECT_DIFFICULTY_BUTTON] = Interactive_Text(select_difficulty_text, DARK_BLUE_COLOR, SELECT_DIFFICULTY_THEME_FONT, cycle_difficulty, True)

    select_theme_text = f"Selected theme: {theme_list[theme_index]}"
    ui_object_list[MENU_OBJECT][SELECT_THEME_BUTTON] = Interactive_Text(select_theme_text, DARK_BLUE_COLOR, SELECT_THEME_FONT, cycle_themes, True)
    
    

    #Playing state ui text
    ui_object_list[GAME_OBJECT] = {}

    # Items are ontop of each other

    ui_object_list[GAME_OBJECT][SOLUTION_TEXT] = Interactive_Text(solution_text, BLACK_COLOR, SOLUTION_FONT)

    event_text = ""
    ui_object_list[GAME_OBJECT][EVENT_TEXT] = Interactive_Text(event_text, BLACK_COLOR, EVENT_FONT)
    
    ui_object_list[GAME_OBJECT][GUESSED_LETTERS_TEXT] = Interactive_Text(empty_string, BLACK_COLOR, GUESS_FONT)
    
    # Other items

    back_button_text = f"BACK"
    ui_object_list[GAME_OBJECT][BACK_BUTTON] = Interactive_Text(back_button_text, BLACK_COLOR, BACK_BUTTON_FONT, go_to_main_menu, True)

    guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."
    new_color = (((COLOR_MAX_VALUE - INITIAL_DANGER_COLOR[0] / max_wrong_guesses) * wrong_guess_amount), INITIAL_DANGER_COLOR[1], INITIAL_DANGER_COLOR[2])
    ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT] = Interactive_Text(guesses_left_text, new_color, GUESSES_LEFT_FONT)

    #Post game ui items
    ui_object_list[GAME_END_OBJECT] = {}
    
    back_button_text = f"BACK"
    ui_object_list[GAME_END_OBJECT][BACK_BUTTON] = Interactive_Text(back_button_text, BLACK_COLOR, BACK_BUTTON_FONT, go_to_main_menu, True) # back button is twice, easier to do it this way, may need changing later.

    continue_text = f"Click here to continue!"
    ui_object_list[GAME_END_OBJECT][CONTINUE_TEXT] = Interactive_Text(continue_text, DARK_BLUE_COLOR, CONTINUE_FONT, new_round, True)

    fit_ui_text()


def reset_buttons():
    global letter_buttons
    for button in letter_buttons:
        button.change_color(BLACK_COLOR)
        button.change_alpha(COLOR_MAX_VALUE)
        button.set_animation(ANIMATION_RESET)

def game_won(answer):
    global guesses_left_text_surface

    guesses_left_text = f""
    ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT].set_text(guesses_left_text)

    ui_object_list[GAME_OBJECT][SOLUTION_TEXT].set_text(answer, SOLVED_COLOR)
    ui_object_list[GAME_OBJECT][SOLUTION_TEXT].set_animation(ANIMATION_RESET)

def solve_word(answer):
    global guesses_left_text, guesses_left_text_surface

    guesses_left_text = f""
    ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT].set_text(guesses_left_text)

    ui_object_list[GAME_OBJECT][SOLUTION_TEXT].set_text(answer, UNSOLVED_COLOR)
    ui_object_list[GAME_OBJECT][SOLUTION_TEXT].set_animation(ANIMATION_SHAKE)

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
        fit_ui_text()
        return
    
    new_solution = guessed_letters + letter_guessed
    guessed_letters_object.set_text(''.join(sorted(new_solution)))

    if letter_guessed in answer.upper():
        event_text_object.set_text(f"Correct!", GREEN_COLOR)
        button.change_color(GREEN_COLOR)
        button.change_alpha(COLOR_MAX_VALUE)

    elif letter_guessed not in answer.upper():
        event_text_object.set_text(f"Character '{letter_guessed}' not in word", RED_COLOR)
        wrong_guess_amount += 1

        guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."

        guesses_left = ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT]
        increment = int((COLOR_MAX_VALUE - INITIAL_DANGER_COLOR[0]) / max_wrong_guesses)
        new_color = ((INITIAL_DANGER_COLOR[0] + increment * wrong_guess_amount), INITIAL_DANGER_COLOR[1], INITIAL_DANGER_COLOR[2])
        guesses_left.set_text(guesses_left_text, new_color)
        guesses_left.set_animation(ANIMATION_SHAKE)

        button.change_color(RED_COLOR)
        button.change_alpha(WRONG_LETTER_ALPHA)
    
    

    if(check_solution(answer)):
        event_text_object.set_text(f"You won!", BLACK_COLOR)
        guesses_left = ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT]
        guesses_left.set_text("")
        game.set_state(STATE_GAME_WON)
        game_won(answer)

    elif wrong_guess_amount == max_wrong_guesses:
        event_text_object.set_text(f"Too many wrong guesses!", BLACK_COLOR)
        guesses_left = ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT]
        guesses_left.set_text("")
        game.set_state(STATE_SHOW_SOLUTION)
        solve_word(answer)
        
    fit_ui_text()


def fit_letter_buttons():
    global letter_buttons

    screen_size_x, screen_size_y = screen.get_size()

    letter_buttons[0].reset_size()
    letter_size = letter_buttons[0].get_surface().get_height()

    keyboard_layout_size_x = screen_size_x * 3/5
    keyboard_padding_x = screen_size_x * 1/5

    keyboard_layout_size_y = screen_size_y / 2
    keyboard_padding_y = keyboard_layout_size_y

    max_characters = len(string.ascii_uppercase)

    button_columns = int(keyboard_layout_size_x / letter_size)
    button_rows = int(keyboard_layout_size_y / letter_size)

    while button_columns * (button_rows - 1) > max_characters:
        button_columns -= 1
        if(max_characters / button_columns >= 4):
            break

    while button_columns * button_rows < max_characters:
        button_columns += 1

    index_x = 0
    index_y = 0

    max_button_distance_x = letter_size * 1.5
    max_button_distance_y = letter_size * 1.5
    
    for button in letter_buttons:
        letter_distance_x = keyboard_layout_size_x/(button_columns - 1) # no clue why button columns - 1 works nicely, i'll figure it out later
        letter_distance_y = keyboard_layout_size_y/button_rows
        if letter_distance_x >= max_button_distance_x:
            keyboard_padding_x = (screen_size_x - (max_button_distance_x * (button_columns - 1))) / 2 # no clue why button columns - 1 works nicely, i'll figure it out later
            
        x_location = (min(letter_distance_x, max_button_distance_x) * index_x) + keyboard_padding_x
        y_location = (min(letter_distance_y, max_button_distance_y) * index_y) + keyboard_padding_y

        button.reset_size()
        button_rect = button.get_surface().get_rect()
        button_rect.x = x_location
        button_rect.y = y_location
        button.set_rect(button_rect)
        button.set_rect_center((button_rect.x, button_rect.y))

        index_x += 1
        if index_x >= button_columns:
            index_x = 0
            index_y += 1


def fit_ui_text():
    global debug_text_rect, debug_timer_text_rect
    #Start menu ui text
    start_menu_layout_size_y = screen_size_y / 2
    start_menu_layout_padding_y = screen_size_y / 5

    menu_button_amount = len(ui_object_list[MENU_OBJECT])
    menu_order = 0
    
    for item in ui_object_list[MENU_OBJECT]:
        object = ui_object_list[MENU_OBJECT][item]
        object_rect = object.get_surface().get_rect()
        object_rect.x = screen_size_x / 2
        object_rect.y = align_ui_info(start_menu_layout_size_y, start_menu_layout_padding_y, menu_button_amount, menu_order)
        object.set_rect(object_rect)
        object.set_rect_center((object_rect.x, object_rect.y))
        object.update_surface()

        menu_order += 1

    #Playing state ui text

    #letter buttons order goes from bottom to top
    game_info_layout_size_y = screen_size_y / 3
    game_info_layout_padding_y = 15
    game_info_amount = 3

    info_order = 0

    event_text = ui_object_list[GAME_OBJECT][EVENT_TEXT]
    event_text.update_surface()
    event_text_rect = event_text.get_surface().get_rect()
    event_text_rect.x = screen_size_x / 2
    event_text_rect.y = align_ui_info(game_info_layout_size_y, game_info_layout_padding_y, game_info_amount, info_order)
    event_text.set_rect(event_text_rect)
    event_text.set_rect_center((event_text_rect.x, event_text_rect.y))
    
    info_order += 1
    
    guessed_letters = ui_object_list[GAME_OBJECT][GUESSED_LETTERS_TEXT]
    guessed_letters.update_surface()
    guessed_text_rect = guessed_letters.get_surface().get_rect()
    guessed_text_rect.x = screen_size_x / 2
    guessed_text_rect.y = align_ui_info(game_info_layout_size_y, game_info_layout_padding_y, game_info_amount, info_order)
    guessed_letters.set_rect(guessed_text_rect)
    guessed_letters.set_rect_center((guessed_text_rect.x, guessed_text_rect.y))

    info_order += 1
    
    solution_text = ui_object_list[GAME_OBJECT][SOLUTION_TEXT]
    solution_text.update_surface()
    solution_text_rect = solution_text.get_surface().get_rect()
    solution_text_rect.x = screen_size_x / 2
    solution_text_rect.y = align_ui_info(game_info_layout_size_y, game_info_layout_padding_y, game_info_amount, info_order)
    solution_text.set_rect(solution_text_rect)
    solution_text.set_rect_center((solution_text_rect.x, solution_text_rect.y))
    
    #end of layout

    back_button = ui_object_list[GAME_OBJECT][BACK_BUTTON] #Twice for GAME_OBJECT, probably needs changing later. Was easy solution
    back_button_rect = back_button.get_surface().get_rect()
    back_button_rect.topright = (screen_size_x - 30, 15)
    back_button.set_rect(back_button_rect)

    guesses_left = ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT]
    guesses_left_text_rect = guesses_left.get_surface().get_rect()
    guesses_left_text_rect.topleft = (5, 10)
    guesses_left.set_rect(guesses_left_text_rect)


    #Post game ui text

    back_button = ui_object_list[GAME_END_OBJECT][BACK_BUTTON] #Twice for GAME_END_OBJECT, probably needs changing later. Was easy solution
    back_button_rect = back_button.get_surface().get_rect()
    back_button_rect.topright = (screen_size_x - 30, 15)
    back_button.set_rect(back_button_rect)

    continue_text = ui_object_list[GAME_END_OBJECT][CONTINUE_TEXT]
    continue_text_rect = continue_text.get_rect()
    continue_text_rect.x = 5
    continue_text_rect.y = 10
    continue_text.set_rect(continue_text_rect)

    #debug text
    debug_text_rect = (0, screen_size_y - 15)
    debug_timer_text_rect.center = (screen_size_x - 10, screen_size_y - 15)

def align_ui_info(layout_size_y, layout_padding_y, info_amount, info_order):
    return (layout_size_y / info_amount) * (info_order + 1) + layout_padding_y


pygame.init()

INIT_SCREEN_WIDTH = 1024
INIT_SCREEN_HEIGHT = 768

RED_COLOR = (200, 50, 25)
GREEN_COLOR = (16, 200, 40)
DARK_GREEN_COLOR = (8, 130, 20)
DARK_BLUE_COLOR = (50, 50, 150)
LIGHT_BLUE_COLOR = (138, 160, 242)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

COLOR_MAX_VALUE = 255
WRONG_LETTER_ALPHA = 100

INITIAL_DANGER_COLOR = (0, 0, 0)

SOLVED_COLOR = GREEN_COLOR
UNSOLVED_COLOR = RED_COLOR

TEMP_COLOR_HOLDER = (174, 199, 245)

MENU_BACKGROUND_COLOR = TEMP_COLOR_HOLDER
GAME_BACKGROUND_COLOR = TEMP_COLOR_HOLDER


# Animation names

ANIMATION_CLICKED = "CLICKED"
ANIMATION_RESET = "RESET"
ANIMATION_SHAKE = "SHAKE"

# Animation frames

ANIMATION_CLICKED_FRAMES = 10
ANIMATION_LETTER_BUTTON_RESET_FRAMES = 10
ANIMATION_RESET_FRAMES = 30
ANIMATION_SHAKE_FRAMES = 10

# Animation scaling

ANIMATION_CLICKED_SCALE = 0.1
ANIMATION_LETTER_BUTTON_RESET_SCALE = 0.1
ANIMATION_RESET_SCALE = 0.2

# Animation shake

ANIMATION_SHAKE_STRENGTH = 2
ANIMATION_SHAKE_RANDOM = "RANDOM"



#Theme names
THEME_ALL = "all"
THEME_GAMING = "gaming"

theme_index = 0

theme_list = [THEME_ALL,
              THEME_GAMING]

#Difficulty names
DIFF_EASY = "easy"
DIFF_HARD = "hard"

difficulty_index = 0

difficulty_list = [DIFF_EASY,
              DIFF_HARD]

DEFAULT_BUTTON_FONT_SIZE = 50
DEFAULT_FONT_SIZE = 50

FONT_FILE_NAME = "MartianMono-VariableFont_wdth,wght.ttf"

#debug related
DEBUG_FONT = pygame.font.Font(FONT_FILE_NAME, 10)
DEBUG_TIMER_FONT = pygame.font.Font(FONT_FILE_NAME, 10)

# In game fonts
GUESS_FONT = pygame.font.Font(FONT_FILE_NAME, 30)
SOLUTION_FONT = pygame.font.Font(FONT_FILE_NAME, 40)
EVENT_FONT = pygame.font.Font(FONT_FILE_NAME, 20)
BUTTON_FONT = pygame.font.Font(FONT_FILE_NAME, DEFAULT_BUTTON_FONT_SIZE)
GUESSES_LEFT_FONT = pygame.font.Font(FONT_FILE_NAME, 25)

# Menu fonts
START_GAME_FONT = pygame.font.Font(FONT_FILE_NAME, 50)
SELECT_THEME_FONT = pygame.font.Font(FONT_FILE_NAME, 50)
SELECT_DIFFICULTY_THEME_FONT = pygame.font.Font(FONT_FILE_NAME, 50)
BACK_BUTTON_FONT = pygame.font.Font(FONT_FILE_NAME, 40)

# Post game fonts
CONTINUE_FONT = pygame.font.Font(FONT_FILE_NAME, 30)

screen = pygame.display.set_mode((INIT_SCREEN_WIDTH, INIT_SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.RESIZABLE)
screen_size_x, screen_size_y = screen.get_size()

# Initializing game variables

answer = ""
letter_buttons = []
solution_text = len(answer) * "_"
event_text = ""
event_text_surface = EVENT_FONT.render(event_text, True, BLACK_COLOR)
wrong_guess_amount = 0
max_wrong_guesses = 8

guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."

clock = pygame.time.Clock()

# Game states
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_SHOW_SOLUTION = "SHOW_SOLUTION"
STATE_GAME_WON = "GAME_WON"

game = Game()

# End of game related objects
GAME_END_OBJECT = "GAME_END_OBJECT"

CONTINUE_TEXT = "CONTINUE_TEXT"


# Game related objects
GAME_OBJECT = "GAME_OBJECT"
SOLUTION_TEXT = "SOLUTION_TEXT"
EVENT_TEXT = "EVENT_TEXT"
GUESSED_LETTERS_TEXT = "GUESSED_LETTERS_TEXT"
GUESSES_LEFT_TEXT = "GUESSES_LEFT_TEXT"

BACK_BUTTON = "BACK_BUTTON"

# Menu related objects
MENU_OBJECT = "MENU_OBJECT"

START_GAME_BUTTON = "START_GAME_BUTTON"
SELECT_THEME_BUTTON = "SELECT_THEME_BUTTON"
SELECT_DIFFICULTY_BUTTON = "SELECT_DIFFICULTY_BUTTON"

ui_object_list = {}

# Debug stuff

debug_mode = False
debug_text = ""
if debug_mode:
    debug_text = "debug text"
debug_text_surface = DEBUG_FONT.render(debug_text, True, BLACK_COLOR)
debug_text_rect = debug_text_surface.get_rect()
debug_text_rect = (0, screen_size_y - 15)

debug_timer_text = 0
debug_timer_text_surface = DEBUG_TIMER_FONT.render(str(debug_timer_text), True, BLACK_COLOR)
debug_timer_text_rect = debug_timer_text_surface.get_rect()
debug_timer_text_rect.center = (screen_size_x - 10, screen_size_y - 15)

DEBUG_TIMER = pygame.USEREVENT
timer = pygame.time.set_timer(DEBUG_TIMER, 1000)


async def main():
    global screen_size_x, screen_size_y, debug_text_surface, debug_text_rect, debug_timer_text_surface, debug_timer_text, object_list_index

    initialize_game()

    is_finger_lifted = True
    running =  True

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == DEBUG_TIMER:
                debug_timer_text += 1
                debug_timer_text_surface = DEBUG_FONT.render(str(debug_timer_text), True, BLACK_COLOR)

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                screen_size_x, screen_size_y = screen.get_size()
                fit_letter_buttons()
                fit_ui_text()
            
            if event.type == pygame.FINGERUP:
                is_finger_lifted = True
                for button in letter_buttons:
                    button.not_clicked()

            if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1: # 1 = left click
                        for button in letter_buttons:
                            button.not_clicked()

            if event.type == pygame.KEYUP:
                    for button in letter_buttons:
                        button.not_clicked()

            if(game.state == STATE_MENU): # Main menu
                object_list_index = MENU_OBJECT
                #Keyboard events
                if(event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_RETURN:
                        start_game()
                        game.set_state(STATE_PLAYING)
                        break

                #Mouse events
                elif(event.type == pygame.MOUSEBUTTONDOWN):
                    if event.button == 1: # 1 = left click
                        mouse_left_click_event(object_list_index)
                        break

                #Touch screen finger events
                elif(event.type == pygame.FINGERDOWN and is_finger_lifted):
                    finger_tap_event(event, object_list_index)
                    is_finger_lifted = False
                    break

            elif(game.state == STATE_PLAYING): # playing state
                object_list_index = GAME_OBJECT
                #Keyboard events
                if(event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_ESCAPE:
                        go_to_main_menu()
                        break
                    else:
                        for button in letter_buttons:
                            try:
                                if chr(event.key).upper() == button.letter:
                                    button.clicked()
                                else:
                                    button.not_clicked()
                            except:
                                break
                        break
                #Mouse events
                elif(event.type == pygame.MOUSEBUTTONDOWN):
                    if event.button == 1: # 1 = left click
                        mouse_pos = pygame.mouse.get_pos()
                        for button in letter_buttons:
                            button_rect = button.get_rect()
                            if button_rect.collidepoint(mouse_pos):
                                button.clicked()
                            else:
                                button.not_clicked()
                        mouse_left_click_event(object_list_index)
                        break
                            
                #Touch screen finger events
                elif(event.type == pygame.FINGERDOWN and is_finger_lifted):
                    finger_pos = (event.x * screen.get_height(), event.y * screen.get_width())
                    if button_rect.collidepoint(finger_pos):
                        button.clicked()
                    else:
                        button.not_clicked()
                    finger_tap_event(event, object_list_index)
                    is_finger_lifted = False
                    break

            elif(game.state == STATE_SHOW_SOLUTION or game.state == STATE_GAME_WON): #Game/round ended
                object_list_index = GAME_END_OBJECT
                #Keyboard events
                if(event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_RETURN:
                        new_round()
                        break
                    elif event.key == pygame.K_ESCAPE:
                        go_to_main_menu()
                        break

                #Mouse events
                elif(event.type == pygame.MOUSEBUTTONDOWN):
                    if event.button == 1: # 1 = left click
                        mouse_left_click_event(object_list_index)
                        break

                #Touch screen finger events
                elif(event.type == pygame.FINGERDOWN and is_finger_lifted):
                    finger_tap_event(event, object_list_index)
                    break
            


        game.update()
        if debug_mode:
            screen.blit(debug_text_surface, debug_text_rect)
            screen.blit(debug_timer_text_surface, debug_timer_text_rect)
        
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

def mouse_left_click_event(object_list_index):
    mouse_pos = pygame.mouse.get_pos()
    object_list = ui_object_list[object_list_index]
    for item in object_list:
        object = object_list[item]
        if object.get_rect().collidepoint(mouse_pos):
            if object.is_clickable():
                object.custom_function()
                return

def finger_tap_event(event, object_list_index):
    global debug_text_surface, screen
    finger_pos = (event.x * screen.get_height(), event.y * screen.get_width())
    
    object_list = ui_object_list[object_list_index]
    for item in object_list:
        object = object_list[item]
        if object.get_rect().collidepoint(finger_pos):
            if object.is_clickable():
                object.custom_function()
                return

asyncio.run(main())