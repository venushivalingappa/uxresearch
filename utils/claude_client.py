import json
import re
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import MODEL, ANTHROPIC_API_KEY


class StageExecutionError(Exception):
    pass


_client: anthropic.Anthropic | None = None


def get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def _extract_json(text: str) -> dict:
    text = text.strip()
    # Strip markdown fences
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Find first { and last }
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
        raise


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((anthropic.RateLimitError, anthropic.APIStatusError)),
    reraise=True,
)
def _call_api(system: str, user: str, max_tokens: int) -> str:
    client = get_client()
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text


def call_claude(system_prompt: str, user_prompt: str, max_tokens: int = 2048) -> dict:
    try:
        raw = _call_api(system_prompt, user_prompt, max_tokens)
    except Exception as e:
        raise StageExecutionError(f"Claude API call failed: {e}") from e

    try:
        return _extract_json(raw)
    except (json.JSONDecodeError, ValueError):
        pass

    # Repair attempt
    repair_prompt = (
        "Your previous response was not valid JSON. "
        "Return ONLY the JSON object with no markdown fences, no explanation, no extra text.\n\n"
        f"Previous response:\n{raw}"
    )
    try:
        raw2 = _call_api(system_prompt, repair_prompt, max_tokens)
        return _extract_json(raw2)
    except Exception as e:
        raise StageExecutionError(f"Failed to parse Claude response as JSON: {e}\n\nRaw: {raw[:500]}") from e
