# load modules
import asyncio
from urllib.request import Request, urlopen
import pandas as pd
import json
import lib.scoresaber.api as scoresaberAPI


async def main():

    for star in range(15):

        # get ranked maplist
        leaderboardInfoCollection = await scoresaberAPI.getLeaderboardInfoCollection(ranked=True, minStar=star-1, maxStar=star+1)

        # set songs
        if leaderboardInfoCollection is not None:
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
        else:
            print(1)
            return

        # read image
        with open(f'img/s{star:02}.txt', 'r') as f:
            img = f.read()

        # gen playlist
        playlist = {
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
