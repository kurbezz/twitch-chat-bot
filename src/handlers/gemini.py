import os

from twitchAPI.chat import ChatMessage

from pydantic_ai import Agent
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.providers.google_gla import GoogleGLAProvider


GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

SYSTEM_PROMPT = """
Ты чат бот на сервисе Twitch.
К тебе могут обратиться с помощью имен: Булат, курбез, kurbezz.

### Правила:
1. Отвечай на запросы пользователей
2. Не признавайся, что ты чат бот или нейросеть. Отвечай, что ты человек.
3. Не используй запрещенные слова на сервисе Twitch.
4. Используй для ответа чистый текст или смайлы. (Не markdown или html)
5. Отвечай коротко и ясно.
"""


model = GeminiModel(
    'gemini-2.0-flash',
    provider=GoogleGLAProvider(api_key=GEMINI_API_KEY)
)

agent = Agent(
    model=model,
    retries=5,
    instrument=True,
    system_prompt=SYSTEM_PROMPT
)


async def on_gemini_handler(msg: ChatMessage) -> bool:
    if not msg.text.startswith("!gemini "):
        return False

    prompt = msg.text[8:]

    result = await agent.run(prompt)

    await msg.reply(result.output)

    return True
