from enum import Enum
from math import prod
from typing import *
import re

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

MAXIMA_ONE: Dict[Color, int] = {
    Color.RED: 12,
    Color.GREEN: 13,
    Color.BLUE: 14,
}

# Regexes
game_re = re.compile(r"Game (\d+)")

color_regexes = {
    color: re.compile(fr"(\d+) {color.value}")
    for color in Color
}

def extract_value(string: str, regex: Pattern[str]) -> int:
    match: Optional[Match[str]] = regex.search(string)
    if match is not None:
        return int(match.group(1))
    return 0

def is_possible_game(game: Dict[Color, int], maxima: Dict[Color, int]) -> bool:
    return all(
        game.get(color, 0) <= max
        for color, max in maxima.items()
    )

def compute_game_power(game: Dict[Color, int]) -> int:
    return prod(game.values())


def part_one() -> int:
    games_results = {}
    with open("input.txt", mode="r") as f_input:
        for line in f_input.readlines():
            game_line, rounds_line = line.split(":", maxsplit=1)

            # Get game ID
            match: Optional[Match[str]] = game_re.search(game_line)
            if match is None:
                raise ValueError(game_line)
            game_id: int = int(match.group(1))

            # Initialize game_results
            tmp_results = {color: 0 for color in Color}

            # Iterate on rounds
            for g_round in rounds_line.split(";"):

                # Look for each color
                for color in Color:
                    tmp_results[color] = max(tmp_results[color], extract_value(g_round, color_regexes[color]))

            # Finaly, add it to results
            games_results[game_id] = tmp_results

    # Compute possible games
    result: int = sum(
        id for id, game in games_results.items() if is_possible_game(game, MAXIMA_ONE)
    )
    return result


def part_two() -> int:
    games_results = {}
    with open("input.txt", mode="r") as f_input:
        for line in f_input.readlines():
            game_line, rounds_line = line.split(":", maxsplit=1)

            # Get game ID
            match: Optional[Match[str]] = game_re.search(game_line)
            if match is None:
                raise ValueError(game_line)
            game_id: int = int(match.group(1))

            # Initialize game_results
            tmp_results = {color: 0 for color in Color}

            # Iterate on rounds
            for g_round in rounds_line.split(";"):

                # Look for each color
                for color in Color:
                    tmp_results[color] = max(tmp_results[color], extract_value(g_round, color_regexes[color]))

            # Finaly, add it to results
            games_results[game_id] = tmp_results

    # Compute possible games power
    result: int = sum(
        compute_game_power(game) for _, game in games_results.items()
    )
    return result

print(part_one())
print(part_two())
