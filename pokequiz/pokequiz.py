import click
import helpers

# import sys


def type_quiz(question_count=10, hints=False):
    correct = 0

    for _ in range(question_count):
        pokemon = helpers.random_pokemon()

        pokemon_name = pokemon.name.replace("-", " ").title()
        pokemon_types = helpers.pokemon_types(pokemon)
        # print(f"Name: {pokemon_name} | Types: {pokemon_types}")
        print()
        # print(helpers.pokemon_type_list())
        helpers.display_list_in_4_columns(helpers.pokemon_type_list())
        print()
        if hints:
            hint_text = f"Hint: it has {len(pokemon_types)} {helpers.simple_pluralize(pokemon_types, 'type','types')}."
        else:
            hint_text = ""
        print(f"What are the typings for {pokemon_name}? {hint_text}")
        guess = input("Answer? ")
        guess_list = sorted(guess.lower().replace(" ", "").split(","))
        # print(f"Guesses as sorted list: {guess_list}")

        if guess_list == pokemon_types:
            print("Correct!")
            correct += 1
        else:
            print(
                f"Wrong! {pokemon_name} has {helpers.simple_pluralize(pokemon_types, 'typing','typings')} of {helpers.combine_words(pokemon_types)}."
            )
        print()

    print("Done!")
    print(f"You got {correct} out of {question_count} correct!")


if __name__ == "__main__":
    print("Welcome to the Pokemon typing quiz!")
    print()
    question_count = click.prompt(
        "How many Pokemon for the quiz?", type=int, default=10
    )
    question_hints = click.confirm("Would you like hints?")
    # try:
    type_quiz(question_count=question_count, hints=question_hints)
    # except KeyboardInterrupt:
    #     sys.exit(1)
