import telegram

from telegram import InlineKeyboardButton
from src.texts.callback_commands_bot import CallbackCommandsBot
from src.texts.commands_bot import CommandsBot


class TelegramBotApiButtons:
    def getSettingsButton(self, temperature, amountImages):
        return telegram.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        f"{CommandsBot.settingsCreativityAI} ({temperature})",
                        callback_data=CallbackCommandsBot.settingsCreativityAI
                    )
                ],
                [
                    InlineKeyboardButton(
                        f"{CommandsBot.settingsAmountImages} ({amountImages})",
                        callback_data=CallbackCommandsBot.settingsAmountImages
                    )
                ],
                [
                    InlineKeyboardButton(
                        CommandsBot.defaultSettings,
                        callback_data=CallbackCommandsBot.settingsToDefault
                    )
                ]
            ],
        )

    def getDefaultButtons(self):
        return telegram.ReplyKeyboardMarkup(
            keyboard=[
                [telegram.KeyboardButton(text=CommandsBot.askQuestion)],
                [telegram.KeyboardButton(text=CommandsBot.getPictureOnRequest)],
                [telegram.KeyboardButton(text=CommandsBot.settings)]
            ],
            resize_keyboard=True
        )
