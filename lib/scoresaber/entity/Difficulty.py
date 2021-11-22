# load modules
from dataclasses import dataclass


# definition class
@dataclass(frozen=True)
class Difficulty:

    leaderboardId: float
    difficulty: float


# definition function
def gen(response):

    instance = Difficulty(
        leaderboardId=response.get('leaderboardId'),
        difficulty=response.get('difficulty')
    )
    return instance


def genList(response):

    if response is None:
        return []
    elif (type(response) == 'list') and (len(response) == 0):
        return []
    else:
        return [gen(v) for v in response]
