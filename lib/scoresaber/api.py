
# load modules
import json
from lib.api import api
from lib.scoresaber.entity import LeaderboardInfoCollection


# init
SERVER = 'https://scoresaber.com'


# definition
async def getLeaderboardInfoCollection(
    search: str = '',
    verified: bool = False,
    ranked: bool = False,
    qualified: bool = False,
    loved: bool = False,
    minStar: float = 0,
    maxStar: float = 100,
    category: int = 0,
    sort: int = 0,
    unique: bool = False
):

    # prepare query
    query_list = []
    if search:
        # base64変換(空白処理が主目的)
        search = search
        query_list.append(f'search={search}')
    if verified:
        query_list.append('verified=true')
    if ranked:
        query_list.append('ranked=true')
    if qualified:
        query_list.append('qualified=true')
    if loved:
        query_list.append('loved=true')
    if minStar >= 0:
        query_list.append(f'minStar={minStar}')
    if maxStar >= 0:
        query_list.append(f'maxStar={maxStar}')
    if category >= 0:
        query_list.append(f'category={category}')
    if sort >= 0:
        query_list.append(f'sort={sort}')
    if unique:
        query_list.append('unique=true')
    if len(query_list) > 0:
        query = f'?{"&".join(query_list)}'
    else:
        query = ''

    # request
    requestUrl = f'{SERVER}/api/leaderboards{query}'
    print(requestUrl)
    response = await api.get(requestUrl)
    responseJson = json.load(response)
    return LeaderboardInfoCollection.gen(responseJson)
