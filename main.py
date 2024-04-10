import sys
from enum import Enum, auto

import pygame

import ptext.ptext as ptext
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
        OPTION_X_POS, OPTION_Y_POS, 40, OPTION_HEIGHT, label="Number of questions:", initial_value="10"
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
                else:
                    ptext.draw(
                        f"Incorrect!\nCorrect types are {helpers.list_as_string(pokemon_types)}",
                        midtop=(WIDTH // 2, 350),
                        width=int(WIDTH * 0.8),
                        fontsize=60,
                        color=WHITE,
                        background=BLACK,
                    )
                    pygame.display.flip()
                    pygame.time.wait(2000)
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


def pokedex_quiz(WIN, question_count=10, hints=True, generation=0):

    clock = pygame.time.Clock()

    inputbox_answer = InputBoxWithLabel(20, 300, 200, 40, label="Guess:", text_color=WHITE, always_active=True)
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

        pokemon_name = pokemon.name.replace("-", " ").lower()
        pokemon_types = helpers.pokemon_types(pokemon)
        pokedex_text = helpers.pokedex_text_entry(pokemon.id)

        question_number_field = FONT.render(f"{question+1} / {question_count}", True, WHITE, BACKGROUND_COLOR)
        if hints:
            # hint_text = f"Hint: {pokemon_name}"
            pokedex_text += f"\n\nTypes: {helpers.list_as_string(pokemon_types)}"
        while run:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    print("quit")
                    return False
                answer = inputbox_answer.handle_event(event)
                if answer:
                    break

            WIN.fill(BACKGROUND_COLOR)
            WIN.blit(question_number_field, (10, 10))

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

            ptext.draw(pokedex_text, midtop=(WIDTH // 2, 100), width=int(WIDTH * 0.8), fontsize=40, align="left")

            inputbox_answer.update_and_draw(WIN)
            guess_button.render(WIN)

            pygame.display.flip()

            if answer or guess_button.clicked(events):
                answer = answer if answer else inputbox_answer.get_value().lower()
                if answer == pokemon_name:
                    correct += 1
                else:
                    ptext.draw(
                        f"Incorrect!\nCorrect answer is {pokemon_name.title()}",
                        midtop=(WIDTH // 2, 350),
                        width=int(WIDTH * 0.8),
                        fontsize=60,
                        color=WHITE,
                        background=BLACK,
                    )
                    pygame.display.flip()
                    pygame.time.wait(1500)
                inputbox_answer.reset()
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
    game_state = GameState.MAIN_MENU
    # game_state = GameState.TYPE_QUIZ
    # game_state = GameState.POKEDEX_QUIZ

    while run:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                run = False

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         print("Paused!")
            #         game_paused = True
            #         pass

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
                    MENU_BUTTON_SIZE, "Pokédex Quiz", [MENU_BUTTON_POS_X, 110], center_text=True
                )
                button_pokedex_quiz.render(WIN)

                if button_type_quiz.clicked(events):
                    game_state = GameState.TYPE_QUIZ
                elif button_pokedex_quiz.clicked(events):
                    game_state = GameState.POKEDEX_QUIZ

            case GameState.TYPE_QUIZ:
                run = options_menu(WIN, type_quiz)
                game_state = GameState.MAIN_MENU
            case GameState.POKEDEX_QUIZ:
                run = options_menu(WIN, pokedex_quiz)
                game_state = GameState.MAIN_MENU
            case _:
                print(f"Unknown game state {game_state}")
                sys.exit(1)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
