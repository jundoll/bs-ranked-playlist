# load modules
from dataclasses import dataclass
from typing import List, Union

from lib.scoresaber.entity import LeaderboardInfo


# definition class
@dataclass(frozen=True)
class LeaderboardInfoCollection:

    leaderboards: Union[List[LeaderboardInfo.LeaderboardInfo], List, None]
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
