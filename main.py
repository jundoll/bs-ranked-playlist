# load modules
import pandas as pd
import asyncio
import json
import lib.scoresaber.api as scoresaberAPI


async def main():

    # 1. ranked playlist
    for star in range(15):

        # print
        page = 1
        print(f'star={star:02}, page={page:03}')

        # get ranked maplist
        leaderboardInfoCollection = await scoresaberAPI.getLeaderboardInfoCollection(ranked=True, minStar=star-1, maxStar=star+1, category=1, sort=0, page=1)

        # set songs
        if leaderboardInfoCollection is not None:
            if (leaderboardInfoCollection.leaderboards is not None) and len(leaderboardInfoCollection.leaderboards) > 0:
                IDs = [x.id for x in leaderboardInfoCollection.leaderboards if int(
                    x.stars) == star]
                songs = [{
                    "songName": x.songName,
                    "levelAuthorName": x.levelAuthorName,
                    "hash": x.songHash,
                    "levelid": f"custom_level_{x.songHash}",
                    "difficulties": [
                        {
                            "characteristic": "Standard",
                            "name": x.difficulty.difficultyRaw.split('_')[1]
                        }
                    ]
                } for x in leaderboardInfoCollection.leaderboards if int(x.stars) == star]
            else:
                return
        else:
            return

        
        while(True):

            # print & increment
            page += 1
            print(f'star={star:02}, page={page:03}')

            # get ranked maplist
            leaderboardInfoCollection = await scoresaberAPI.getLeaderboardInfoCollection(ranked=True, minStar=star-1, maxStar=star+1, category=1, sort=0, page=page)

            # set songs
            if leaderboardInfoCollection is not None:
                if (leaderboardInfoCollection.leaderboards is not None) and len(leaderboardInfoCollection.leaderboards) > 0:
                    # get
                    IDs += [x.id for x in leaderboardInfoCollection.leaderboards if int(
                        x.stars) == star]
                    songs += [{
                        "songName": x.songName,
                        "levelAuthorName": x.levelAuthorName,
                        "hash": x.songHash,
                        "levelid": f"custom_level_{x.songHash}",
                        "difficulties": [
                            {
                                "characteristic": "Standard",
                                "name": x.difficulty.difficultyRaw.split('_')[1]
                            }
                        ]
                    } for x in leaderboardInfoCollection.leaderboards if int(x.stars) == star]
                else:
                    break
            else:
                break

            await asyncio.sleep(1/200)

        # del duplicated element
        slct_index = [not b for b in list(pd.Index(IDs).duplicated())]
        songs = [e for e, i in zip(songs, slct_index) if i]

        # read image
        with open(f'imgs/s{star:02}.txt', 'r') as f:
            img = f.read()

        # gen playlist
        playlist = {
            "customData": {
                "syncURL": f"https://github.com/jundoll/bs-ranked-playlist/releases/latest/download/ranked_star_{star:02}.bplist",
                "weighting": 20,
                "customPassText": None
            },
            "playlistTitle": f"ranked_star_{star:02}",
            "playlistAuthor": "",
            "songs": songs,
            "image": img
        }

        # save
        with open(f'out/ranked_star_{star:02}.bplist', 'w') as f:
            json.dump(playlist, f)


    # 2. qualified playlist

    # print
    page = 1
    print(f'star=qualified, page={page:03}')

    # get qualified maplist
    leaderboardInfoCollection = await scoresaberAPI.getLeaderboardInfoCollection(qualified=True, category=4, sort=1, page=1)

    # set songs
    if leaderboardInfoCollection is not None:
        if (leaderboardInfoCollection.leaderboards is not None) and len(leaderboardInfoCollection.leaderboards) > 0:
            IDs = [x.id for x in leaderboardInfoCollection.leaderboards]
            songs = [{
                "songName": x.songName,
                "levelAuthorName": x.levelAuthorName,
                "hash": x.songHash,
                "levelid": f"custom_level_{x.songHash}",
                "difficulties": [
                    {
                        "characteristic": "Standard",
                        "name": x.difficulty.difficultyRaw.split('_')[1]
                    }
                ]
            } for x in leaderboardInfoCollection.leaderboards]
        else:
            return
    else:
        return

    while(True):

        # print & increment
        page += 1
        print(f'star=qualified, page={page:03}')

        # get ranked maplist
        leaderboardInfoCollection = await scoresaberAPI.getLeaderboardInfoCollection(qualified=True, category=4, sort=1, page=page)

        # set songs
        if leaderboardInfoCollection is not None:
            if (leaderboardInfoCollection.leaderboards is not None) and len(leaderboardInfoCollection.leaderboards) > 0:
                # get
                IDs += [x.id for x in leaderboardInfoCollection.leaderboards]
                songs += [{
                    "songName": x.songName,
                    "levelAuthorName": x.levelAuthorName,
                    "hash": x.songHash,
                    "levelid": f"custom_level_{x.songHash}",
                    "difficulties": [
                        {
                            "characteristic": "Standard",
                            "name": x.difficulty.difficultyRaw.split('_')[1]
                        }
                    ]
                } for x in leaderboardInfoCollection.leaderboards]
            else:
                break
        else:
            break

        await asyncio.sleep(1/200)

    # del duplicated element
    slct_index = [not b for b in list(pd.Index(IDs).duplicated())]
    songs = [e for e, i in zip(songs, slct_index) if i]

    # read image
    with open(f'imgs/qualified.txt', 'r') as f:
        img = f.read()

    # gen playlist
    playlist = {
        "customData": {
            "syncURL": f"https://github.com/jundoll/bs-ranked-playlist/releases/latest/download/ranked_star_qualified.bplist",
            "weighting": 20,
            "customPassText": None
        },
        "playlistTitle": f"ranked_star_qualified",
        "playlistAuthor": "",
        "songs": songs,
        "image": img
    }

    # save
    with open(f'out/ranked_star_qualified.bplist', 'w') as f:
        json.dump(playlist, f)



if __name__ == '__main__':
    asyncio.run(main())
