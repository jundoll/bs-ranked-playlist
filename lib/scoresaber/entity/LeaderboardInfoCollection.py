# load modules
from dataclasses import dataclass
from typing import List, Union

from lib.scoresaber.entity import LeaderboardInfo


# definition class
@dataclass(frozen=True)
class LeaderboardInfoCollection:

    leaderboards: Union[List[LeaderboardInfo.LeaderboardInfo], List]
    totalCount:  float


# definition function
def gen(response):

    if response is not None:
        instance = LeaderboardInfoCollection(
            leaderboards=LeaderboardInfo.genList(response.get('leaderboards')),
            totalCount=response.get('totalCount')
        )
        return instance


def genList(response):

    if response is not None:
        if type(response) is list:
            return [gen(v) for v in response]
