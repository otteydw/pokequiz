import random
from functools import lru_cache

import pokebase as pb
from pokebase import cache
from rich import box
from rich.console import Console
from rich.table import Table

cache.API_CACHE


def random_pokemon():
    MAX_POKEMON = 1010
    pokemon_id = random.randint(1, MAX_POKEMON)
    mon = pb.pokemon(pokemon_id)
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
    pokemon_type_list = sorted(
        [pokemon_type["name"] for pokemon_type in pb.APIResourceList("type")]
    )
    pokemon_type_list.remove("shadow")
    pokemon_type_list.remove("unknown")
    return pokemon_type_list


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
    # chunks = to_chunks(list_of_items, 4)
    chunks = split_list(list_of_items, 4)

    table = Table(title="Pokemon Types", show_header=False, box=box.SIMPLE)
    # table.add_column("Released", justify="right", style="cyan", no_wrap=True)
    # table.add_column("Title", style="magenta")
    # table.add_column("Box Office", justify="right", style="green")
    # table.add_column("Dingo", justify="right", style="green")
    table.add_column()
    table.add_column()
    table.add_column()
    table.add_column()
    # Iterate over the chunks and add each item to a row in the table.
    for chunk in chunks:
        table.add_row(*chunk)

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
