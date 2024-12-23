from PySide6.QtWidgets import (
    QVBoxLayout,
    QFrame,
    QWidget,
    QPushButton,
    QLabel,
    QScrollArea, QHBoxLayout)

import partner
from frames import addPartnerFrame, partnerMoreInfoFrame
from partner import Partner


class MainWindowFrame(QFrame):
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

        # заголовок фрейма
        self.widgetsLayoutContainer.addWidget(QLabel("Список партнеров", objectName="title"))

        # здесь содержатся карточки товаров (создание ниже)
        self.scrollArea = self.createScrollArea()
        self.widgetsLayoutContainer.addWidget(self.scrollArea)

        # добавление карточек партнеров в скролл
        self.scrollArea.setWidget(self.createPartnerCards())

        # кнопка добавить партнера
        self.buttonAddPartner = QPushButton("Добавить партнера", objectName="buttonAddPartner")
        self.buttonAddPartner.clicked.connect(self.showAddPartnerFrame)
        self.widgetsLayoutContainer.addWidget(self.buttonAddPartner)

    # функция области, где содержатся карточки партнеров
    def createScrollArea(self):
        scroll = QScrollArea(self)

        # имя объекта для стилей
        scroll.setObjectName("partnerCard")

        # разрешение на растягивание
        scroll.setWidgetResizable(True)
        return scroll

    # функция создания и заполнение прокрутки карточками партнеров
    def createPartnerCards(self):
        # контейнер для карточек партнеров (сама в ахуе зачем так много разных контейнеров)
        self.containerWidgets = QWidget()
        self.containerWidgets.setObjectName("containerWidgets")
        self.containerWidgets.setContentsMargins(5, 5, 5, 5)
        # вертикальная прокрутка карточек партнеров
        self.verticalScrollContainer = QVBoxLayout(self.containerWidgets)

        # заполнение списка партнеров
        for partners in self.database.takePartnerInfo():
            self.partnerCard = QWidget()
            self.partnerCard.setObjectName("partnerCard")
            # вертикальная разметка для карточек партнеров
            self.partnerCardInfoVertical = QVBoxLayout(self.partnerCard)
            # горизонтальная разметка для карточек партнеров (где название компании и процент скидки
            self.partnerCardInfoHorizontal = QHBoxLayout(self.partnerCard)
            # лейбл названия компании
            self.partnerCardInfoHorizontal.addWidget(QLabel(f'{partners["type"].replace("  ", "")} | {partners["name"].replace("  ", "")}'))
            # лейбл процента скидки
            salePercent = self.takeSaleCount(partners["name"])
            self.partnerCardInfoHorizontal.addWidget(QLabel(f'{salePercent}%', objectName="salePercent"))
            self.partnerCardInfoVertical.addLayout(self.partnerCardInfoHorizontal)
            # лейбл директора
            self.partnerCardInfoVertical.addWidget(QLabel(f'{partners["director"]}'))
            # лейбл номера телефона
            self.partnerCardInfoVertical.addWidget(QLabel(f'+7 {partners["phone"]}'))
            # лейбл рейтинга
            self.partnerCardInfoVertical.addWidget(QLabel(f'Рейтинг: {partners["rate"]}'))

            # кнопка
            self.buttonUpdatePartner = QPushButton("Подробнее", objectName="buttonMore")
            self.buttonUpdatePartner.setObjectName(f"{partners['name'].strip()}")
            self.buttonUpdatePartner.clicked.connect(self.showUpdatePartnerFrame)
            self.partnerCardInfoVertical.addWidget(self.buttonUpdatePartner)

            self.verticalScrollContainer.addWidget(self.partnerCard)
        return self.containerWidgets

    def takeSaleCount(self, partnername: str):
        count: int = self.database.saleSum(partnername)['procent']
        if (count == None):
            return 0
        if (count > 300000):
            return 15
        if (count > 50000):
            return 10
        if (count > 10000):
            return 5
        return 5

    def showAddPartnerFrame(self):
        self.controller.showCurrentFrame(addPartnerFrame.AddPartnerFrame)

    def showUpdatePartnerFrame(self):
        sender = self.sender()
        Partner.setName(sender.objectName())
        self.controller.showCurrentFrame(partnerMoreInfoFrame.PartnerMoreInfoFrame, sender.objectName())