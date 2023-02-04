class SettingsAI:
    temperature = 0.5
    amountImages = 5

    def toDefault(self):
        self.temperature = 0.5
        self.amountImages = 5

    def setTemperature(self, value) -> bool:
        if 0 <= value <= 0.9:
            self.temperature = value
            return True
        else:
            return False

    def setAmountImages(self, value) -> bool:
        if 1 <= value <= 10:
            self.amountImages = value
            return True
        else:
            return False
