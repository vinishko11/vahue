from PySide6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

import messageBox
from frames import partnerMoreInfoFrame
from partner import Partner


class UpdatePartnerFrame(QFrame):
    def __init__(self, parent, controller):
        QFrame.__init__(self, parent)
        self.controller = controller
        self.database = self.controller.database

        # заполняем данными фрейм
        self.updateStartValues()

        # установка разметки
        self.setLayout(self.widgetsLayoutContainer)

    # функция для обновления данных на актуальные
    def updateStartValues(self):
        # контейнер для виджетов
        self.widgetsLayoutContainer = QVBoxLayout(QWidget(self))

        # начальные данные о партнере
        self.latestPartnerInfo = self.database.getPartnerByName(Partner.getName())

        # заголовок фрейма
        self.widgetsLayoutContainer.addWidget(QLabel("Обновление партнера", objectName="title"))

        # поля ввода
        self.widgetsLayoutContainer.addWidget(QLabel("Имя партнера"))
        self.inputPartnerName = self.createPatternQLineEdit(self.latestPartnerInfo['name'].strip())

        self.widgetsLayoutContainer.addWidget(QLabel("Тип партнера"))
        self.inputPartnerType = self.createPatternQLineEdit(self.latestPartnerInfo['type'].strip())

        self.widgetsLayoutContainer.addWidget(QLabel("Имя директора партнера"))
        self.inputPartnerDirector = self.createPatternQLineEdit(self.latestPartnerInfo['director'].strip())

        self.widgetsLayoutContainer.addWidget(QLabel("Электронная почта партнера"))
        self.inputPartnerMail = self.createPatternQLineEdit(self.latestPartnerInfo['mail'].strip())

        self.widgetsLayoutContainer.addWidget(QLabel("Номер телефона партнера"))
        self.inputPartnerPhone = self.createPatternQLineEdit(f'+7 {self.latestPartnerInfo["phone"].strip()}')

        self.widgetsLayoutContainer.addWidget(QLabel("Юридический адрес партнера"))
        self.inputPartnerAddress = self.createPatternQLineEdit(self.latestPartnerInfo['address'].strip())

        self.widgetsLayoutContainer.addWidget(QLabel("Инн партнера"))
        self.inputPartnerInn = self.createPatternQLineEdit(self.latestPartnerInfo['inn'].strip())

        self.widgetsLayoutContainer.addWidget(QLabel("Рейтинг партнера"))
        self.inputPartnerRate = self.createPatternQLineEdit(self.latestPartnerInfo['rate'])

        self.buttonUpdatePartnerInDB = QPushButton("Обновить данные", objectName="buttonUpdatePartnerInDB")
        self.buttonUpdatePartnerInDB.clicked.connect(self.updatePartnerInDB)
        self.widgetsLayoutContainer.addWidget(self.buttonUpdatePartnerInDB)

        self.buttonBack = QPushButton("Назад", objectName="buttonBack")
        self.buttonBack.clicked.connect(self.showPartnerMoreInfoFrame)
        self.widgetsLayoutContainer.addWidget(self.buttonBack)

    def createPatternQLineEdit(self, latestInfo: str):
        latestText = QLineEdit(self)
        latestText.setText(latestInfo)
        self.widgetsLayoutContainer.addWidget(latestText)
        return latestText

    def updatePartnerInDB(self):
        latestPartnerInfo: dict = {"name": self.inputPartnerName.text(),
                              "type": self.inputPartnerType.text(),
                              "director": self.inputPartnerDirector.text(),
                              "mail": self.inputPartnerMail.text(),
                              "phone": self.inputPartnerPhone.text()[3:],
                              "address": self.inputPartnerAddress.text(),
                              "inn": self.inputPartnerInn.text(),
                              "rate": self.inputPartnerRate.text(),
                              }
        if self.database.updatePartner(latestPartnerInfo):
            messageBox.sendInfoMessageBox("Данные успешно обновлены")
            Partner.setName(self.inputPartnerName.text())
            return
        messageBox.sendInfoMessageBox("Ошибка обновления данных")
        return

    def showPartnerMoreInfoFrame(self):
        self.controller.showCurrentFrame(partnerMoreInfoFrame.PartnerMoreInfoFrame)