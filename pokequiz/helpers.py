import random
import sys
from functools import lru_cache
from pathlib import Path, PurePath

import pokebase as pb
import requests
from pokebase import cache
from rich import box
from rich.console import Console
from rich.table import Table

# from rich.align import Align

cache.API_CACHE

GENERATIONS = [
    "Kanto",
    "Johto",
    "Hoenn",
    "Sinnoh",
    "Unova",
    "Kalos",
    "Alola",
    "Galar",
    "Paldea",
]

POKEMON_TYPES = {
    "bug": ":lady_beetle:",
    "dark": ":new_moon:",
    "dragon": ":dragon_face:",
    "electric": ":bulb:",
    "fairy": ":fairy:",
    "fighting": ":boxing_glove:",
    "fire": ":fire:",
    "flying": ":eagle:",
    "ghost": ":ghost:",
    "grass": ":herb:",
    "ground": ":mountain: ",
    "ice": ":snowflake: ",
    "normal": ":grinning_face:",
    "poison": ":skull_and_crossbones: ",
    "psychic": ":crystal_ball:",
    "rock": "🪨 ",
    "steel": ":nut_and_bolt:",
    "water": ":droplet:",
}

CACHED_IMAGES_DIRECTORY = Path("images/cached/")
STATIC_IMAGES_DIRECTORY = Path("images/static/")

TYPE_IMAGES_DIRECTORY = Path.joinpath(STATIC_IMAGES_DIRECTORY, "types")


def random_pokemon():
    MAX_POKEMON = 1010
    pokemon_id = random.randint(1, MAX_POKEMON)
    mon = pb.pokemon(pokemon_id)
    return mon


def random_pokemon_from_generation(generation_number):
    generation_resource = pb.generation(generation_number)
    random_mon = random.choice(generation_resource.pokemon_species)
    mon = pb.pokemon(random_mon.name)
    return mon


# def pokemon_types(pokemon_id):
#    mon = pb.pokemon(pokemon_id)
#    mon_types = [pokemon_type.type.name for pokemon_type in mon.types]
#    return mon_types


def pokemon_types(pokemon):
    mon_types = sorted([pokemon_type.type.name for pokemon_type in pokemon.types])
    return mon_types


@lru_cache(maxsize=None)
def pokemon_type_list():
    pokemon_type_list = sorted([pokemon_type["name"] for pokemon_type in pb.APIResourceList("type")])
    pokemon_type_list.remove("shadow")
    pokemon_type_list.remove("unknown")
    return pokemon_type_list


def pokemon_type_list_with_emoji():
    pokemon_type_list = sorted(POKEMON_TYPES.keys())
    pokemon_types_with_emoji = []
    for pokemon_type in pokemon_type_list:
        pokemon_types_with_emoji.append(f"{POKEMON_TYPES[pokemon_type]} {pokemon_type}")
    return pokemon_types_with_emoji


def combine_words(words):
    """Combines a list of words into a string, using commas and the word "and" to separate the words.

    Args:
      words: A list of strings.

    Returns:
      A string containing the combined words, using commas and the word "and" to separate the words.
    """

    if len(words) == 1:
        return words[0]
    elif len(words) == 2:
        return f"{words[0]} and {words[1]}"
    else:
        return f"{', '.join(words[:-1])} and {words[-1]}"


def simple_pluralize(word_list, singular_string, pluralized_string):
    if len(word_list) == 1:
        return singular_string

    return pluralized_string


# def print_list_in_columns(list_of_items, columns=4):
#   """Prints a list of items in columns.

#   Args:
#     list_of_items: A list of items to print.
#     columns: The number of columns to print the items in.
#   """

#   table = textualize.Textualize(columns=columns)

#   for i in range(0, len(list_of_items), columns):
#     table.add_row(list_of_items[i:i + columns])

#   print(table.render())


def display_list_in_4_columns(list_of_items):
    """Displays a list of unknown length in 4 columns using the textual library.

    Args:
    list_of_items: A list of items to display.
    """

    # Split the list into chunks of 4 items.
    chunks = split_list(list_of_items, 4)

    table = Table(title="Pokemon Types", show_header=False, box=box.SIMPLE)
    # Create 4 non-labeled columns
    for _ in range(4):
        table.add_column()
    # Iterate over the chunks and add each item to a row in the table.
    for chunk in chunks:
        table.add_row(*chunk)

    # table = Align.center(table, vertical="middle")
    console = Console()
    console.print(table)


def split_list(list1, n):
    """Splits a list into a list of sublists with each sublist being of size n or less.

    Args:
      list1: A list of elements.
      n: The size of each sublist.

    Returns:
      A list of sublists.
    """

    sublists = []
    for i in range(0, len(list1), n):
        sublists.append(list1[i : i + n])
    return sublists


def format_guess_as_list(guess):
    """Format a user's guess by converting to lowercase, removing spaces and then splitting into a list.

    Args:
        guess string: Responses in upper or lower case, with or without spaces, multiple words split by commas.

    Returns:
        list: A list of strings
    """
    return sorted(guess.lower().replace(" ", "").split(","))


def check_valid_pokemon_types(types_to_check):
    return set(types_to_check).issubset(pokemon_type_list())


def generation_number_to_name(generation_number):
    if generation_number < 1 or generation_number > 9:
        raise Exception("Invalid generation!")
    return GENERATIONS[generation_number - 1]


def generation_menu():
    print("A: All")
    for generation_number_offset, generation_name in enumerate(GENERATIONS):
        print(f"{generation_number_offset+1}: {generation_name}")


def pokedex_text_entry(pokemon_name_or_id, language="en"):
    mon = pb.pokemon_species(pokemon_name_or_id)
    for flavor_text_entry in mon.flavor_text_entries:
        # from rich import inspect
        # inspect(flavor_text_entry.language)
        if flavor_text_entry.language.name == language:
            flavor_text = flavor_text_entry.flavor_text.replace("\n", " ").replace("\x0c", " ")

            for substring in [mon.name.upper(), mon.name.capitalize(), mon.name]:
                flavor_text = flavor_text.replace(substring, "_____")

            for substring in ["POKé BALL", "POKéMON"]:
                flavor_text = flavor_text.replace(substring, substring.title())

            flavor_text = flavor_text.replace(substring, "_____")
            return flavor_text


def multiple_choice_from_generation(correct_answer, total_answers, generation):
    choices = set()
    choices.add(correct_answer.capitalize())
    while len(choices) < total_answers:
        if generation == 0:
            pokemon = random_pokemon()
        else:
            pokemon = random_pokemon_from_generation(generation)
        choices.add(pokemon.name.capitalize())
    return sorted(list(choices))


def pokemon_sprite(pokemon):
    pokemon_image_file = Path(PurePath(CACHED_IMAGES_DIRECTORY, pokemon.name + ".gif"))

    if not pokemon_image_file.is_file():
        image_url = pokemon.sprites.front_default
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(pokemon_image_file, "wb") as f:
                f.write(response.content)
        else:
            print(f"Error downloading {image_url}. Response code {response.status_code}.")
            sys.exit(1)

    return pokemon_image_file


def type_sprite(type_name):

    type_image_file = Path(PurePath(TYPE_IMAGES_DIRECTORY, type_name + ".png"))
    return type_image_file


def str2bool(s):
    return s.lower() in ("yes", "true", "t", "1")


def list_as_string(lst):
    if len(lst) == 2:
        return " and ".join(lst)
    else:
        return lst[0]
