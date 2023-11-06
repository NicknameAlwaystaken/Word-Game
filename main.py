# Simple pygame program


# Import and initialize the pygame library

import pygame
import string
import random
import asyncio
import math
import numpy as np


class Game:
    def __init__(self):
        self.__state = STATE_MENU
        self.__previous_state = None
        self.__background_color = MENU_BACKGROUND_COLOR
        self.__background_shapes = Background_Shapes_List()
        preload_list.append(lambda:self.create_background_shapes(SHAPE_STAR_AMOUNT))
    
    def create_background_shapes(self, amount):
        print("Generating stars")
        for i in range(amount):
            rand_x_position = random.randrange(0, screen_size_x)
            rand_y_position = random.randrange(0, screen_size_y)

            rand_r = random.randrange(50,200)
            rand_g = random.randrange(50,200)
            rand_b = random.randrange(50,200)
            color = (rand_r, rand_g, rand_b)

            background_star = Background_Shape(screen, SHAPE_STAR_NAME, rand_x_position ,rand_y_position, color)

            min_speed = 0.5
            max_speed = 2.0

            random_percentage = random.random()
            
            rand_x_speed = (((max_speed - min_speed) * random_percentage) + min_speed)
            rand_y_speed = (((max_speed - min_speed) * 1.0 - random_percentage) + min_speed) * -1

            background_star.set_move_speed(rand_x_speed, rand_y_speed)

            self.__background_shapes.add_item(background_star)


    def set_state(self, state):
        if state == STATE_RESUME:
            self.__state = self.__previous_state
        elif state == STATE_FROZEN:
            self.__previous_state = self.__state
            self.__state = state
        else:
            self.__state = state

        if self.__state == STATE_PLAYING or self.__state == STATE_SHOW_SOLUTION or self.__state == STATE_GAME_WON:
            self.__background_color = GAME_BACKGROUND_COLOR
        elif self.__state == STATE_MENU:
            self.__background_color = MENU_BACKGROUND_COLOR
        else:
            self.__background_color = WHITE_COLOR

    def get_state(self):
        return self.__state

    def __background(self):
        screen.fill(self.__background_color)
        self.__background_shapes.update()

    
    def update(self):
        if self.__state == STATE_FROZEN:
            return
        self.__background()
        if self.__state == STATE_PLAYING or self.__state == STATE_SHOW_SOLUTION or self.__state == STATE_GAME_WON:
            for button in letter_buttons:
                button.draw()

            for item in ui_object_list[GAME_OBJECT]:
                object = ui_object_list[GAME_OBJECT][item]
                object.draw()
            
            if self.__state == STATE_SHOW_SOLUTION or self.__state == STATE_GAME_WON:
                for item in ui_object_list[GAME_END_OBJECT]:
                    object = ui_object_list[GAME_END_OBJECT][item]
                    object.draw()

        elif self.__state == STATE_MENU:
            for item in ui_object_list[MENU_OBJECT]:
                object = ui_object_list[MENU_OBJECT][item]
                object.draw()

class Background_Shapes_List:
    def __init__(self):
        self.__list = []

    def __getitem__(self, index):
        return self.__list[index]

    def update(self):
        list = self.__list
        for item in list:
            item.update()

    def get_list(self):
        return self.__list
    
    def add_item(self, item):
        self.__list.append(item)

class Background_Shape(pygame.Surface):
    def __init__(self, parent, shape, x ,y, color = None):
        
        rand_x = random.random()
        rand_y = random.random()
        self.__direction = rand_x, rand_y
        self.__center_x = x
        self.__center_y = y
        self.__parent = parent
        self.__color = color

        self.__rotation_counter = 0
        self.__rotation_list = rotated_shapes[shape]

    def set_move_speed(self, x, y):
        self.__direction = x, y
        
    def update(self):

        if self.__rotation_list:

            # Moving center
            self.__center_x += self.__direction[0]
            self.__center_y += self.__direction[1]

            if(self.__center_x < -50):
                self.__center_x = screen_size_x + 45
            elif self.__center_x > screen_size_x + 50:
                self.__center_x = -45
                
            if(self.__center_y < -50):
                self.__center_y = screen_size_y + 45
            elif self.__center_y > screen_size_y + 50:
                self.__center_y = -45



            # Rotation
            current_rotation = self.__rotation_counter

            new_surface = self.__rotation_list[current_rotation]
            new_surface_rect = new_surface.get_rect()
            new_surface_rect.center = self.__center_x, self.__center_y

            self.__rotation_counter += 1
            if self.__rotation_counter >= len(self.__rotation_list):
                self.__rotation_counter = 0

            self.__parent.blit(new_surface, new_surface_rect)
        
    
    def get_rect(self) -> pygame.Rect:
        return self.__rect

