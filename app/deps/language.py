from fastapi import Request, Depends
from typing import Literal

async def lang_dep(
        request: Request,
) -> Literal["en", "ro"]:
    accept_language = request.headers.get("accept-language", "")
    if "ro" in accept_language:
        return "ro"
    return "en"
