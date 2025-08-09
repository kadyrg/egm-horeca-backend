from fastapi import Request

from app.core import settings


def get_preferred_language(accept_language: str) -> str:
    if not accept_language:
        return "en"
    languages = [lang.split(";")[0].strip() for lang in accept_language.split(",")]
    for lang in languages:
        if lang in settings.supported_languages:
            return lang
    return "en"

def lang_dep(request: Request) -> str:
    accept_language = request.headers.get("accept-language", "")
    return get_preferred_language(accept_language)
