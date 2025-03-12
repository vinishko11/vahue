from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QLineEdit,
    QFrame
)

from db import database

from SendMessages import *

from frames import MainFrame

class AddPartnerClass(QFrame):
    def __init__(self, main_class_controller):
        QFrame.__init__(self)
        self.controller = main_class_controller
        self.db: database.Database = main_class_controller.db

        self.main_frame_layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        title_label = QLabel("Добавление партнера")
        title_label.setObjectName("Title")
        self.main_frame_layout.addWidget(title_label)

        self.create_hint_label("Введите Имя партнера")
        self.partner_name = self.create_edit_line("Введите имя", 100)

        self.create_hint_label("Введите Телефон партнера")
        self.partner_phone = self.create_edit_line("Введите Телефон", 13)
        self.partner_phone.setInputMask('+7 000 000 00 00') # Добавление маски для ввода

        self.create_hint_label("Введите ИНН партнера")
        self.partner_inn = self.create_edit_line("Введите инн", 10)

        self.create_hint_label("Введите Юридический адрес партнера")
        self.partner_ur_addr = self.create_edit_line("Введите Юр. адрес", 300)

        self.create_hint_label("Введите ФИО директора партнера")
        self.partner_dir = self.create_edit_line("Введите ФИО директора", 100)

        self.create_hint_label("Введите Рейтинг (от 1 до 10) партнера")
        self.partner_rate = self.create_edit_line("Введите рейтинг", 2)

        self.create_hint_label("Введите Электронную почту партнера")
        self.partner_mail = self.create_edit_line("Введите почту", 100)

        self.create_hint_label("Укажите тип партнера")
        self.partner_type = QComboBox()
        self.partner_type.addItems(["ООО", "ОАО", "ПАО", "ЗАО"])
        self.main_frame_layout.addWidget(self.partner_type)

        add_btn = QPushButton("Добавить партнера")
        add_btn.clicked.connect(self.add_partner)
        self.main_frame_layout.addWidget(add_btn)

        back_btn = QPushButton("На главную")
        back_btn.clicked.connect(
            lambda : self.controller.switch_frame(MainFrame.MainFrameClass)
        )
        self.main_frame_layout.addWidget(back_btn)

    def add_partner(self):
        partner_input_data: dict = {
            "type": self.partner_type.currentText(),
            "name": self.partner_name.text(),
            "dir": self.partner_dir.text(),
            "mail": self.partner_mail.text(),
            "phone": self.partner_phone.text()[3:],
            "addr": self.partner_ur_addr.text(),
            "inn": self.partner_inn.text(),
            "rate": int(self.partner_rate.text())
        }

        if self.db.add_new_partner(partner_input_data):
            send_info_message("Партнер добавлен!")
            return
        send_stop_message("Ошибка добавления!")
        return


    def create_hint_label(self, text: str):
        label = QLabel(text)
        label.setObjectName("Hint_label")

        self.main_frame_layout.addWidget(label)

    def create_edit_line(self, placeholder_text: str, max_length: int):

        edit = QLineEdit()
        edit.setPlaceholderText(placeholder_text)
        edit.setMaxLength(max_length)

        self.main_frame_layout.addWidget(edit)

        return edit
