import os
import json
import aiofiles

from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope


APP_ID = os.environ["TWITCH_APP_ID"]
APP_SECRET = os.environ["TWITCH_APP_SECRET"]
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]


class TokenManager:
    FILENAME = "tokens.json"

    @classmethod
    async def load(cls) -> tuple[str, str] | None:
        try:
            async with aiofiles.open(cls.FILENAME, "r") as f:
                data = await f.read()

                json_data = json.loads(data)

            return json_data["auth_token"], json_data["refresh_token"]
        except Exception as e:
            print(e)

        return None

    @classmethod
    async def save(cls, auth_token: str, refresh_token: str):
        async with aiofiles.open(cls.FILENAME, "w") as f:
            await f.write(
                json.dumps({
                    "auth_token": auth_token,
                    "refresh_token": refresh_token
                })
            )


async def get_auth_token(client: Twitch) -> tuple[str, str]:
    auth = UserAuthenticator(client, USER_SCOPE)

    token_data = await auth.authenticate()
    if token_data is None:
        raise RuntimeError("Authorization failed!")

    return token_data


async def get_client() -> Twitch:
    client = Twitch(APP_ID, APP_SECRET)

    saved_token = await TokenManager.load()

    if saved_token:
        token, refresh_token = saved_token
    else:
        token, refresh_token = await get_auth_token(client)
        await TokenManager.save(token, refresh_token)

    await client.set_user_authentication(
        token,
        scope=USER_SCOPE,
        refresh_token=refresh_token,
        validate=True,
    )

    return client
