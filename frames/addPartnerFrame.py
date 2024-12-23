from PySide6.QtWidgets import QFrame, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit

import messageBox
from frames import mainWindowFrame

class AddPartnerFrame(QFrame):
    def __init__(self, parent, controller):
        QFrame.__init__(self, parent)
        self.controller = controller
        self.database = self.controller.database

        # заполняем данными фрейм
        self.updateStartValues()

        # установка разметки
        self.setLayout(self.widgetsLayoutContainer)

    def updateStartValues(self):
        # контейнер для виджетов
        self.widgetsLayoutContainer = self.widgetsLayoutContainer =  QVBoxLayout(QWidget(self))

        # заголовок окна
        self.widgetsLayoutContainer.addWidget(QLabel("Добавление партнера", objectName="title"))

        # поля ввода
        self.widgetsLayoutContainer.addWidget(QLabel("Введите имя"))
        self.inputPartnerName = self.createPaternQLineEdit("Ввод имени")

        self.widgetsLayoutContainer.addWidget(QLabel("Введите тип партнера"))
        self.inputPartnerType = self.createPaternQLineEdit("Ввод типа партнера")

        self.widgetsLayoutContainer.addWidget(QLabel("Введите имя директора"))
        self.inputPartnerDirector = self.createPaternQLineEdit("Ввод имени директора")

        self.widgetsLayoutContainer.addWidget(QLabel("Введите номер телефона"))
        self.inputPartnerPhone = self.createPaternQLineEdit("Ввод номера телефона")

        self.widgetsLayoutContainer.addWidget(QLabel("Введите почту"))
        self.inputPartnerMail = self.createPaternQLineEdit("Ввод почты")

        self.widgetsLayoutContainer.addWidget(QLabel("Введите юридический адрес"))
        self.inputPartnerAddress = self.createPaternQLineEdit("Ввод юридического адреса")

        self.widgetsLayoutContainer.addWidget(QLabel("Введите инн"))
        self.inputPartnerInn = self.createPaternQLineEdit("Ввод инн")

        self.widgetsLayoutContainer.addWidget(QLabel("Введите рейтинг"))
        self.inputPartnerRate = self.createPaternQLineEdit("Ввод рейтинга")

        self.buttonAddPartnerToDB = QPushButton("Добавить партнера", objectName="buttonAddPartnerToDB")
        self.buttonAddPartnerToDB.clicked.connect(self.addPartnerToDB)
        self.widgetsLayoutContainer.addWidget(self.buttonAddPartnerToDB)

        self.buttonBack = QPushButton("Назад", objectName="buttonBack")
        self.buttonBack.clicked.connect(self.showMainWindowFrame)
        self.widgetsLayoutContainer.addWidget(self.buttonBack)

    def createPaternQLineEdit(self, placeHolderText):
        inputText = QLineEdit()
        inputText.setPlaceholderText(placeHolderText)
        self.widgetsLayoutContainer.addWidget(inputText)
        return inputText

    def addPartnerToDB(self):
        infoFromUser: dict = {"name": self.inputPartnerName.text(),
                             "type": self.inputPartnerType.text(),
                             "director": self.inputPartnerDirector.text(),
                             "phone": self.inputPartnerPhone.text()[3:],
                             "mail": self.inputPartnerMail.text(),
                             "address": self.inputPartnerAddress.text(),
                             "inn": self.inputPartnerInn.text(),
                             "rate": self.inputPartnerRate.text(),
                             }
        if self.database.addPartner(infoFromUser):
            messageBox.sendInfoMessageBox("Партнер успешно добавлен")
            return
        messageBox.sendInfoMessageBox("Ошибка добавления партнера")
        return

    def showMainWindowFrame(self):
        self.controller.showCurrentFrame(mainWindowFrame.MainWindowFrame)