class Button:
    def __init__(self, surface, custom_function = None, clickable: bool = False) -> None:

        self.__surface = pygame.Surface.copy(surface)
        self.__rect = self.__surface.get_rect()
        self.__clickable = clickable
        self.__custom_function = custom_function
        self.__is_selected = False
        self.__selectable = True

        self.__animation_step = 0
        self.__is_animating = False
        self.__animation = "NONE"

    def get_rect(self):
        return self.__rect
    
    def get_rect_center(self):
        return self.__rect.center
    
    def set_rect(self, rect):
        self.__rect = rect
        
    def set_rect_center(self, rect):
        self.__rect.center = rect
    
    def get_surface(self):
        return self.__surface
    
    def is_clickable(self):
        return self.__clickable
    
    def custom_function(self):
        self.__custom_function()
        
    def clicked(self):
        if self.__clickable and self.__custom_function != None:
            self.__custom_function()
    
    def draw(self):
        if self.__is_animating:
            if self.__animation == ANIMATION_SELECTED:
                selected_animation(self, ANIMATION_SELECTED_SCALE, ANIMATION_SELECTED_FRAMES, self.__is_selected)

        else:
            screen.blit(self.__surface, self.__rect)
        
    def set_animation(self, animation):
        self.__animation = animation
        self.__is_animating = True
        
    def set_animation_step(self, step):
        self.__animation_step = step
        
    def get_animation_step(self):
        return self.__animation_step
        
    def stop_animation(self):
        self.__is_animating = False

    def select(self, selected):
        if self.__selectable:
            self.__is_selected = selected
            if selected:
                self.set_animation(ANIMATION_SELECTED)

    def set_image(self, image):
        self.__surface = image
                
    def update_surface(self): # Delete when can
        pass

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
        
        self.__is_selected = False
        self.__selectable = False


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
            if self.__animation == ANIMATION_POPOUT:
                scaling_up = True
                scale_animation(self, ANIMATION_POPOUT_SCALE, ANIMATION_POPOUT_FRAMES, scaling_up)

            if self.__animation == ANIMATION_SHORT_POPOUT:
                scaling_up = True
                scale_animation(self, ANIMATION_SHORT_POPOUT_SCALE, ANIMATION_SHORT_POPOUT_FRAMES, scaling_up)

            if self.__animation == ANIMATION_SHAKE:
                style = ANIMATION_SHAKE_RANDOM
                shake_animation(self, ANIMATION_SHAKE_STRENGTH, ANIMATION_SHAKE_FRAMES, style)
                
            if self.__animation == ANIMATION_SELECTED:
                selected_animation(self, ANIMATION_SELECTED_SCALE, ANIMATION_SELECTED_FRAMES, self.__is_selected)

        else:
            if not self.__hidden:
                screen.blit(self.__surface, (self.__rect.x, self.__rect.y))
                
    
    def custom_function(self):
        self.__custom_function()
        
    def select(self, selected):
        if self.__selectable:
            self.__is_selected = selected
            if selected:
                self.set_animation(ANIMATION_SELECTED)

