from pokequiz.helpers import combine_words, split_list


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
