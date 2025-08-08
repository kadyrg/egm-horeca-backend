from fastapi import Request, Depends

SUPPORTED_LANGUAGES = {"en", "ro"}

def get_preferred_language(accept_language: str) -> str:
    if not accept_language:
        return "en"

    languages = [lang.split(";")[0].strip() for lang in accept_language.split(",")]

    for lang in languages:
        if lang in SUPPORTED_LANGUAGES:
            return lang

    return "en"

def language_dependency(request: Request) -> str:
    accept_language = request.headers.get("accept-language", "")
    return get_preferred_language(accept_language)
