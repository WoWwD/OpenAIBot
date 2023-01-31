import openai


class OpenaiApi:
    apiKey: str

    def __init__(self, apiKey):
        openai.api_key = apiKey

    def completionCreate(self, question):
        result = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0.5,
            max_tokens=2048,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return result.choices[0].text

    def imageCreate(self, prompt):
        result = openai.Image.create(
            prompt=prompt,
            n=5,
            size="512x512",
        )
        result2 = result["data"]
        images = []
        for img in result2:
            images.append(img["url"])

        return images


