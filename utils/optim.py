# inspired by https://www.geeksforgeeks.org/python-program-for-binary-search/
from typing import Callable, Tuple

# Returns index of x in arr if present, else -1


def highest_valid_binary_search(
        valid_fun: Callable[[float], bool],
        low: float,
        high: float,
        prec: float,
        low_valid: bool = None,
        high_valid: bool = None,
        lower_bound: bool = True) -> Tuple[bool, float]:

    if high < low:
        return (False, 0)

    if low_valid is None:
        low_valid = valid_fun(low)

    if not low_valid:
        return (False, 0)

    if high_valid is None:
        high_valid = valid_fun(high)

    if high_valid:
        return (True, high)

    # low_valid & !high_valid
    mid = (low+high)/2
    mid_valid = valid_fun(mid)

    end_for_prec = (high-low) < 2 * prec

    if mid_valid:
        if end_for_prec:
            return (True, mid if lower_bound else high)
        else:
            return highest_valid_binary_search(valid_fun, mid, high, prec, low_valid=True, high_valid=False, lower_bound=lower_bound)
    else:
        if end_for_prec:
            return (True, low if lower_bound else mid)
        else:
            return highest_valid_binary_search(valid_fun, low, mid, prec, low_valid=True, high_valid=False, lower_bound=lower_bound)


# highest_valid_binary_search(lambda x: x < 4, 0, 8, 1, lower_bound=False)
