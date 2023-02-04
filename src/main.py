from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from src.constants import Constants
from src.data.api.openai_api import OpenaiApi
from src.data.api.telegram_bot_api.telegram_bot_api import TelegramBotApi
from src.data.api.translator_api import TranslatorApi
from src.settings_ai import SettingsAI


def main():
    completionSettings = SettingsAI()
    openaiApi = OpenaiApi(Constants.openaiApiKey, completionSettings)
    translatorApi = TranslatorApi()
    telegramBotApi = TelegramBotApi(translatorApi, openaiApi, completionSettings)

    application = Application.builder().token(Constants.botToken).build()
    application.add_handler(CommandHandler("start", telegramBotApi.firstLaunch))
    application.add_handler(CallbackQueryHandler(telegramBotApi.settings))

    application.add_handler(MessageHandler(filters.TEXT, telegramBotApi.getCommand))

    # keep_alive()
    application.run_polling()


if __name__ == "__main__":
    main()
