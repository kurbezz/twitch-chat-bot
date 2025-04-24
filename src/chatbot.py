from asyncio import sleep

from twitchAPI.type import ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage

from auth import get_client, Twitch
from handlers import HANDLERS


class ChatBot:
    TARGET_CHANNELS = [
        "kurbezz",
        "kamsyll"
    ]

    def __init__(self, client: Twitch):
        self.client = client

    @classmethod
    async def on_ready(cls, ready_event: EventData):
        print("[system]: Ready!")

        for channel in cls.TARGET_CHANNELS:
            print(f"[system]: Subscribe to {channel}...")
            await ready_event.chat.join_room(channel)
            print(f"[system]: Subscribed to {channel}!")

    @classmethod
    async def on_message(cls, msg: ChatMessage):
        print(f"[{msg.user.name}]: {msg.text}")

        for handler in HANDLERS:
            await handler(msg)

    @classmethod
    async def run(cls):
        client = await get_client()

        chat = await Chat(client)

        chat.register_event(ChatEvent.READY, cls.on_ready)
        chat.register_event(ChatEvent.MESSAGE, cls.on_message)

        chat.start()

        try:
            while True:
                await sleep(1)
        except KeyboardInterrupt:
            print("[system]: Shutting down...")
        finally:
            chat.stop()
            await client.close()
