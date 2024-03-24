import sys
from enum import Enum, auto

import pygame

from pokequiz.constants import BACKGROUND_COLOR, BLACK, FONT, HEIGHT, WHITE, WIDTH
from pokequiz.helpers import POKEMON_TYPES

# FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poke Quiz")

COLOR_INACTIVE = pygame.Color("lightskyblue3")
COLOR_ACTIVE = pygame.Color("dodgerblue2")
# FONT = pygame.font.Font(pygame.font.get_default_font(), 32)


class GameState(Enum):
    MAIN_MENU = auto()
    TYPE_QUIZ = auto()
    POKEDEX_QUIZ = auto()


class Button:
    def __init__(self, size, text, pos, bgColor=WHITE, textColor=BLACK, center_text=False):
        self.pos = pos
        self.size = size
        self.text = text
        self.center_text = center_text
        self.bgColor = bgColor
        self.textColor = textColor
        # self.font = pygame.font.Font(pygame.font.get_default_font(), self.size[1])
        # self.textSurf = self.font.render(f"{self.text}", True, self.textColor)
        # self.button = pygame.Surface((self.size[0], self.size[1])).convert()
        # self.button.fill(self.bgColor)

    def render(self, window):
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.size[1])
        self.textSurf = self.font.render(f"{self.text}", True, self.textColor)
        self.button = pygame.Surface((self.size[0], self.size[1])).convert()
        self.button.fill(self.bgColor)

        window.blit(self.button, (self.pos[0], self.pos[1]))
        if self.center_text:
            text_width, _ = self.textSurf.get_size()
            text_position = (self.pos[0] + (self.size[0] - text_width) // 2, self.pos[1] + 5)
        else:
            text_position = (self.pos[0] + 1, self.pos[1] + 5)
        # window.blit(self.textSurf, (self.pos[0]+1, self.pos[1]+5))
        window.blit(self.textSurf, text_position)

    def clicked(self, events):
        mousePos = pygame.mouse.get_pos()  #  get the mouse position
        for event in events:
            if self.button.get_rect(topleft=self.pos).collidepoint(mousePos[0], mousePos[1]):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return True
        return False

    def flip(self):
        self.bgColor, self.textColor = self.textColor, self.bgColor


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    WIN.blit(img, (x, y))


class InputBox:

    def __init__(self, x, y, w, h, text=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


def type_quiz(WIN):
    run = True
    clock = pygame.time.Clock()

    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 20
    BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)
    BUTTON_X_BUFFER = 10
    BUTTON_Y_BUFFER = 20
    type_buttons = []
    for type_num, pokemon_type in enumerate(POKEMON_TYPES.keys()):
        button_x = 50 + (BUTTON_WIDTH + BUTTON_X_BUFFER) * (type_num % 6)
        button_y = 50 + (BUTTON_HEIGHT + BUTTON_Y_BUFFER) * (type_num // 6)
        button = Button(BUTTON_SIZE, pokemon_type.upper(), [button_x, button_y], center_text=True)
        type_buttons.append(button)

    while run:
        # clock.tick(FPS)

        WIN.fill(BACKGROUND_COLOR)

        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == "q":
                    run = False
            if event.type == pygame.QUIT:
                print("quit")
                run = False

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()

        for button in type_buttons:
            button.render(WIN)

        for button in type_buttons:
            if button.clicked(events):
                print(button.text.lower())
                button.flip()

        pygame.display.flip()
        clock.tick(30)


def main():
    run = True
    # game_state = GameState.MAIN_MENU
    game_state = GameState.TYPE_QUIZ

    # clock = pygame.time.Clock()

    while run:
        # clock.tick(FPS)
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # print("Paused!")
                    # game_paused = True
                    pass

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     pos = pygame.mouse.get_pos()

        WIN.fill(BACKGROUND_COLOR)

        match game_state:
            case GameState.MAIN_MENU:
                MENU_BUTTON_SIZE = (400, 50)
                MENU_BUTTON_POS_X = (WIDTH - MENU_BUTTON_SIZE[0]) // 2
                button_type_quiz = Button(MENU_BUTTON_SIZE, "Type Quiz", [MENU_BUTTON_POS_X, 50], center_text=True)
                button_type_quiz.render(WIN)

                button_pokedex_quiz = Button(
                    MENU_BUTTON_SIZE, "Pokedex Quiz", [MENU_BUTTON_POS_X, 110], center_text=True
                )
                button_pokedex_quiz.render(WIN)

                if button_type_quiz.clicked(events):
                    print("Type Quiz")
                    game_state = GameState.TYPE_QUIZ

                if button_pokedex_quiz.clicked(events):
                    print("Pokedex Quiz")
                    game_state = GameState.POKEDEX_QUIZ
            case GameState.TYPE_QUIZ:
                # draw_text("Press SPACE", FONT, TEXT_COLOR,160,250)
                type_quiz(WIN)
                game_state = GameState.MAIN_MENU
                # input_box1 = InputBox(100, 100, 140, 32)
                # input_box2 = InputBox(100, 300, 140, 32)
                # input_boxes = [input_box1, input_box2]

                # for event in events:
                #     for box in input_boxes:
                #         box.handle_event(event)
                # for box in input_boxes:
                #     box.update()
                # for box in input_boxes:
                #     box.draw(WIN)
                # pygame.display.flip()
            case _:
                print("Unknown game state")
                print(game_state)
                sys.exit(1)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
