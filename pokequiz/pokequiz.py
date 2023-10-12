import helpers


def type_quiz(question_count=3, hints=False):
    correct = 0
    for _ in range(question_count):
        pokemon = helpers.random_pokemon()

        pokemon_name = pokemon.name
        pokemon_types = helpers.pokemon_types(pokemon)
        # print(f"Name: {pokemon_name} | Types: {pokemon_types}")

        print(helpers.pokemon_type_list())
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
    type_quiz(hints=True)
