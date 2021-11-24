
# load modules
import asyncio
import time
import urllib.parse
from urllib import error, request


# const
MAX_RETRIES = 20
SLEEP_WAIT = 5
USER_AGENT = "bs-ranked-playlist/1.0.0"


# definition
class Limiter:

    def __init__(self):

        self.ratelimit_reset = None
        self.ratelimit_remaining = None
        self.ratelimit_limit = None

    async def wait(self):
        now = self.unix_timestamp()
        if (self.ratelimit_reset is None) or (now > self.ratelimit_reset):
            self.ratelimit_reset = None
            self.ratelimit_remaining = None
            return
        if self.ratelimit_remaining == 0:
            sleepTime = self.ratelimit_reset - now
            await asyncio.sleep(sleepTime)
            self.ratelimit_remaining = self.ratelimit_limit
            self.ratelimit_reset = None

    def unix_timestamp(self):
        return round(time.time() / 1000)

    def setLimitData(self, remaining, reset, limit):
        self.ratelimit_remaining = remaining
        self.ratelimit_reset = reset
        self.ratelimit_limit = limit


async def get(requestUrl: str):

    # init
    limiter = Limiter()

    # execute
    for _ in range(MAX_RETRIES):
        await limiter.wait()
        headers = {"User-Agent": urllib.parse.quote(USER_AGENT)}
        req = request.Request(requestUrl, headers=headers)
        try:
            response = request.urlopen(req)
            remaining = response.headers.get("x-ratelimit-remaining")
            reset = response.headers.get("x-ratelimit-reset")
            limit = response.headers.get("x-ratelimit-limit")
            limiter.setLimitData(remaining, reset, limit)
        except error.HTTPError as e:
            if e.code == 401:
                # Not logged in
                raise e
            elif e.code == 404:
                # Not found
                return e
            elif e.code == 422:
                # Invalid parameter
                raise e
            elif e.code == 429:
                # Too many requests
                await asyncio.sleep(SLEEP_WAIT)
            else:
                raise e
        else:
            return response
