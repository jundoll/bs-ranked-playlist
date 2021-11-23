# load modules
import pandas as pd
import asyncio
import json
import lib.scoresaber.api as scoresaberAPI


async def main():

    for star in range(15):

        # get ranked maplist
        leaderboardInfoCollection = await scoresaberAPI.getLeaderboardInfoCollection(ranked=True, minStar=star-1, maxStar=star+1, category=1, sort=0, page=1)

        # set songs
        if leaderboardInfoCollection is not None:
            if len(leaderboardInfoCollection.leaderboards) > 0:
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
                            "name": x.difficultyRaw.split('_')[1]
                        }
                    ]
                } for x in leaderboardInfoCollection.leaderboards if int(x.stars) == star]
                totalCount = leaderboardInfoCollection.totalCount
            else:
                return
        else:
            return

        page = 0
        while(len(songs) < totalCount):
            # increment
            page += 1
            print(f'star={star:02}, page={page:03}')

            # get ranked maplist
            leaderboardInfoCollection = await scoresaberAPI.getLeaderboardInfoCollection(ranked=True, minStar=star-1, maxStar=star+1, category=1, sort=0, page=page)

            # set songs
            if leaderboardInfoCollection is not None:
                if len(leaderboardInfoCollection.leaderboards) > 0:
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
                                "name": x.difficultyRaw.split('_')[1]
                            }
                        ]
                    } for x in leaderboardInfoCollection.leaderboards if int(x.stars) == star]

                    # del duplicated element
                    slct_index = [not b for b in list(pd.Index(IDs).duplicated())]
                    IDs = [e for e, i in zip(IDs, slct_index) if i]
                    songs = [e for e, i in zip(songs, slct_index) if i]
                else:
                    break
            else:
                break

            await asyncio.sleep(1/200)

        # read image
        with open(f'img/s{star:02}.txt', 'r') as f:
            img = f.read()

        # gen playlist
        playlist = {
            "customData": {
                "syncURL": f"https://github.com/jundoll/bs-ranked-playlist/releases/latest/download/ranked_star_{star:02}.bplist",
                "weighting": 20,
                "customPassText": None
            },
            "playlistTitle": f"ranked_star_{star:02}",
            "playlistAuthor": "aruru",
            "songs": songs,
            "image": img
        }

        # save
        with open(f'dist/ranked_star_{star:02}.bplist', 'w') as f:
            json.dump(playlist, f)


if __name__ == '__main__':
    asyncio.run(main())
