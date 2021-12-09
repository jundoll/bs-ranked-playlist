# load modules
from dataclasses import dataclass
from typing import Union

from lib.scoresaber.entity import LeaderboardPlayer


# definition class
@dataclass(frozen=True)
class Score:

    id: float
    leaderboardPlayerInfo: Union[LeaderboardPlayer.LeaderboardPlayer, None]
    rank: float
    baseScore: float
    modifiedScore: float
    pp: float
    weight: float
    modifiers: str
    badCuts: float
    missedNotes: float
    maxCombo: float
    fullCombo: bool
    hmd: float
    hasReplay: bool
    timeSet: str


# definition function
def gen(response):

    if response is not None:
        instance = Score(
            id=response.get('id'),
            leaderboardPlayerInfo=LeaderboardPlayer.gen(
                response.get('leaderboardPlayerInfo')),
            rank=response.get('rank'),
            baseScore=response.get('baseScore'),
            modifiedScore=response.get('modifiedScore'),
            pp=response.get('pp'),
            weight=response.get('weight'),
            modifiers=response.get('modifiers'),
            badCuts=response.get('badCuts'),
            missedNotes=response.get('missedNotes'),
            maxCombo=response.get('maxCombo'),
            fullCombo=response.get('fullCombo'),
            hmd=response.get('hmd'),
            hasReplay=response.get('hasReplay'),
            timeSet=response.get('timeSet')
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
