import random

import pokebase as pb
from pokebase import cache

cache.API_CACHE


def random_pokemon():
    pokemon_id = random.randint(1, 1010)
    mon = pb.pokemon(pokemon_id)
    return mon


# def pokemon_types(pokemon_id):
#    mon = pb.pokemon(pokemon_id)
#    mon_types = [pokemon_type.type.name for pokemon_type in mon.types]
#    return mon_types


def pokemon_types(pokemon):
    mon_types = sorted([pokemon_type.type.name for pokemon_type in pokemon.types])
    return mon_types


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
        return f"{', '.join(words[:-1])}, and {words[-1]}"


def simple_pluralize(word_list, singular_string, pluralized_string):
    if len(word_list) == 1:
        return singular_string

    return pluralized_string
