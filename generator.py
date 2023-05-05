from typing import List
from openai_client import OpenAIClient


class Generator:
    def __init__(self,
                 oai_client: OpenAIClient,
                 prompt_file: str = "./prompts/prompt.txt") -> None:
        self.oai_client = oai_client
        with open(prompt_file, "r", encoding="utf-8") as f:
            self.prompt = f.read()

    async def make_new_line(self,
                            class_line: str,
                            text_line: str,
                            temperature: float,
                            presence_penalty: float
                            ) -> str:
        p = (
            self.prompt
            .replace("<CLASS>", class_line)
            .replace("<TEXT>", text_line)
        )
        result = await self.oai_client.completions(
            prompt=p,
            temperature=temperature,
            presence_penalty=presence_penalty,
            max_tokens=500,
            n=1,
            stop="\n"
        )
        return result[0]["text"]
