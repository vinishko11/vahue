from PySide6.QtWidgets import (
    QVBoxLayout,  # Разметка, которая размещает объекты вертикально
    QLabel,  # Текстовое поле для объектов
    QPushButton,  # Кнопка для пользователя
    QLineEdit,  # Поле для текстового ввода
    QFrame  # Нужно для сборки фрейма
)

from db import database

from Partner import Partner

from frames import MainFrame, HistoryFrame


class PartnerInfoClass(QFrame):
    def __init__(self, main_class_controller):
        QFrame.__init__(self)
        self.controller = main_class_controller
        self.db: database.Database = main_class_controller.db

        self.main_frame_layout = QVBoxLayout(self)
        self.setup_ui()

    def setup_ui(self):
        title_label = QLabel("Информация о партнере")
        title_label.setObjectName("Title")
        self.main_frame_layout.addWidget(title_label)
        labels_hints = [
            "Тип партнера",
            "Имя партнера",
            "Директор партнера",
            "Почта партнера",
            "Телефон партнера",
            "Юридический адрес партнера",
            "ИНН партнера",
            "Рейтинг партнера",
        ]
        hints_index = 0
        for key, value in self.db.take_partner_info(Partner.get_name()).items():
            self.create_hint_label(labels_hints[hints_index])
            hints_index += 1
            self.create_main_label(value)

        history_btn = QPushButton("История продаж партнера")
        history_btn.clicked.connect(
            lambda: self.controller.switch_frame(HistoryFrame.HistoryFrameClass)
        )

        back_btn = QPushButton("На главную")
        back_btn.clicked.connect(
            lambda: self.controller.switch_frame(MainFrame.MainFrameClass)
        )
        self.main_frame_layout.addWidget(history_btn)
        self.main_frame_layout.addWidget(back_btn)

    def create_hint_label(self, text: str):
        label = QLabel(text)
        label.setObjectName("Hint_label")
        self.main_frame_layout.addWidget(label)

    def create_main_label(self, text: str):
        label = QLabel(str(text))
        label.setObjectName("Main_label")
        self.main_frame_layout.addWidget(label)
