import sys

from rich import print
from rich.prompt import Confirm, IntPrompt, Prompt

from pokequiz import helpers


def type_quiz(question_count=10, hints=False, generation=0):
    correct = 0

    previous_pokemon = set()
    pokemon = None
    for _ in range(question_count):
        while pokemon is None or pokemon.id in previous_pokemon:
            if generation == 0:
                pokemon = helpers.random_pokemon()
            else:
                pokemon = helpers.random_pokemon_from_generation(generation)
        previous_pokemon.add(pokemon.id)

        pokemon_name = pokemon.name.replace("-", " ").title()
        pokemon_types = helpers.pokemon_types(pokemon)
        print()
        helpers.display_list_in_4_columns(helpers.pokemon_type_list_with_emoji())
        print()
        if hints:
            hint_text = f"Hint: it has {len(pokemon_types)} {helpers.simple_pluralize(pokemon_types, 'type','types')}."
        else:
            hint_text = ""

        valid_guess = False
        while not valid_guess:
            print(f"What are the typings for [bold]{pokemon_name}[/bold]? {hint_text}")
            guess = Prompt.ask("Answer")
            guess_list = helpers.format_guess_as_list(guess)
            if helpers.check_valid_pokemon_types(guess_list):
                valid_guess = True
            else:
                print("[red]Invalid type specified. Please try again.[/red]\n")

        if guess_list == pokemon_types:
            print("[green]Correct![/green]")
            correct += 1
        else:
            print(
                f"[red]Wrong![/red] {pokemon_name} has {helpers.simple_pluralize(pokemon_types, 'typing','typings')} of [bold]{helpers.combine_words(pokemon_types)}[/bold]."
            )
        print()

    print("Done!")
    print(f"You got {correct} out of {question_count} ({round(100*correct/question_count)}%) correct!")


def generation_selection():
    valid_generation = False
    while not valid_generation:
        generation_to_quiz = Prompt.ask("From what generation?", default="All")
        if generation_to_quiz[0].upper() == "A":
            generation_to_quiz = 0
            valid_generation = True
        elif generation_to_quiz.isnumeric() and 1 <= int(generation_to_quiz) <= len(helpers.GENERATIONS):
            generation_to_quiz = int(generation_to_quiz)
            valid_generation = True
        else:
            print("[red]Invalid selection!")

    return generation_to_quiz


def type_quiz_intro():
    print("Welcome to the Pokemon typing quiz!")
    print()
    question_count = IntPrompt.ask("How many Pokemon for the quiz?", default=10)
    helpers.generation_menu()
    generation_to_quiz = generation_selection()
    question_hints = Confirm.ask("Would you like hints?", default=False)
    type_quiz(
        question_count=question_count,
        hints=question_hints,
        generation=generation_to_quiz,
    )


def pokedex_text_quiz_intro():
    print("Welcome to the Pokemon Pokedex Entry Quiz!")
    print()
    question_count = IntPrompt.ask("How many Pokemon for the quiz?", default=10)
    helpers.generation_menu()
    generation_to_quiz = generation_selection()
    question_hints = Confirm.ask("Would you like hints?", default=False)
    pokedex_text_quiz(
        question_count=question_count,
        hints=question_hints,
        generation=generation_to_quiz,
    )


def pokedex_text_quiz(question_count=10, hints=False, generation=0):
    correct = 0

    previous_pokemon = set()
    pokemon = None
    for _ in range(question_count):
        while pokemon is None or pokemon.id in previous_pokemon:
            if generation == 0:
                pokemon = helpers.random_pokemon()
            else:
                pokemon = helpers.random_pokemon_from_generation(generation)
        previous_pokemon.add(pokemon.id)

        pokemon_name = pokemon.name.replace("-", " ").title()
        pokemon_text = helpers.pokedex_text_entry(pokemon.id)
        print()

        # print(f"CHEAT: This is text entry for {pokemon_name}.")
        print(pokemon_text)
        print("Which Pokemon is this?")
        if hints:
            print("Possible choices:")
            for possible_choice in helpers.multiple_choice_from_generation(pokemon_name, 4, generation):
                print(f" {possible_choice}")
        guess = Prompt.ask("Answer")

        if guess.lower() == pokemon_name.lower():
            print("[green]Correct![/green]")
            correct += 1
        else:
            print(f"[red]Wrong![/red] The correct answer is [bold]{pokemon_name}[/bold].")
        print()

    print("Done!")
    print(f"You got {correct} out of {question_count} ({round(100*correct/question_count)}%) correct!")


def game_menu():
    AVAILABLE_GAMES = {1: "Pokemon Types Quiz", 2: "Pokedex Entry Quiz"}

    print("--- Available Games ---")
    for key in AVAILABLE_GAMES.keys():
        print(f"{key}. {AVAILABLE_GAMES[key]}")
    game_choice = IntPrompt.ask("Which game would you like to play?")

    match game_choice:
        case 1:
            type_quiz_intro()
        case 2:
            pokedex_text_quiz_intro()
        case _:
            sys.exit()


if __name__ == "__main__":
    # type_quiz_intro()
    # pokedex_text_quiz_intro()
    game_menu()
