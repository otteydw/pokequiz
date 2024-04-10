import sys
from enum import Enum, auto

import pygame

from pokequiz import helpers
from pokequiz.constants import (
    BACKGROUND_COLOR,
    BLACK,
    FONT,
    GREEN,
    HEIGHT,
    RED,
    WHITE,
    WIDTH,
)
from pokequiz.gui import Button, ButtonImage, InfoBox, InputBoxWithLabel
from pokequiz.helpers import POKEMON_TYPES, str2bool

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Poke Quiz")


class GameState(Enum):
    MAIN_MENU = auto()
    TYPE_QUIZ = auto()
    POKEDEX_QUIZ = auto()


def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    WIN.blit(img, (x, y))


def options_menu(WIN, quiz):
    run = True
    clock = pygame.time.Clock()

    OPTION_HEIGHT = 40
    OPTION_X_POS = 80
    OPTION_Y_POS = 40
    OPTION_Y_BUFFER = 5
    inputbox_number_of_questions = InputBoxWithLabel(
        OPTION_X_POS, OPTION_Y_POS, 40, OPTION_HEIGHT, label="Number of questions:", initial_value="100"
    )
    inputbox_hints = InputBoxWithLabel(
        OPTION_X_POS,
        OPTION_Y_POS + (OPTION_HEIGHT + OPTION_Y_BUFFER),
        40,
        OPTION_HEIGHT,
        label="Hints:",
        initial_value="True",
    )
    inputbox_generation = InputBoxWithLabel(
        OPTION_X_POS,
        OPTION_Y_POS + 2 * (OPTION_HEIGHT + OPTION_Y_BUFFER),
        40,
        OPTION_HEIGHT,
        label="Generation:",
        initial_value="0",
    )

    START_BUTTON_SIZE = (400, 50)
    START_BUTTON_POS_X = (WIDTH - START_BUTTON_SIZE[0]) // 2
    START_BUTTON_POS_Y = 4 * (OPTION_HEIGHT + 2 * OPTION_Y_BUFFER)
    button_start = Button(START_BUTTON_SIZE, "Start", [START_BUTTON_POS_X, START_BUTTON_POS_Y], center_text=True)

    while run:
        events = pygame.event.get()
        WIN.fill(BACKGROUND_COLOR)

        button_start.render(WIN)

        for event in events:
            if event.type == pygame.QUIT:
                return False
            inputbox_number_of_questions.handle_event(event)
            inputbox_hints.handle_event(event)
            inputbox_generation.handle_event(event)
            if button_start.clicked(events):
                question_count = int(inputbox_number_of_questions.get_value())
                hints = str2bool(inputbox_hints.get_value())
                generation = int(inputbox_generation.get_value())
                run = quiz(WIN, question_count=question_count, hints=hints, generation=generation)
        clock.tick(FPS)
        inputbox_number_of_questions.update_and_draw(WIN)
        inputbox_hints.update_and_draw(WIN)
        inputbox_generation.update_and_draw(WIN)
        pygame.display.flip()

    return True


