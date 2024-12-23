class Partner:
    name = None

    @staticmethod
    def getName():
        return Partner.name

    @staticmethod
    def setName(newName: str):
        Partner.name = newName.strip()