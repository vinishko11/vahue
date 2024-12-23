import re

def checkNameString(partnername: str):
    if (str(partnername) and len(partnername) > 0):
        return True
    print("Неверное имя компании")
    return False

def checkTypeString(partnertype: str):
    if (partnertype in ["ЗАО", "ООО", "ПАО", "ОАО"] and len(partnertype) == 3):
        return True
    print("Неверный тип компании")
    return False

def checkDirectorString(partnerdirector: str):
    if (len(partnerdirector.split(' ')) == 3 and str(partnerdirector)):
        return True
    print("Неверное имя директора")
    return False

def checkPhoneString(partnerphone: str):
    try:
        regex = re.compile(r'[0-9][0-9][0-9] [0-9][0-9][0-9] [0-9][0-9] [0-9][0-9]')
        if re.fullmatch(regex, partnerphone):
            return True
        print("Неверный номер телефона")
        return False
    except Exception:
        print("Неверный номер телефона")
        return False

def checkMailString(partnermail: str):
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if re.fullmatch(regex, partnermail):
        return True
    print("Неверная почта")
    return False

def checkAddressString(partneraddress: str):
    if (len(partneraddress.split(',')[0]) == 6 and partneraddress.split(',')[0].isdigit() and len(partneraddress[6:]) > 1):
        return True
    print("Неверный адрес компании")
    return False

def checkInnString(partnerinn: str):
    try:
        if (partnerinn.isdigit() and len(partnerinn) == 10):
            return True
        print("Неверный номер ИНН компании")
        return False
    except Exception:
        print("Неверный номер ИНН компании")
        return False

def checkRate(partnerrate):
    try:
        if (int(partnerrate) in range(1, 11)):
            return True
        print("Неверный рейтинг компании")
        return False
    except Exception:
        print("Неверный рейтинг компании")
        return False

def checkInputInfo(infoFromUser: dict):
    try:
        if (checkNameString(infoFromUser["name"]) and
            checkTypeString(infoFromUser["type"]) and
            checkDirectorString(infoFromUser["director"]) and
            checkPhoneString(infoFromUser["phone"]) and
            checkMailString(infoFromUser["mail"]) and
            checkAddressString(infoFromUser["address"]) and
            checkInnString(infoFromUser["inn"]) and
            checkRate(infoFromUser["rate"])):
            return True
        else:
            return False
    except Exception:
        return False

# infoFromUser: dict = {
#     "type": "ООО",
#     "name": "Винлаб",
#     "director": "Беляева Алина Альбертовна",
#     "mail": "alinabelyaeva@mail.ru",
#     "phone": "985 865 17 70",
#     "address": "199933, Москва, ул. Образцова, 14",
#     "inn": "1234567890",
#     "rate": 10
# }
# print(checkInputInfo(infoFromUser))