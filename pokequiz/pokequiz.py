import helpers
from rich import print
from rich.prompt import Confirm, IntPrompt, Prompt


def type_quiz(question_count=10, hints=False):
    correct = 0
    previous_pokemon = set()
    pokemon = None
    for _ in range(question_count):
        while pokemon is None or pokemon.id in previous_pokemon:
            pokemon = helpers.random_pokemon()
        previous_pokemon.add(pokemon.id)

        pokemon_name = pokemon.name.replace("-", " ").title()
        pokemon_types = helpers.pokemon_types(pokemon)
        print()
        helpers.display_list_in_4_columns(helpers.pokemon_type_list())
        print()
        if hints:
            hint_text = f"Hint: it has {len(pokemon_types)} {helpers.simple_pluralize(pokemon_types, 'type','types')}."
        else:
            hint_text = ""
        print(f"What are the typings for {pokemon_name}? {hint_text}")
        guess = Prompt.ask("Answer")
        guess_list = sorted(guess.lower().replace(" ", "").split(","))

        if guess_list == pokemon_types:
            print("[green]Correct![/green]")
            correct += 1
        else:
            print(
                f"[red]Wrong![/red] {pokemon_name} has {helpers.simple_pluralize(pokemon_types, 'typing','typings')} of [bold]{helpers.combine_words(pokemon_types)}[/bold]."
            )
        print()

    print("Done!")
    print(f"You got {correct} out of {question_count} correct!")


if __name__ == "__main__":
    print("Welcome to the Pokemon typing quiz!")
    print()
    question_count = IntPrompt.ask("How many Pokemon for the quiz?", default=10)
    question_hints = Confirm.ask("Would you like hints?", default=False)
    type_quiz(question_count=question_count, hints=question_hints)
