from twitchAPI.chat import ChatMessage


async def on_goida_handler(message: ChatMessage) -> bool:
    if "гойда" not in message.text.lower():
        return False

    await message.reply("ГООООООООООООООООООООООООООООООООООООЙДА!")

    return True
