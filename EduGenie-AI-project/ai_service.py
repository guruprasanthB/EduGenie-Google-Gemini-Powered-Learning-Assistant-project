import asyncio
import json
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from config import settings


class TransientProviderError(ValueError):
    def __init__(self, message: str, retry_after: float | None = None):
        super().__init__(message)
        self.retry_after = retry_after


def _extract_error_message(payload: object) -> str:
    if payload is None:
        return "Request rejected"

    if isinstance(payload, str):
        stripped = payload.strip()
        if stripped:
            return stripped
        return "Request rejected"

    if isinstance(payload, list):
        for item in payload:
            message = _extract_error_message(item)
            if message != "Request rejected":
                return message
        return "Request rejected"

    if isinstance(payload, dict):
        for key in ("message", "error", "description", "detail"):
            value = payload.get(key)
            message = _extract_error_message(value)
            if message != "Request rejected":
                return message

        for value in payload.values():
            if isinstance(value, (dict, list)):
                message = _extract_error_message(value)
                if message != "Request rejected":
                    return message

    return "Request rejected"


def _read_http_error_body(exc: HTTPError) -> str:
    try:
        body = exc.read()
    except Exception:
        body = None

    if body is None and getattr(exc, "fp", None) is not None:
        try:
            body = exc.fp.read()
        except Exception:
            body = None

    if isinstance(body, bytes):
        return body.decode("utf-8", errors="replace")
    if isinstance(body, str):
        return body
    if body is None:
        return ""
    return str(body)


def _post_json(url: str, payload: dict, headers: dict[str, str] | None = None) -> dict:
    request = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **(headers or {})},
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raw_body = _read_http_error_body(exc).strip()
        try:
            body = json.loads(raw_body) if raw_body else {}
            message = _extract_error_message(body)
        except (json.JSONDecodeError, TypeError, ValueError):
            message = _extract_error_message(raw_body)
        if exc.code in {429, 500, 502, 503, 504}:
            retry_after = None
            try:
                retry_after = float(exc.headers.get("Retry-After"))
            except (AttributeError, TypeError, ValueError):
                pass
            raise TransientProviderError(
                f"AI provider is temporarily unavailable (HTTP {exc.code}): {message}",
                retry_after,
            ) from exc
        raise ValueError(f"AI provider returned HTTP {exc.code}: {message}") from exc
    except URLError as exc:
        raise ValueError("Could not connect to the AI provider. Check your network and try again.") from exc
    except json.JSONDecodeError as exc:
        raise ValueError("The AI provider returned an invalid response.") from exc


def _extract_text_blocks(data: object) -> list[str]:
    texts: list[str] = []

    def append_text(value: object) -> None:
        if isinstance(value, str) and value.strip():
            texts.append(value.strip())

    def walk(node: object) -> None:
        if isinstance(node, dict):
            if isinstance(node.get("text"), str):
                append_text(node["text"])
            if isinstance(node.get("content"), list):
                for item in node["content"]:
                    walk(item)
            if isinstance(node.get("parts"), list):
                for item in node["parts"]:
                    walk(item)
            for value in node.values():
                if isinstance(value, (dict, list)):
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return texts


def _generate_gemini(
    prompt: str,
    response_mime_type: str | None,
    model: str | None = None,
) -> str:
    if not settings.gemini_api_key:
        raise ValueError("GEMINI_API_KEY is not configured. Add it to the project's .env file.")

    gemini_model = model or settings.gemini_model
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {},
    }
    if response_mime_type:
        payload["generationConfig"]["responseMimeType"] = response_mime_type

    data = _post_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent",
        payload,
        {"x-goog-api-key": settings.gemini_api_key},
    )

    texts = _extract_text_blocks(data)
    if texts:
        return "\n".join(texts).strip()
    raise ValueError("The AI provider returned no text. Try again with a shorter prompt.")


def _generate_local(prompt: str) -> str:
    if not settings.local_explanation_enabled:
        raise ValueError("GEMINI_API_KEY is not configured. Add it to the project's .env file.")
    data = _post_json(
        "http://127.0.0.1:11434/api/generate",
        {"model": settings.local_explanation_model, "prompt": prompt, "stream": False},
    )
    text = data.get("response", "").strip()
    if not text:
        raise ValueError("The local model returned no text.")
    return text


async def generate_text(
    prompt: str,
    *,
    response_mime_type: str | None = None,
    local: bool = False,
) -> str:
    if len(prompt) > settings.max_input_chars + 6000:
        raise ValueError(f"This request is too long. Keep it under {settings.max_input_chars} characters.")
    models = [None] if local else [settings.gemini_model]
    if (
        not local
        and settings.gemini_fallback_model
        and settings.gemini_fallback_model != settings.gemini_model
    ):
        models.append(settings.gemini_fallback_model)

    last_error = None
    for model in models:
        try:
            if local:
                return await asyncio.to_thread(_generate_local, prompt)
            return await asyncio.to_thread(
                _generate_gemini,
                prompt,
                response_mime_type,
                model,
            )
        except TransientProviderError as exc:
            last_error = exc

    if last_error is not None:
        raise last_error
    raise ValueError("The AI provider could not complete this request.")