def type_quiz(WIN, question_count=10, hints=True, generation=0):

    clock = pygame.time.Clock()

    BUTTON_WIDTH = 150
    BUTTON_HEIGHT = 40
    BUTTON_SIZE = (BUTTON_WIDTH, BUTTON_HEIGHT)
    BUTTON_X_BUFFER = 5
    BUTTON_Y_BUFFER = 5
    BUTTON_BEGINNING_X_POSITION = (WIDTH - (6 * BUTTON_WIDTH) - (5 * BUTTON_X_BUFFER)) / 2
    BUTTON_BEGINNING_Y_POSITION = 260
    type_buttons = []
    for type_num, pokemon_type in enumerate(POKEMON_TYPES.keys()):
        button_x = BUTTON_BEGINNING_X_POSITION + (BUTTON_WIDTH + BUTTON_X_BUFFER) * (type_num % 6)
        button_y = BUTTON_BEGINNING_Y_POSITION + (BUTTON_HEIGHT + BUTTON_Y_BUFFER) * (type_num // 6)
        button = ButtonImage(
            BUTTON_SIZE, pokemon_type.upper(), helpers.type_sprite(pokemon_type.lower()), (button_x, button_y)
        )
        type_buttons.append(button)

    guess_button = Button((400, 100), "Guess", [50, 480], bgColor=RED, textColor=WHITE, center_text=True)

    correct = 0
    previous_pokemon = set()
    pokemon = None
    for question in range(question_count):
        run = True
        while pokemon is None or pokemon.id in previous_pokemon:
            if generation == 0:
                pokemon = helpers.random_pokemon()
            else:
                pokemon = helpers.random_pokemon_from_generation(generation)
        previous_pokemon.add(pokemon.id)

        pokemon_name = pokemon.name.replace("-", " ").title()
        pokemon_types = helpers.pokemon_types(pokemon)

        pokemon_name_field = FONT.render(f"{question+1}: {pokemon_name}", True, WHITE, BACKGROUND_COLOR)
        if hints:
            # hint_text = f"Hint: {pokemon_types}"
            hint_text = f"Hint: it has {len(pokemon_types)} {helpers.simple_pluralize(pokemon_types, 'type','types')}."
            pokemon_hint_field = FONT.render(hint_text, True, WHITE, BACKGROUND_COLOR)

        POKEMON_IMAGE_WIDTH = 250
        POKEMON_IMAGE_HEIGHT = 250
        pokemon_image = pygame.image.load(helpers.pokemon_sprite(pokemon))
        pokemon_image = pygame.transform.scale(pokemon_image, (POKEMON_IMAGE_WIDTH, POKEMON_IMAGE_HEIGHT))

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

            SCORE_FIELD_WIDTH, SCORE_FIELD_HEIGHT = 120, 60
            score_field = InfoBox(
                size=(SCORE_FIELD_WIDTH, SCORE_FIELD_HEIGHT),
                text=str(correct),
                pos=(WIDTH - SCORE_FIELD_WIDTH, 0),
                textColor=WHITE,
                bgColor=GREEN,
                center_text=True,
            )
            score_field.render(WIN)

            POKEMON_IMAGE_X = (WIDTH - pokemon_image.get_width()) / 2
            POKEMON_IMAGE_Y = 15
            WIN.blit(pokemon_image, (POKEMON_IMAGE_X, POKEMON_IMAGE_Y))

            if hints:
                WIN.blit(pokemon_hint_field, (10, 400))

            for button in type_buttons:
                button.render(WIN)

            guess_button.render(WIN)

            for button in type_buttons:
                if button.clicked(events):
                    button.flip()

            pygame.display.flip()

            selected_types = [button.text.lower() for button in type_buttons if button.is_selected()]

            if guess_button.clicked(events):
                if selected_types == pokemon_types:
                    correct += 1
                for button in type_buttons:
                    button.deselect()
                    # button.render(WIN)
                # pygame.display.flip()
                run = False

            clock.tick(FPS)

    # Display score at the end
    popup = InfoBox(
        size=(int(WIDTH * 0.75), 40),
        text=f"You got {correct} / {question_count} correct! ({round(100*correct/question_count)}%)",
        pos=(int(WIDTH * 0.125), HEIGHT // 4),
        textColor=WHITE,
        bgColor=BLACK,
        center_text=True,
    )
    popup.render(WIN)
    pygame.display.flip()
    pygame.time.wait(5000)
    return True


def main():
    run = True
    # game_state = GameState.MAIN_MENU
    game_state = GameState.TYPE_QUIZ

    while run:
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

                # button_pokedex_rock = ButtonImage((100,20), "rock", helpers.type_sprite('rock'), [MENU_BUTTON_POS_X, 170])
                # button_pokedex_rock.render(WIN)

                if button_type_quiz.clicked(events):
                    print("Type Quiz")
                    game_state = GameState.TYPE_QUIZ

                if button_pokedex_quiz.clicked(events):
                    print("Pokedex Quiz")
                    game_state = GameState.POKEDEX_QUIZ
            case GameState.TYPE_QUIZ:
                # run = type_quiz(WIN)
                run = options_menu(WIN, type_quiz)
                game_state = GameState.MAIN_MENU
            case _:
                print("Unknown game state")
                print(game_state)
                sys.exit(1)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
