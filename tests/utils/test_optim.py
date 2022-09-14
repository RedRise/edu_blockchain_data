from utils.optim import highest_valid_binary_search
from typing import Callable


def get_valid_fun(thresh: float) -> Callable[[float], bool]:
    def res_fun(x: float) -> float:
        return x < thresh
    return res_fun


def test_highest_valid_binary_search_fails_if_low_above_high():
    (success, res) = highest_valid_binary_search(get_valid_fun(4), 10, 1, 1)
    assert not success


def test_highest_valid_binary_search_fails_lower_bound():
    (success, res) = highest_valid_binary_search(
        get_valid_fun(4), 0, 8, 1, lower_bound=True)
    assert success
    assert res == 3.5


def test_highest_valid_binary_search_fails_higher_bound():
    (success, res) = highest_valid_binary_search(
        get_valid_fun(4), 0, 8, 1, lower_bound=False)
    assert success
    assert res == 4
