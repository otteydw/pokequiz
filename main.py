import sys
from enum import Enum, auto

import pygame

from pokequiz import helpers
from pokequiz.constants import BACKGROUND_COLOR, FONT, HEIGHT, WHITE, WIDTH
from pokequiz.gui import Button
from pokequiz.helpers import POKEMON_TYPES

# FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poke Quiz")


class GameState(Enum):
    MAIN_MENU = auto()
    TYPE_QUIZ = auto()
    POKEDEX_QUIZ = auto()


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    WIN.blit(img, (x, y))


def type_quiz(WIN, question_count=2, hints=False, generation=0):

    clock = pygame.time.Clock()

    BUTTON_WIDTH = 100
    BUTTON_HEIGHT = 20
    BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)
    BUTTON_X_BUFFER = 10
    BUTTON_Y_BUFFER = 20
    type_buttons = []
    for type_num, pokemon_type in enumerate(POKEMON_TYPES.keys()):
        button_x = 50 + (BUTTON_WIDTH + BUTTON_X_BUFFER) * (type_num % 6)
        button_y = 100 + (BUTTON_HEIGHT + BUTTON_Y_BUFFER) * (type_num // 6)
        button = Button(BUTTON_SIZE, pokemon_type.upper(), [button_x, button_y], center_text=True)
        type_buttons.append(button)

    guess_button = Button(
        (400, 100), "Guess", [50, 300], bgColor=pygame.Color("red"), textColor=WHITE, center_text=True
    )

    correct = 0
    previous_pokemon = set()
    pokemon = None
    for _ in range(question_count):
        run = True
        while pokemon is None or pokemon.id in previous_pokemon:
            if generation == 0:
                pokemon = helpers.random_pokemon()
            else:
                pokemon = helpers.random_pokemon_from_generation(generation)
        previous_pokemon.add(pokemon.id)

        pokemon_name = pokemon.name.replace("-", " ").title()
        print(pokemon_name)  # DEBUG
        pokemon_types = helpers.pokemon_types(pokemon)

        pokemon_name_field = FONT.render(f"{pokemon_name}: {pokemon_types}", True, WHITE, BACKGROUND_COLOR)

        # input_box1 = InputBox(20, 400, 140, FONT_HEIGHT + 10, auto_active=True)

        while run:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    print("quit")
                    return False
                    # run = False

                # answer = input_box1.handle_event(event)
                # if answer:
                #     print(f"Answer was {answer}")
                #     if answer.lower() == pokemon_name.lower():
                #         print("Winner!")
                #         correct += 1

            WIN.fill(BACKGROUND_COLOR)
            WIN.blit(pokemon_name_field, (10, 10))

            for button in type_buttons:
                button.render(WIN)

            guess_button.render(WIN)

            for button in type_buttons:
                if button.clicked(events):
                    # print(button.text.lower())
                    button.flip()

            # input_box1.update()
            # input_box1.draw(WIN)
            pygame.display.flip()

            selected_types = [button.text.lower() for button in type_buttons if button.is_selected()]

            if guess_button.clicked(events):
                if selected_types == pokemon_types:
                    print("Correct!")
                    correct += 1
                    for button in type_buttons:
                        button.deselect()
                        # button.render(WIN)
                    # pygame.display.flip()
                    run = False

            clock.tick(30)

    return True


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
                run = type_quiz(WIN)
                game_state = GameState.MAIN_MENU
            case _:
                print("Unknown game state")
                print(game_state)
                sys.exit(1)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
