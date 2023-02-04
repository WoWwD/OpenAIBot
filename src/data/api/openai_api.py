import openai

from src.settings_ai import SettingsAI


class OpenaiApi:
    settingsAI: SettingsAI
    apiKey: str

    def __init__(self, apiKey, completionSettings):
        openai.api_key = apiKey
        self.settingsAI = completionSettings

    def completionCreate(self, question):
        result = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=self.settingsAI.temperature,
            max_tokens=2048,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return result.choices[0].text

    def imageCreate(self, prompt):
        try:
            result = openai.Image.create(
                prompt=prompt,
                n=self.settingsAI.amountImages,
                size="512x512",
            )
            result2 = result["data"]
            images = []
            for img in result2:
                images.append(img["url"])
            return images
        except openai.error.InvalidRequestError:
            return False
