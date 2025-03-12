class Partner:
    name = None

    @staticmethod
    def get_name():
        return Partner.name

    @staticmethod
    def set_name(new_name: str):
        Partner.name = new_name