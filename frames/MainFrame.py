from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QFrame

)

from PySide6.QtGui import (
    QPixmap
)

from db import database

from frames import AddPartnerFrame, PartnerInfoFrame, UpdatePartnerFrame


class MainFrameClass(QFrame):
    # Класс для главного окна приложения с карточками партнеров
    def __init__(self, main_class_controller):
        # Инициализация главного окна
        QFrame.__init__(self)
        self.controller = main_class_controller
        self.db: database.Database = main_class_controller.db

        self.main_frame_layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        # Настройка интерфейса главного окна - создание заголовка,
        # области прокрутки и кнопки добавления партнера
        title_label = QLabel("Карточки партнеров")
        title_label.setObjectName("Title")
        self.main_frame_layout.addWidget(title_label)

        self.add_picture()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(
            self.create_partners_cards())

        self.main_frame_layout.addWidget(scroll_area)

        add_partner_btn = QPushButton("Добавить нового партнера")
        add_partner_btn.clicked.connect(
            lambda: self.controller.switch_frame(AddPartnerFrame.AddPartnerClass)
        )

        self.main_frame_layout.addWidget(add_partner_btn)

    def add_picture(self):
        # Добавление логотипа в интерфейс
        picture_place = QLabel()
        picture_read = QPixmap('D:\\Education\\vahue\\icons\\icon.png')

        picture_place.setScaledContents(True)
        picture_place.setFixedSize(52, 52)
        picture_place.setPixmap(picture_read)

        hbox = QHBoxLayout()
        hbox.addWidget(QWidget())
        hbox.addWidget(picture_place)
        hbox.addWidget(QWidget())

        self.main_frame_layout.addLayout(hbox)

    def calculate_discount(self, partner_name: str):
        # Расчет скидки для партнера на основе количества продаж
        count = self.db.take_count_of_sales(partner_name)
        if count == None:
            return 0
        elif count > 300_000:
            return 15
        elif count > 50_000:
            return 10
        elif count > 10000:
            return 5
        return 0

    def create_partners_cards(self):
        # Создание карточек с информацией о каждом партнере
        cards_container = QWidget()
        self.cards_container_layout = QVBoxLayout(cards_container)

        for partner_information in self.db.take_all_partners_info():
            card = QWidget()
            card.setObjectName(f"Card")

            card_layout = QVBoxLayout()
            card.setLayout(card_layout)

            card_top_level_hbox = QHBoxLayout()
            partner_type_label = QLabel(f'{partner_information["type"]} | {partner_information["name"]}')
            partner_type_label.setStyleSheet('QLabel {font-size: 18px}')

            partner_discount_label = QLabel(f'{self.calculate_discount(partner_information["name"])}%')
            partner_discount_label.setStyleSheet('QLabel {qproperty-alignment: AlignRight; font-size: 18px}')

            card_top_level_hbox.addWidget(partner_type_label)
            card_top_level_hbox.addWidget(partner_discount_label)

            card_layout.addLayout(card_top_level_hbox)

            dir_label = QLabel(f"{partner_information['dir']}")
            dir_label.setObjectName("Card_label")

            phone_label = QLabel(f"+7 {partner_information['phone']}")
            phone_label.setObjectName("Card_label")

            rate_label = QLabel(f"Рейтинг: {partner_information['rate']}")
            rate_label.setObjectName("Card_label")

            partner_card_button = QPushButton("Подробнее")
            partner_card_button.setAccessibleName(f"{partner_information['name']}")
            partner_card_button.clicked.connect(
                self.open_partner_info_frame
            )

            update_btn = QPushButton("Редактировать")
            update_btn.setAccessibleName(f"{partner_information['name']}")
            update_btn.clicked.connect(
                self.open_update_info_frame
            )
            card_layout.addWidget(dir_label)
            card_layout.addWidget(phone_label)
            card_layout.addWidget(rate_label)
            card_layout.addWidget(partner_card_button)
            card_layout.addWidget(update_btn)

            self.cards_container_layout.addWidget(card)

        return cards_container

    def open_partner_info_frame(self):
        # Открытие окна с подробной информацией о партнере
        sender = self.sender()
        partner_name = sender.accessibleName()
        self.controller.switch_frame(PartnerInfoFrame.PartnerInfoClass, partner_name)


    def open_update_info_frame(self):
        # Открытие окна для редактирования информации о партнере
        sender = self.sender()
        partner_name = sender.accessibleName()
        self.controller.switch_frame(UpdatePartnerFrame.UpdatePartnerClass, partner_name)