class Letter_Button():

    def __init__(self, x, y, letter):
        self.__font = BUTTON_FONT
        self.__original_image = letter_button_fitted_image
        self.__surface = pygame.Surface.copy(self.__original_image)
        self.__x_center = x
        self.__y_center = y
        self.__rect = self.__surface.get_rect()
        self.__rect.center = (self.__x_center, self.__y_center)
        self.letter = letter
        self.is_clicked = False
        self.correct_letter = None
        self.__color = BLACK_COLOR

        self.__selectable = True
        self.__is_selected = False

        self.__animation_step = 0
        self.__is_animating = False
        self.__animation = "NONE"

        self.__is_changed = False # Flag to reduce rendering when nothing changed

    def change_color(self, color):
        self.__color = color
        self.__is_changed = True

    def change_alpha(self, alpha):
        self.__alpha = alpha
        self.__is_changed = True

    
    def draw(self):
        if self.__is_animating or self.__is_changed:
            self.__surface = pygame.Surface.copy(self.__original_image)
            self.__rect = self.__surface.get_rect()
            self.__rect.center = (self.__x_center, self.__y_center)
            font_surface = self.__font.render(self.letter, True, self.__color)
            self.__surface.blit(font_surface, (15, 0)) # fix math here
            self.__surface.set_alpha(self.__alpha)

            self.__is_changed = False

        if self.is_clicked:
            self.__is_animating = True
            self.__animation = ANIMATION_CLICKED
            if self.__animation_step == -1:
                self.__animation_step = 0

        if self.__is_animating:
            if self.__animation == ANIMATION_CLICKED:
                scaling_up = False
                scale_animation(self, ANIMATION_CLICKED_SCALE, ANIMATION_CLICKED_FRAMES, scaling_up)

            elif self.__animation == ANIMATION_LETTER_POPOUT:
                scaling_up = True
                scale_animation(self, ANIMATION_LETTER_BUTTON_RESET_SCALE, ANIMATION_LETTER_BUTTON_RESET_FRAMES, scaling_up)

            elif self.__animation == ANIMATION_SELECTED:
                selected_animation(self, ANIMATION_SELECTED_SCALE, ANIMATION_SELECTED_FRAMES, self.__is_selected)
        else:
            screen.blit(self.__surface, self.__rect)
    
    def clicked(self):
        self.is_clicked = True
        check_letter(self.letter, self)
        self.__selectable = False
    
    def not_clicked(self):
        self.is_clicked = False
        
    def set_animation(self, animation):
        if animation == ANIMATION_SELECTED and not self.__is_animating or animation is not ANIMATION_SELECTED: # I don't want hover animation change ongoing animation
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
        self.__rect = self.__surface.get_rect()

    def get_rect(self):
        return self.__rect
    
    def get_surface(self):
        return self.__surface
    
    def get_animation_step(self):
        return self.__animation_step
    
    def set_animation_step(self, step):
        self.__animation_step = step

    def select(self, selected):
        if self.__selectable:
            self.__is_selected = selected
            if selected:
                self.set_animation(ANIMATION_SELECTED)

    def set_selectable(self, selectable):
        self.__selectable = selectable


def render_rotation_images(image, rotation_angle, color = None):
    rotation_amount = math.floor(360 / rotation_angle + 0.5)
    new_rotation_angle = 360 / rotation_amount
    rotated_images = []
    
    for i in range(rotation_amount):

        # Rotation
        new_surface = pygame.transform.rotozoom(image, new_rotation_angle * i, 1.0)

        # Coloring
        if color: # Borrowed code https://stackoverflow.com/questions/42821442/how-do-i-change-the-colour-of-an-image-in-pygame-without-changing-its-transparen
            w, h = new_surface.get_size()
            r, g, b = color
            for x in range(w):
                for y in range(h):
                    a = new_surface.get_at((x, y))[3]
                    new_surface.set_at((x, y), pygame.Color(r, g, b, a))

        rotated_images.append(new_surface)

    return rotated_images
    
def shake_animation(self, strength, animation_frames, style):
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

def scale_animation(self, max_scale, animation_frames, scaling_up):
    current_step = self.get_animation_step()
    half_steps = int(animation_frames / 2)

    current_scale = max_scale / half_steps * current_step

    surface = self.get_surface()

    if current_step >= half_steps and current_scale >= max_scale:
        current_scale = max(max_scale - (current_scale - max_scale), 0)
    if not scaling_up:
        new_surface = pygame.transform.smoothscale_by(surface, 1.0 - current_scale)
    if scaling_up:
        new_surface = pygame.transform.smoothscale_by(surface, 1.0 + current_scale)
    new_rect = new_surface.get_rect()
    new_rect.center = self.get_rect_center()
    screen.blit(new_surface, new_rect)

    self.set_animation_step(current_step + 1)
    if current_step + 1 > animation_frames:
        self.set_animation_step(-1)
        self.stop_animation()
        
