from openai import AsyncOpenAI

class BaseAgent:
    def __init__(self, client: AsyncOpenAI, model: str):
        self.client = client
        self.model = model

    # This helper makes it easy for every agent to call OpenAI with Structured Outputs
    async def get_structured_response(self, system_prompt: str, user_content: str, response_format):
        response = await self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format=response_format,
        )
        return response.choices[0].message.parsed