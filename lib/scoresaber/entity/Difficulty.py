# load modules
from dataclasses import dataclass


# definition class
@dataclass(frozen=True)
class Difficulty:

    leaderboardId: float
    difficulty: float
    gameMode: str
    difficultyRaw: str


# definition function
def gen(response):

    instance = Difficulty(
        leaderboardId=response.get('leaderboardId'),
        difficulty=response.get('difficulty'),
        gameMode=response.get('gameMode'),
        difficultyRaw=response.get('difficultyRaw')
    )
    return instance


def genList(response):

    if response is None:
        return None
    else:
        if type(response) is list:
            if len(response) == 0:
                return []
            else:
                return [gen(v) for v in response]
        elif type(response) is dict:
            return [gen(response)]
