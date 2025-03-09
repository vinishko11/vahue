from PySide6.QtWidgets import (
    QWidget,
    QStackedWidget,
    QVBoxLayout,
    QApplication
)

import sys

from frames import MainFrame

from db import database

class MainAppClass(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.setWindowTitle("Мастер Пол")
        self.resize(800, 600)

        self.db = database.Database()

        self.frames_container = QStackedWidget()

        main_frame = MainFrame.MainFrameClass(self)
        self.frames_container.addWidget(main_frame)

        layout = QVBoxLayout(self)
        layout.addWidget(
            self.frames_container)



# #67BA80 - Акцентирование внимания
# #F4E8D3 - Дополнительный фон
# #FFFFFF - Основной фон
# Segoe UI - Шрифт
styles_sheet = '''
QPushButton {
background: #67BA80;
color: #000000;
}

QLineEdit {
font-size: 15px;
}


#Title {
font-size: 20px;
qproperty-alignment: AlignCenter;
}

#Hint_label {
font-size: 18px;
padding: 10px, 0px, 0px, 0px;
font-weight: bold;
}

#Main_label {
font-size: 15px;
}

#Card_label {
font-size: 15px;
}

#Card {
border: 2px solid black;
}

#Top_lvl_label {
font-size: 30px;
}

'''

application = QApplication(sys.argv)
application.setStyleSheet(styles_sheet)
application.setFont('Segoe UI')
main_class_object = MainAppClass()
main_class_object.show()
application.exec()