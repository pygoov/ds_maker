import aiohttp

from typing import Optional, List


class OpenAIClient:

    def __init__(self, token: str) -> None:
        self._token = token

    def _request(self, *args, **keargs):
        headers = keargs.get("headers", {})
        headers["Authorization"] = f"Bearer {self._token}"
        keargs["headers"] = headers
        return aiohttp.request(*args, **keargs)

    async def get_balance(self) -> dict:
        async with self._request(
            "GET", "https://api.openai.com/dashboard/billing/subscription",
        ) as rsp:
            if rsp.status != 200:
                text = await rsp.read()
                raise Exception(f'request failed[statue={rsp.status}]: {text}')
            data = await rsp.json()
            assert isinstance(data, dict)
            return data

    async def completions(self,
                          prompt: str,
                          model: str = "text-davinci-003",
                          max_tokens: int = 1000,
                          temperature: float = 0.5,
                          presence_penalty: float = 0.5,
                          top_p: float = 1,
                          n: int = 1,
                          stop: Optional[str] = None) -> List[dict]:
        print('start completions')
        async with self._request(
            "POST", "https://api.openai.com/v1/completions",
            json={
                "prompt": prompt,
                "model": model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "presence_penalty": presence_penalty,
                "top_p": top_p,
                "n": n,
                "stop": stop,
                "stream": False,  # TODO: may be write
            }
        ) as rsp:
            print('completions end')
            if rsp.status != 200:
                text = await rsp.read()
                raise Exception(f'request failed[statue={rsp.status}]: {text}')
            data = await rsp.json()

        return data["choices"]
