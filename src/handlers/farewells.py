from twitchAPI.chat import ChatMessage


TRIGGER_AND_RESPONSE: list[tuple[str, str]] = [
    ("пока", "Пока")
]


async def on_farewells(msg: ChatMessage) -> bool:
    if msg.user.name.lower() == "kurbezz":
        return False

    for trigger, response in TRIGGER_AND_RESPONSE:
        if trigger in msg.text.lower():
            await msg.reply(response)
            return True

    return False
