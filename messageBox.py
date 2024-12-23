from PySide6.QtWidgets import QMessageBox


def sendInfoMessageBox(messageText: str):
    messageBox = QMessageBox()
    messageBox.setWindowTitle("Информация")
    messageBox.setText(messageText)
    messageBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    messageBox.setDefaultButton(QMessageBox.StandardButton.Yes)
    messageBox.setIcon(QMessageBox.Icon.Information)
    result = messageBox.exec()
    # print(result)
    return result

def send_discard_message_box(message_text: str):
    messageBox = QMessageBox()
    messageBox.setWindowTitle("Информация")
    messageBox.setText(message_text)
    messageBox.setStandardButtons(QMessageBox.StandardButton.Yes |QMessageBox.StandardButton.No)
    messageBox.setDefaultButton(QMessageBox.StandardButton.Yes)
    messageBox.setIcon(QMessageBox.Icon.Warning)
    result = messageBox.exec()
    # print(result)
    return result