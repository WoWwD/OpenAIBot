from telegram import Update
from telegram.ext import ContextTypes
from src.data.api.openai_api import OpenaiApi
from src.data.api.transalator_api import TranslatorApi


class TelegramBotApi:
    translatorApi: TranslatorApi
    openaiApi: OpenaiApi

    def __init__(self, translatorApi, openaiApi):
        self.translatorApi = translatorApi
        self.openaiApi = openaiApi

    async def firstLaunch(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Ahoj!")

    async def getAnswerToQuestion(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        questionOnEnglish = self.translatorApi.toLanguage(update.message.text, "en")
        answerOnEnglish = self.openaiApi.getAnswerToQuestion(questionOnEnglish + "?")
        answerOnRussian = self.translatorApi.toLanguage(answerOnEnglish, "ru")
        await update.message.reply_text(text=f"Eng:{answerOnEnglish}\n\nRus:\n\n{answerOnRussian}")