def selected_animation(self, max_scale, animation_frames, selected):
    current_step = self.get_animation_step()
    
    current_scale = max_scale / animation_frames * current_step

    surface = self.get_surface()

    new_surface = pygame.transform.smoothscale_by(surface, 1.0 + current_scale)

    new_rect = new_surface.get_rect()
    new_rect.center = self.get_rect_center()
    screen.blit(new_surface, new_rect)
    
    if selected and current_step + 1 <= animation_frames:
        self.set_animation_step(current_step + 1)
    elif not selected and current_step - 1 > -1:
        self.set_animation_step(current_step - 1)

    if not selected and current_step - 1 <= 0:
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
    file_name = theme_list[theme_index] + "wordlist.txt"
    with open(file_name, "r") as openfile:
        for line in openfile:
            word = line.rstrip()
            list_of_answers.append(word)

def get_new_word():
    global list_of_answers
    random_int = random.randrange(0, len(list_of_answers))
    return list_of_answers[random_int]

def go_to_main_menu():
    pygame.mixer.Sound.play(back_sound)
    game.set_state(STATE_MENU)

def cycle_themes():
    pygame.mixer.Sound.play(change_setting_sound)
    global theme_list, theme_index
    theme_index += 1
    if theme_index >= len(theme_list):
        theme_index = 0
    
    ui_object_list[MENU_OBJECT][SELECT_THEME_BUTTON].set_image(theme_image_list[theme_list[theme_index]])
    fit_ui_text()

def new_round():
    pygame.mixer.Sound.play(start_game_sound)
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

    solution_text = ui_object_list[GAME_OBJECT][SOLUTION_TEXT]
    solution_text.set_animation(ANIMATION_SHORT_POPOUT)

def loading_screen():
    center = screen_size_x / 2, screen_size_y / 2
    loading_text = LOADING_TEXT_FONT.render("Loading...", True, (BLACK_COLOR))
    loading_text_rect = loading_text.get_rect()
    loading_text_rect.center = center
    screen.fill(MENU_BACKGROUND_COLOR)
    screen.blit(loading_text, loading_text_rect)
    pygame.display.update()
    print(game.get_state())
    game.set_state(STATE_FROZEN)
    print(game.get_state())
    for function in preload_list:
        function()
    game.set_state(STATE_RESUME)
    print(game.get_state())

def start_game():
    pygame.mixer.Sound.play(start_game_sound)
    reset_game()
    game.set_state(STATE_PLAYING)

def init_ui_text(ui_object_list):
    empty_string = ""
    
    #Main menu ui text
    ui_object_list[MENU_OBJECT] = {}

    # Menu items
    ui_object_list[MENU_OBJECT][START_GAME_BUTTON] = Button(start_game_button_fitted_image, start_game, True)

    ui_object_list[MENU_OBJECT][SELECT_THEME_BUTTON] = Button(all_button_fitted_image, cycle_themes, True)

    theme_text = f"Theme:"
    ui_object_list[MENU_OBJECT][THEME_TEXT] = Interactive_Text(theme_text, BLACK_COLOR, THEME_FONT)
    
    
    

    #Playing state ui text
    ui_object_list[GAME_OBJECT] = {}

    # Items are ontop of each other

    ui_object_list[GAME_OBJECT][SOLUTION_TEXT] = Interactive_Text(solution_text, BLACK_COLOR, SOLUTION_FONT)

    event_text = ""
    ui_object_list[GAME_OBJECT][EVENT_TEXT] = Interactive_Text(event_text, BLACK_COLOR, EVENT_FONT)
    
    ui_object_list[GAME_OBJECT][GUESSED_LETTERS_TEXT] = Interactive_Text(empty_string, BLACK_COLOR, GUESS_FONT)
    
    # Other items

    ui_object_list[GAME_OBJECT][BACK_BUTTON] = Button(back_button_fitted_image, go_to_main_menu, True)

    guesses_left_text = f"You have {max_wrong_guesses-wrong_guess_amount} wrong guesses left."
    new_color = (((COLOR_MAX_VALUE - INITIAL_DANGER_COLOR[0] / max_wrong_guesses) * wrong_guess_amount), INITIAL_DANGER_COLOR[1], INITIAL_DANGER_COLOR[2])
    ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT] = Interactive_Text(guesses_left_text, new_color, GUESSES_LEFT_FONT)

    #Post game ui items
    ui_object_list[GAME_END_OBJECT] = {}
    
    ui_object_list[GAME_END_OBJECT][BACK_BUTTON] = ui_object_list[GAME_OBJECT][BACK_BUTTON] # Currently adding back button to two lists for use between 2 game states

    ui_object_list[GAME_END_OBJECT][CONTINUE_TEXT] = Button(continue_button_loaded_image, new_round, True)

    fit_ui_text()


