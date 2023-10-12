import random
import pokebase as pb
from pokebase import cache
cache.API_CACHE

def random_pokemon():
    pokemon_id = random.randint(1, 1010)
    mon = pb.pokemon(pokemon_id)
    return mon.name

def pokemon_types(pokemon_id):
   mon = pb.pokemon(pokemon_id)
   mon_types = [pokemon_type.type.name for pokemon_type in mon.types]
   return mon_types
