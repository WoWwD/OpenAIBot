from telegram import Update, InputMediaPhoto
from telegram.ext import ContextTypes, CallbackContext
from src.texts.callback_commands_bot import CallbackCommandsBot
from src.texts.commands_bot import CommandsBot
from src.data.api.openai_api import OpenaiApi
from src.data.api.telegramBotApi.telegramBotApiButtons.telegram_bot_api_buttons import TelegramBotApiButtons
from src.data.api.translator_api import TranslatorApi
from src.settings_ai import SettingsAI
from src.texts.answers import Answers


class TelegramBotApi(TelegramBotApiButtons):
    translatorApi: TranslatorApi
    openaiApi: OpenaiApi
    settingsAI: SettingsAI

    def __init__(self, translatorApi, openaiApi, settingsAI):
        self.translatorApi = translatorApi
        self.openaiApi = openaiApi
        self.settingsAI = settingsAI

    async def firstLaunch(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(CommandsBot.default, reply_markup=self.getDefaultButtons())

    async def getAnswerToQuestion(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        questionOnEnglish = self.translatorApi.toLanguage(update.message.text, "en")
        answerOnEnglish = self.openaiApi.completionCreate(questionOnEnglish + "?")
        answerOnRussian = self.translatorApi.toLanguage(answerOnEnglish, "ru")
        await update.message.reply_text(text=f"Eng:{answerOnEnglish}\n\nRus:\n\n{answerOnRussian}")

    async def getImageByPrompt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        answerOnEnglish = self.openaiApi.completionCreate(update.message.text)
        result = self.openaiApi.imageCreate(answerOnEnglish)
        if not result:
            await update.message.reply_text(text=Answers.forbiddenText)
        else:
            media_group = []
            for images in result:
                media_group.append(InputMediaPhoto(media=images))
            await update.message.reply_media_group(media=media_group)

    async def getCommand(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.message.text == CommandsBot.askQuestion:
            CommandsBot.current = CommandsBot.askQuestion
            await update.message.reply_text(Answers.askQuestion)
        elif update.message.text == CommandsBot.getPictureOnRequest:
            CommandsBot.current = CommandsBot.getPictureOnRequest
            await update.message.reply_text(Answers.enterText)
        elif update.message.text == CommandsBot.settings:
            CommandsBot.current = CommandsBot.default
            await update.message.reply_text(
                CommandsBot.choose,
                reply_markup=self.getSettingsButton(
                    self.settingsAI.temperature,
                    self.settingsAI.amountImages
                )
            )
        elif CommandsBot.current == CommandsBot.settingsCreativityAI:
            result = self.settingsAI.setTemperature(value=float(update.message.text))
            if result:
                CommandsBot.current = CommandsBot.default
                await update.message.reply_text(text=Answers.settingsChanged)
            else:
                await update.message.reply_text(text=Answers.wrongFormat)
        elif CommandsBot.current == CommandsBot.settingsAmountImages:
            result = self.settingsAI.setAmountImages(value=int(update.message.text))
            if result:
                CommandsBot.current = CommandsBot.default
                await update.message.reply_text(text=Answers.settingsChanged)
            else:
                await update.message.reply_text(text=Answers.wrongFormat)
        elif CommandsBot.current == CommandsBot.default:
            await update.message.reply_text(Answers.default)
        else:
            await update.message.reply_text(Answers.waiting)
            if CommandsBot.current == CommandsBot.askQuestion:
                await self.getAnswerToQuestion(update, ContextTypes.DEFAULT_TYPE)
            if CommandsBot.current == CommandsBot.getPictureOnRequest:
                await self.getImageByPrompt(update, ContextTypes.DEFAULT_TYPE)

    async def settings(self, update: Update, context: CallbackContext):
        query = update.callback_query
        choice = query.data

        if choice == CallbackCommandsBot.settingsCreativityAI:
            CommandsBot.current = CommandsBot.settingsCreativityAI
            await update.callback_query.message.edit_text(text=Answers.setCreativityAI)
        if choice == CallbackCommandsBot.settingsAmountImages:
            CommandsBot.current = CommandsBot.settingsAmountImages
            await update.callback_query.message.edit_text(text=Answers.setAmountImages)
        if choice == CallbackCommandsBot.settingsToDefault:
            self.settingsAI.toDefault()
            await update.callback_query.message.edit_text(text=Answers.settingsChanged)
