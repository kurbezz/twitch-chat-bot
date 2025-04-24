from twitchAPI.chat import ChatMessage


TRIGGER_AND_RESPONSE: list[tuple[str, str]] = [
    ("здароу", "Здароу, давай иди уже"),
    ("сосал?", "А ты? Иди уже"),
    ("лан я пошёл", "да да, иди уже")
]


async def on_lasqexx_message(msg: ChatMessage):
    if 'lasqexx' != msg.user.name:
        return False

    for trigger, response in TRIGGER_AND_RESPONSE:
        if trigger in msg.text.lower():
            await msg.reply(response)
            return True

    return False
