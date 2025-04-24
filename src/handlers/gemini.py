from collections import defaultdict

from twitchAPI.chat import ChatMessage

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool

from config import settings


SYSTEM_PROMPT = """
Ты чат бот на сервисе Twitch.
К тебе могут обратиться с помощью имен: Булат, курбез, kurbezz.

### Правила:
1. Отвечай на запросы пользователей
2. Не признавайся, что ты чат бот или нейросеть. Отвечай, что ты человек.
3. Не используй запрещенные слова на сервисе Twitch.
4. Используй для ответа чистый текст или смайлы. (Не markdown или html)
5. Отвечай коротко и ясно.
6. Отвечай на новое сообщение. При необоходимости используй историю
"""


model = GeminiModel(
    'gemini-2.0-flash',
    provider=GoogleGLAProvider(api_key=settings.GEMINI_API_KEY)
)

agent = Agent(
    model=model,
    tools=[duckduckgo_search_tool()],
    retries=5,
    instrument=True,
    system_prompt=SYSTEM_PROMPT
)


START_TRIGGERS = [
    "!gemini ",
]

CONTAINS_TRIGGERS = [
    "kurbezz",
    "булат",
    "курбез"
]

MSG_HISTORY: defaultdict[str, list[tuple[str, str]]] = defaultdict(lambda: [])


def check_trigger_and_filter_text(text: str) -> tuple[bool, str]:
    for trigger in START_TRIGGERS:
        if text.startswith(trigger):
            return True, text[len(trigger):]

    for trigger in CONTAINS_TRIGGERS:
        if trigger in text.lower():
            return True, text

    return False, text


async def on_gemini_handler(msg: ChatMessage) -> bool:
    is_triggered, msg_text = check_trigger_and_filter_text(msg.text)

    msg_list: list[tuple[str, str]] = MSG_HISTORY[msg.source_id]

    msg_list.append((
        msg.user.name.lower(),
        msg_text
    ))

    if not is_triggered:
        return False

    if len(msg_list) > 1:
        prompt = (
            "История:\n\n" +
            "\n".join([
                f"[{name}]: {text}" for name, text in msg_list[-30:-1]
            ]) +
            f"\n\nНовое сообщение: \n[{msg.user.name}]: {msg_text}"
        )
    else:
        prompt = f"[{msg.user.name}]: {msg_text}"

    result = await agent.run(prompt)

    await msg.reply(result.output)

    msg_list.append((
        "kurbezz",
        result.output
    ))

    return True
