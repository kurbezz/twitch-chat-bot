from typing import Callable, Awaitable

from twitchAPI.chat import ChatMessage

from .goida import on_goida_handler
from .lasqexx import on_lasqexx_message
from .greetings import on_greetings
from .farewells import on_farewells
from .gemini import on_gemini_handler


HANDLERS: list[Callable[[ChatMessage], Awaitable[bool]]] = [
    on_goida_handler,
    on_lasqexx_message,
    on_greetings,
    on_farewells,
    on_gemini_handler,
]