def reset_buttons():
    global letter_buttons
    for button in letter_buttons:
        button.change_color(BLACK_COLOR)
        button.change_alpha(COLOR_MAX_VALUE)
        button.set_selectable(True)

def game_won(answer):
    global guesses_left_text_surface

    guesses_left_text = f""
    ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT].set_text(guesses_left_text)

    ui_object_list[GAME_OBJECT][SOLUTION_TEXT].set_text(answer, SOLVED_COLOR)
    ui_object_list[GAME_OBJECT][SOLUTION_TEXT].set_animation(ANIMATION_POPOUT)

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
        pygame.mixer.Sound.play(correct_sound)
        event_text_object.set_text(f"Correct!", GREEN_COLOR)
        button.change_color(GREEN_COLOR)
        button.change_alpha(COLOR_MAX_VALUE)

    elif letter_guessed not in answer.upper():
        pygame.mixer.Sound.play(wrong_sound)
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
        pygame.mixer.Sound.play(correct_word_sound)
        event_text_object.set_text(f"You won!", BLACK_COLOR)
        guesses_left = ui_object_list[GAME_OBJECT][GUESSES_LEFT_TEXT]
        guesses_left.set_text("")
        game.set_state(STATE_GAME_WON)
        game_won(answer)

    elif wrong_guess_amount == max_wrong_guesses:
        pygame.mixer.Sound.play(failed_word_sound)
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
    
    object = ui_object_list[MENU_OBJECT][START_GAME_BUTTON]
    object_rect = object.get_surface().get_rect()
    object_rect.x = screen_size_x / 2
    object_rect.y = align_ui_info(start_menu_layout_size_y, start_menu_layout_padding_y, menu_button_amount, menu_order)
    object.set_rect(object_rect)
    object.set_rect_center((object_rect.x, object_rect.y))
    object.update_surface()

    menu_order += 2
    
    # Theme: with theme and difficulty buttons

    theme_padding = 0
    center = screen_size_x / 2

    object_width_list = [ui_object_list[MENU_OBJECT][THEME_TEXT].get_surface().get_rect().width,
        ui_object_list[MENU_OBJECT][SELECT_THEME_BUTTON].get_surface().get_rect().width]

    object = ui_object_list[MENU_OBJECT][THEME_TEXT]
    object_rect = object.get_surface().get_rect()
    object_rect.x = center - (sum(object_width_list) / 3)
    object_rect.y = align_ui_info(start_menu_layout_size_y, start_menu_layout_padding_y, menu_button_amount, menu_order)
    object.set_rect(object_rect)
    object.set_rect_center((object_rect.x, object_rect.y))
    object.update_surface()
    
    object = ui_object_list[MENU_OBJECT][SELECT_THEME_BUTTON]
    object_rect = object.get_surface().get_rect()
    object_rect.x = center + (sum(object_width_list) / 3)
    object_rect.y = align_ui_info(start_menu_layout_size_y, start_menu_layout_padding_y, menu_button_amount, menu_order)
    object.set_rect(object_rect)
    object.set_rect_center((object_rect.x, object_rect.y))
    object.update_surface()

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

    continue_text = ui_object_list[GAME_END_OBJECT][CONTINUE_TEXT]
    continue_text_rect = continue_text.get_rect()
    continue_text_rect.x = 30
    continue_text_rect.y = 15
    continue_text.set_rect(continue_text_rect)

    #debug text
    debug_text_rect = (0, screen_size_y - 15)
    debug_timer_text_rect.center = (screen_size_x - 10, screen_size_y - 15)

def align_ui_info(layout_size_y, layout_padding_y, info_amount, info_order):
    return (layout_size_y / info_amount) * (info_order + 1) + layout_padding_y



