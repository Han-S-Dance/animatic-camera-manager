from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QLabel, QMessageBox, QVBoxLayout

class CustomDialog(QDialog):
    def __init__(self, message, title, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.Ok

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)

        self.layout = QVBoxLayout()
        message = QLabel(message)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

        self.setWindowFlag(Qt.WindowContextHelpButtonHint,False)

class CustomMessageBox(QMessageBox):
    def __init__(self, message, title, yes_text, no_text, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle(title)
        self.setText(message)
        self.addButton(yes_text, QMessageBox.AcceptRole)
        self.addButton(no_text, QMessageBox.RejectRole)
