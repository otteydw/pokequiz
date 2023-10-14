from pokequiz.helpers import (check_valid_pokemon_types, combine_words,
                              format_guess_as_list, split_list)


def test_combine_words():
    assert combine_words(["apple"]) == "apple"
    assert combine_words(["apple", "banana"]) == "apple and banana"
    assert combine_words(["apple", "banana", "orange"]) == "apple, banana and orange"
    assert (
        combine_words(["apple", "banana", "orange", "cherry"])
        == "apple, banana, orange and cherry"
    )


def test_split_list():
    assert split_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4) == [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10],
    ]


def test_format_guess_as_list():
    assert format_guess_as_list("Psychic, fairy") == ["fairy", "psychic"]
    assert format_guess_as_list("") == [""]


def test_check_valid_pokemon_types():
    assert check_valid_pokemon_types(["fairy"])
    assert check_valid_pokemon_types(["psychic", "rock"])
    assert not check_valid_pokemon_types(["dingo"])
    assert not check_valid_pokemon_types([""])
