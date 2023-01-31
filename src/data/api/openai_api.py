import openai


class OpenaiApi:
    apiKey: str

    def __init__(self, apiKey):
        openai.api_key = apiKey

    def getAnswerToQuestion(self, question):
        result = openai.Completion.create(
            model="text-davinci-003",
            prompt=question,
            temperature=0.5,
            max_tokens=2048,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return result.choices[0].text

