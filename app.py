import sys
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QStackedWidget,
    QApplication,
    QVBoxLayout,
    QWidget)

from frames import mainWindowFrame
from db.database import Database
from partner import Partner


class Application(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Мастер пол")
        self.resize(QSize(800, 800))
        self.setMaximumSize(QSize(800, 800))
        self.setObjectName("mainWindowWidget")
        icon = QIcon()
        icon.addPixmap(QPixmap("res/icon.ico"))
        self.setWindowIcon(icon)

        # инициализация базы данных
        self.database = Database()
        # инициализация стартового фрейма
        self.mainWindowFrame = mainWindowFrame.MainWindowFrame(self, self)
        # создаем контейнер для фреймов
        self.framesContainer = QStackedWidget()
        # стартовый фрейм в контейнер
        self.framesContainer.addWidget(self.mainWindowFrame)
        # макет для фреймов из контейнера
        self.framesContainerLayout = QVBoxLayout(self)
        # добавляем контейнер в планировщик
        self.framesContainerLayout.addWidget(self.framesContainer)

    def showCurrentFrame(self, frame, partnername: str = Partner.getName()):
        currentFrame = frame(self, self)
        # self.framesContainer.removeWidget(currentFrame)
        if partnername:
            Partner.setName(partnername)

        self.framesContainer.addWidget(currentFrame)
        self.framesContainer.setCurrentWidget(currentFrame)

StyleSheet = '''
#mainWindowWidget {
    background: #FFFFFF;
}

#partnerCard {
    background-color: #F4E8D3;
}

QMessageBox {
    background: #FFFFFF;
}

QVBoxLayout {
    background: #F4E8D3;
}
QLabel {
    color: #000000;
    font-size: 16px;
}

/* цвет всех заголовков */
#title {
    color: #000000;
    font-size: 25px;
    font-weight: bold;
    qproperty-alignment: AlignCenter;
}

/* белая подложка в области прокрутки */
#containerWidgets {
    background: #FFFFFF;
}

/* стиль для полей ввода */
QLineEdit {
    height: 40px;
    color: #000000;
    background: #FFFFFF
}

/* зеленый цвет и черные буквы для кнопок */
QPushButton {
    background: #67BA80;
    color: #000000;
    height: 30px;
    font-size: 18px;
}

/* бежевый цвет для подложек карточек партнеров */
#partnerCard, #scroll_widgets_contents{
    background: #F4E8D3;
}

/* стиль для скидки */
#salePercent {
    background: #F4E8D3;
    color: #000000;
    qproperty-alignment: AlignRight;
}

/* бежевый цвет для карточек партнеров */
#Partner_name, #Partner_phone, #partner_information_data, #text_enter_hint{
    background: #F4E8D3;
    color: #000000;
    padding: 0px 0px 0px 10px;
}
'''

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Установка стилей
    app.setStyleSheet(StyleSheet)

    # Инициализация приложения
    mainWindow = Application()
    mainWindow.setWindowIcon(QIcon("res/icon.ico"))

    # Демонстрация главного окна
    mainWindow.show()
    sys.exit(app.exec())