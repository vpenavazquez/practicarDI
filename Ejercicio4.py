import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout, QPushButton, QMessageBox

from PyQt6.QtGui import QColor, QPalette


class FormularioRegistro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Registro Usuario")
        self.setMinimumSize(350, 250)

        layout = QVBoxLayout()

        nombre = QLabel("Nombre")
        self.txt_nombre = QLineEdit()
        email = QLabel("Email")
        self.txt_email = QLineEdit()
        password = QLabel("Password")
        self.txt_password = QLineEdit()

        self.txt_nombre.setPlaceholderText("Ingrese un nombre")
        self.txt_email.setPlaceholderText("Ingrese un email")
        self.txt_password.setPlaceholderText("Ingrese un password")
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)


        perfil = QLabel("Perfil")
        self.combo_perfil = QComboBox()

        self.combo_perfil.addItems(["Estudiante", "Profesor", "Invitado"])

        self.chk_terminos = QCheckBox("Acepto los términos y condiciones")

        self.btn_registrar = QPushButton("Registrar")

        layout.addWidget(nombre)
        layout.addWidget(self.txt_nombre)
        layout.addWidget(email)
        layout.addWidget(self.txt_email)
        layout.addWidget(password)
        layout.addWidget(self.txt_password)

        layout.addWidget(perfil)
        layout.addWidget(self.combo_perfil)
        layout.addWidget(self.chk_terminos)
        layout.addWidget(self.btn_registrar)

        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)
        self.btn_registrar.clicked.connect(self.validar_registro)

        self.show()

    def validar_registro(self):
        nombre = self.txt_nombre.text().strip()
        email = self.txt_email.text().strip()
        password = self.txt_password.text().strip()

        if not nombre or not email or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return False

        if "@" not in email:
            QMessageBox.warning(self, "Error", "El email debe ser válido (debe incluir '@')")
            return

        if not self.chk_terminos.isChecked():
            QMessageBox.warning(self, "Error", "Debes aceptar los términos y condiciones.")
            return

        perfil_elegido = self.combo_perfil.currentText()
        QMessageBox.information(self, "LETSGO", "Registro perfe")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FormularioRegistro()
    sys.exit(app.exec())