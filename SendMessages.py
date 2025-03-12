from PySide6.QtWidgets import (
    QMessageBox
)


def send_info_message(message_text: str):
    messageBox = QMessageBox()
    messageBox.setText(message_text)
    messageBox.setIcon(QMessageBox.Icon.Information)
    messageBox.setStandardButtons(QMessageBox.StandardButton.Yes)
    result = messageBox.exec()
    return result

def send_warning_message(message_text: str):
    message = QMessageBox()
    message.setText(message_text)
    message.setIcon(QMessageBox.Icon.Warning)
    message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    user_result = message.exec()
    print(user_result, "RESULT")
    return user_result

def send_stop_message(message_text: str):
    message = QMessageBox()
    message.setText(message_text)
    message.setIcon(QMessageBox.Icon.Critical)
    message.setStandardButtons(QMessageBox.StandardButton.Yes)
    user_result = message.exec()
    return user_result
