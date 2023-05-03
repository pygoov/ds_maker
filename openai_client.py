import aiohttp

from typing import Optional


class OpenAIClient:

    def __init__(self, token: str) -> None:
        self._token = token

    def _request(self, *args, **keargs):
        headers = keargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self._token}"
        keargs["headers"] = headers
        return aiohttp.request(*args, **keargs)

    async def completions(self,
                          prompt: str,
                          model: str = "text-davinci-003",
                          max_tokens: int = 1000,
                          temperature: float = 0.5,
                          presence_penalty: float = 0.5,
                          top_p: float = 1,
                          stop: Optional[str] = None) -> str:
        async with self._request(
            "POST", "https://api.openai.com/v1/completions",
            json={
                "prompt": prompt,
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "presence_penalty": presence_penalty,
                "top_p": top_p,
                "n": 1,
                "stop": stop,
                "stream": False,  # TODO: may be write
            }
        ) as rsp:
            data = await rsp.json()
            print(data)
        return data["choices"][0]["text"]
