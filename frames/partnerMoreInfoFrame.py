from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QFrame, QPushButton

from frames import updatePartnerFrame, mainWindowFrame, historyFrame
from partner import Partner


class PartnerMoreInfoFrame(QFrame):
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
        self.widgetsLayoutContainer =  QVBoxLayout(QWidget(self))

        partnerInfo = self.database.getPartnerByName(Partner.getName())

        # заголовок фрейма
        self.widgetsLayoutContainer.addWidget(QLabel(f"{partnerInfo['name'].strip()}", objectName="Title"))

        # информация о партнере
        self.widgetsLayoutContainer.addWidget(QLabel(f"Имя партнера:"))
        self.widgetsLayoutContainer.addWidget(QLabel(f"{partnerInfo['name'].strip()}", objectName="partner_information_data"))

        self.widgetsLayoutContainer.addWidget(QLabel(f"Телефон партнера:"))
        self.widgetsLayoutContainer.addWidget(QLabel(f"+7 {partnerInfo['phone'].strip()}", objectName="partner_information_data"))

        self.widgetsLayoutContainer.addWidget(QLabel(f"Тип партнера:"))
        self.widgetsLayoutContainer.addWidget(QLabel(f"{partnerInfo['type'].strip()}", objectName="partner_information_data"))

        self.widgetsLayoutContainer.addWidget(QLabel(f"Почта партнера:"))
        self.widgetsLayoutContainer.addWidget(QLabel(f"{partnerInfo['mail'].strip()}", objectName="partner_information_data"))

        self.widgetsLayoutContainer.addWidget(QLabel(f"Юридический адрес партнера:"))
        self.widgetsLayoutContainer.addWidget(QLabel(f"{partnerInfo['address'].strip()}", objectName="partner_information_data"))

        self.widgetsLayoutContainer.addWidget(QLabel(f"ИНН партнера:"))
        self.widgetsLayoutContainer.addWidget(QLabel(f"{partnerInfo['inn'].strip()}", objectName="partner_information_data"))

        self.widgetsLayoutContainer.addWidget(QLabel(f"Рейтинг партнера:"))
        self.widgetsLayoutContainer.addWidget(QLabel(f"{partnerInfo['rate']}", objectName="partner_information_data"))

        self.widgetsLayoutContainer.addWidget(QLabel(f"Директор партнера:"))
        self.widgetsLayoutContainer.addWidget(QLabel(f"{partnerInfo['director'].strip()}", objectName="partner_information_data"))


        self.buttonShowNextFrame = QPushButton("Обновить данные", objectName="buttonNextFrame")
        self.buttonShowNextFrame.clicked.connect(self.showUpdatePartnerFrame)
        self.widgetsLayoutContainer.addWidget(self.buttonShowNextFrame)

        self.buttonHistory = QPushButton("История", objectName="buttonHistory")
        self.buttonHistory.clicked.connect(self.showHistoryFrame)
        self.widgetsLayoutContainer.addWidget(self.buttonHistory)

        self.buttonBack = QPushButton("Назад", objectName="buttonBack")
        self.buttonBack.clicked.connect(self.showMainWindowFrame)
        self.widgetsLayoutContainer.addWidget(self.buttonBack)

    def showHistoryFrame(self):
        self.controller.showCurrentFrame(historyFrame.HistoryFrame, Partner.getName())

    def showUpdatePartnerFrame(self):
        self.controller.showCurrentFrame(updatePartnerFrame.UpdatePartnerFrame, Partner.getName())

    def showMainWindowFrame(self):
        self.controller.showCurrentFrame(mainWindowFrame.MainWindowFrame)