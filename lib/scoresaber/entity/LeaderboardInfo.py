# load modules
from dataclasses import dataclass
from typing import List, Union

from lib.scoresaber.entity import Difficulty
from lib.scoresaber.entity import Score


# definition class
@dataclass(frozen=True)
class LeaderboardInfo:

    id: float
    songHash: str
    songName: str
    songSubName: str
    songAuthorName: str
    levelAuthorName: str
    difficulty: Difficulty.Difficulty
    maxScore: float
    createdDate: str
    rankedDate: str
    qualifiedDate: str
    lovedDate: str
    ranked: bool
    qualified: bool
    loved: bool
    maxPP: float
    stars: float
    positiveModifiers: bool
    plays: float
    dailyPlays: float
    coverImage: float
    playerScore: Union[Score.Score, None]
    difficulties: Union[List[Difficulty.Difficulty], List, None]


# definition function
def gen(response):

    if response is not None:
        instance = LeaderboardInfo(
            id=response.get('id'),
            songHash=response.get('songHash'),
            songName=response.get('songName'),
            songSubName=response.get('songSubName'),
            songAuthorName=response.get('songAuthorName'),
            levelAuthorName=response.get('levelAuthorName'),
            difficulty=Difficulty.gen(response.get('difficulty')),
            maxScore=response.get('maxScore'),
            createdDate=response.get('createdDate'),
            rankedDate=response.get('rankedDate'),
            qualifiedDate=response.get('qualifiedDate'),
            lovedDate=response.get('lovedDate'),
            ranked=response.get('ranked'),
            qualified=response.get('qualified'),
            loved=response.get('loved'),
            maxPP=response.get('maxPP'),
            stars=response.get('stars'),
            positiveModifiers=response.get('positiveModifiers'),
            plays=response.get('plays'),
            dailyPlays=response.get('dailyPlays'),
            coverImage=response.get('coverImage'),
            playerScore=Score.gen(response.get('playerScore')),
            difficulties=Difficulty.genList(response.get('difficulties'))
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
