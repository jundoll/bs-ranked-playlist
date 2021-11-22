# load modules
from dataclasses import dataclass


# definition class
@dataclass(frozen=True)
class LeaderboardPlayer:

    id: str
    name: str
    profilePicture: str
    country: str
    permissions: float
    role: str


# definition function
def gen(response):

    if response is not None:
        instance = LeaderboardPlayer(
            id=response.get('id'),
            name=response.get('name'),
            profilePicture=response.get('profilePicture'),
            country=response.get('country'),
            permissions=response.get('permissions'),
            role=response.get('role')
        )
        return instance


def genList(response):

    if response is not None:
        if type(response) is list:
            return [gen(v) for v in response]
