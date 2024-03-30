import sys
from enum import Enum, auto

import pygame

from pokequiz import helpers
from pokequiz.constants import BACKGROUND_COLOR, FONT, GREEN, HEIGHT, RED, WHITE, WIDTH
from pokequiz.gui import Button, ButtonImage
from pokequiz.helpers import POKEMON_TYPES

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

        # input_box1 = InputBox(20, 400, 140, FONT_HEIGHT + 10, auto_active=True)

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

            # Score
            score_field = FONT.render(str(correct), True, WHITE, GREEN)
            score_field_rect = pygame.Rect(WIDTH - 100, 0, 100, score_field.get_height())
            pygame.draw.rect(WIN, pygame.Color("green"), score_field_rect)
            WIN.blit(score_field, (WIDTH - score_field.get_width() - 10, 0))

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

            # input_box1.update()
            # input_box1.draw(WIN)
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

    print(f"You got {correct} out of {question_count} ({round(100*correct/question_count)}%) correct!")
    return True


def main():
    run = True
    game_state = GameState.MAIN_MENU
    # game_state = GameState.TYPE_QUIZ

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
