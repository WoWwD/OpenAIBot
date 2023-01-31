from telegram.ext import Application, CommandHandler, MessageHandler, filters
from src.background import keep_alive
from src.constants import Constants
from src.data.api.openai_api import OpenaiApi
from src.data.api.telegram_bot_api import TelegramBotApi
from src.data.api.transalator_api import TranslatorApi


def main():
    openaiApi = OpenaiApi(Constants.openaiApiKey)
    translatorApi = TranslatorApi()
    telegramBotApi = TelegramBotApi(translatorApi, openaiApi)

    application = Application.builder().token(Constants.botToken).build()
    application.add_handler(CommandHandler("start", telegramBotApi.firstLaunch))
    application.add_handler(MessageHandler(filters.TEXT, telegramBotApi.getAnswerToQuestion))

    # keep_alive()
    application.run_polling()


if __name__ == "__main__":
    main()
