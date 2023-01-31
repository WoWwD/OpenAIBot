import telegram

from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes
from src.commands_bot import CommandsBot
from src.data.api.openai_api import OpenaiApi
from src.data.api.transalator_api import TranslatorApi
from src.settings_bot import SettingsBot


class TelegramBotApi:
    translatorApi: TranslatorApi
    openaiApi: OpenaiApi

    def __init__(self, translatorApi, openaiApi):
        self.translatorApi = translatorApi
        self.openaiApi = openaiApi

    async def firstLaunch(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = telegram.ReplyKeyboardMarkup(
            keyboard=[
                [telegram.KeyboardButton(text=CommandsBot.askQuestion)],
                [telegram.KeyboardButton(text=CommandsBot.getPictureOnRequest)]
            ],
            resize_keyboard=True
        )
        await update.message.reply_text(CommandsBot.firstLaunch, reply_markup=keyboard)

    async def handlerMessages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if await self.isCommands(update):
            return
        else:
            await update.message.reply_text("Думаю...")
            await self.getFunc(update, ContextTypes.DEFAULT_TYPE)

    async def getAnswerToQuestion(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        questionOnEnglish = self.translatorApi.toLanguage(update.message.text, "en")
        answerOnEnglish = self.openaiApi.completionCreate(questionOnEnglish + "?")
        answerOnRussian = self.translatorApi.toLanguage(answerOnEnglish, "ru")
        await update.message.reply_text(text=f"Eng:{answerOnEnglish}\n\nRus:\n\n{answerOnRussian}")

    async def getImageByPrompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        answerOnEnglish = self.openaiApi.completionCreate(update.message.text)
        result = self.openaiApi.imageCreate(answerOnEnglish)
        media_group = []
        for images in result:
            media_group.append(InputMediaPhoto(media=images))
        await update.message.reply_media_group(media=media_group)

    async def isCommands(self, update: Update) -> bool:
        if update.message.text == CommandsBot.askQuestion:
            SettingsBot.numberCommand = 1
            await update.message.reply_text("Введи вопрос и я попробую ответить на него")
            return True
        elif update.message.text == CommandsBot.getPictureOnRequest:
            SettingsBot.numberCommand = 2
            await update.message.reply_text("Введи текст и я создам по нему изображение")
            return True
        else:
            return False

    async def getFunc(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if SettingsBot.numberCommand == 1:
            await self.getAnswerToQuestion(update, ContextTypes.DEFAULT_TYPE)
        if SettingsBot.numberCommand == 2:
            await self.getImageByPrompt(update, ContextTypes.DEFAULT_TYPE)


