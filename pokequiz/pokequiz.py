import helpers

def quiz():
    some_pokemon_name = helpers.random_pokemon()
    some_pokemon_types = helpers.pokemon_types(some_pokemon_name)
    print(f"Name: {some_pokemon_name} | Types: {some_pokemon_types}")

if __name__ == '__main__':
    quiz()