async def main():
    global screen_size_x, screen_size_y, debug_text_surface, debug_text_rect, debug_timer_text_surface, debug_timer_text, object_list_index

    loading_screen()
    initialize_game()

    is_finger_lifted = True
    running =  True

    while running:
        events = pygame.event.get()
        for event in events:
            mouse_pos = pygame.mouse.get_pos()
            if event.type == DEBUG_TIMER and debug_mode:
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

            # Main menu
            if(game.get_state() == STATE_MENU): 
                object_list_index = MENU_OBJECT
                
                # Hover over
                object_list = ui_object_list[object_list_index]
                for item in object_list:
                    object = object_list[item]
                    if object.get_rect().collidepoint(mouse_pos):
                        object.select(True)
                    else:
                        object.select(False)
                        
                for button in letter_buttons:
                    if button.get_rect().collidepoint(mouse_pos):
                        button.select(True)
                    else:
                        button.select(False)

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
            
            # playing state
            elif(game.get_state() == STATE_PLAYING): 
                object_list_index = GAME_OBJECT
                
                # Hover over
                object_list = ui_object_list[object_list_index]
                for item in object_list:
                    object = object_list[item]
                    if object.get_rect().collidepoint(mouse_pos):
                        object.select(True)
                    else:
                        object.select(False)
                        
                for button in letter_buttons:
                    if button.get_rect().collidepoint(mouse_pos):
                        button.select(True)
                    else:
                        button.select(False)
                
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

            #Game/round ended
            elif(game.get_state() == STATE_SHOW_SOLUTION or game.get_state() == STATE_GAME_WON): 
                object_list_index = GAME_END_OBJECT
                
                # Hover over
                object_list = ui_object_list[object_list_index]
                for item in object_list:
                    object = object_list[item]
                    if object.get_rect().collidepoint(mouse_pos):
                        object.select(True)
                    else:
                        object.select(False)

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

        clock.tick(TICK_SPEED)

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


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    preload_list = []

    INIT_SCREEN_WIDTH = 1024
    INIT_SCREEN_HEIGHT = 768

    screen = pygame.display.set_mode((INIT_SCREEN_WIDTH, INIT_SCREEN_HEIGHT), pygame.DOUBLEBUF | pygame.RESIZABLE)
    screen_size_x, screen_size_y = screen.get_size()

    # Game states
    STATE_FROZEN = "FROZEN"
    STATE_RESUME = "RESUME"
    STATE_MENU = "MENU"
    STATE_PLAYING = "PLAYING"
    STATE_SHOW_SOLUTION = "SHOW_SOLUTION"
    STATE_GAME_WON = "GAME_WON"
    


    RED_COLOR = (200, 50, 25)
    GREEN_COLOR = (16, 140, 40)
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

    DARKER_MENU_BACKGROUND_COLOR = (127,159,219)

    
    # Images for shapes

    white_star_image = pygame.image.load("white_star.png").convert_alpha()
    white_star_fitted_image = pygame.transform.smoothscale(white_star_image, (50, 50))

    # Shape variables

    SHAPE_STAR_NAME = "STAR"
    SHAPE_STAR_AMOUNT = 20

    rotated_shapes = {}
    rotated_shapes[SHAPE_STAR_NAME] = render_rotation_images(white_star_fitted_image, 1.5, DARKER_MENU_BACKGROUND_COLOR)

    # Game sounds

    start_game_sound = pygame.mixer.Sound("start_game_sound.ogg")
    correct_sound = pygame.mixer.Sound("correct_sound.ogg")
    failed_word_sound = pygame.mixer.Sound("failed_word_sound.ogg")
    correct_word_sound = pygame.mixer.Sound("correct_word_sound.ogg")
    wrong_sound = pygame.mixer.Sound("wrong_sound.ogg")
    back_sound = pygame.mixer.Sound("back_sound.ogg")
    change_setting_sound = pygame.mixer.Sound("change_setting_sound.ogg")

    game = Game()



    # Animation names

    ANIMATION_CLICKED = "CLICKED"
    ANIMATION_POPOUT = "POPOUT"
    ANIMATION_SHORT_POPOUT = "SHORT_POPOUT"
    ANIMATION_LETTER_POPOUT = "LETTER_POPOUT"
    ANIMATION_SHAKE = "SHAKE"
    ANIMATION_SELECTED = "HOVER"


    TICK_SPEED = 60

    # Animation frames

    ANIMATION_CLICKED_FRAMES = TICK_SPEED / 6
    ANIMATION_LETTER_BUTTON_RESET_FRAMES = TICK_SPEED / 6
    ANIMATION_POPOUT_FRAMES = TICK_SPEED / 2
    ANIMATION_SHORT_POPOUT_FRAMES = TICK_SPEED / 6
    ANIMATION_SHAKE_FRAMES = TICK_SPEED / 6
    ANIMATION_SELECTED_FRAMES = TICK_SPEED / 6

    # Animation scaling

    ANIMATION_CLICKED_SCALE = 0.1
    ANIMATION_LETTER_BUTTON_RESET_SCALE = 0.1
    ANIMATION_POPOUT_SCALE = 0.2
    ANIMATION_SHORT_POPOUT_SCALE = 0.1
    ANIMATION_SELECTED_SCALE = 0.1

    # Animation shake

    ANIMATION_SHAKE_STRENGTH = 2
    ANIMATION_SHAKE_RANDOM = "RANDOM"



    #Theme names
    THEME_ALL = "all"
    THEME_GAMING = "gaming"

    theme_index = 0

    theme_list = [THEME_ALL,
                THEME_GAMING]


    DEFAULT_BUTTON_FONT_SIZE = 60
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
    THEME_FONT = pygame.font.Font(FONT_FILE_NAME, 50)
    SELECT_THEME_FONT = pygame.font.Font(FONT_FILE_NAME, 50)
    SELECT_DIFFICULTY_THEME_FONT = pygame.font.Font(FONT_FILE_NAME, 50)
    BACK_BUTTON_FONT = pygame.font.Font(FONT_FILE_NAME, 40)

    # Loading screen font

    LOADING_TEXT_FONT = pygame.font.Font(FONT_FILE_NAME, 60)

    # Post game fonts
    CONTINUE_FONT = pygame.font.Font(FONT_FILE_NAME, 30)


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
    THEME_TEXT = "THEME_TEXT"
    SELECT_THEME_BUTTON = "SELECT_THEME_BUTTON"

    # Images for buttons

    letter_button_loaded_image = pygame.image.load("letter_button_background.png").convert_alpha()
    letter_button_fitted_image = pygame.transform.smoothscale(letter_button_loaded_image, (75, 75))

    back_button_loaded_image = pygame.image.load("back_button.png").convert_alpha()
    back_button_fitted_image = back_button_loaded_image #pygame.transform.smoothscale(back_button_loaded_image, (75, 75))

    continue_button_loaded_image = pygame.image.load("continue_button.png").convert_alpha()
    continue_button_fitted_image = continue_button_loaded_image #pygame.transform.smoothscale(continue_button_loaded_image, (75, 75))

    start_game_button_loaded_image = pygame.image.load("start_game_button.png").convert_alpha()
    start_game_button_fitted_image = start_game_button_loaded_image #pygame.transform.smoothscale(start_game_button_loaded_image, (75, 75))

    easy_button_loaded_image = pygame.image.load("easy_button.png").convert_alpha()
    easy_button_fitted_image = easy_button_loaded_image #pygame.transform.smoothscale(easy_button_loaded_image, (75, 75))

    hard_button_loaded_image = pygame.image.load("hard_button.png").convert_alpha()
    hard_button_fitted_image = hard_button_loaded_image #pygame.transform.smoothscale(hard_button_loaded_image, (75, 75))
    
    gaming_button_loaded_image = pygame.image.load("gaming_button.png").convert_alpha()
    gaming_button_fitted_image = gaming_button_loaded_image #pygame.transform.smoothscale(gaming_button_loaded_image, (75, 75))

    all_button_loaded_image = pygame.image.load("all_button.png").convert_alpha()
    all_button_fitted_image = all_button_loaded_image #pygame.transform.smoothscale(all_button_loaded_image, (75, 75))

    ui_object_list = {}

    
    #Theme names
    THEME_ALL = "all"
    THEME_GAMING = "gaming"

    theme_index = 0

    theme_list = [THEME_ALL,
                THEME_GAMING]

    theme_image_list = {"all" : all_button_fitted_image, "gaming" : gaming_button_fitted_image}

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

    # Performance enhancer
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.USEREVENT, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP,
                              pygame.FINGERDOWN, pygame.VIDEORESIZE, pygame.KEYUP, pygame.FINGERUP])

    asyncio.run(main())