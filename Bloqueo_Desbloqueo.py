import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QCheckBox, \
    QStackedLayout, QHBoxLayout, QPushButton, QMessageBox, QGridLayout

from PyQt6.QtGui import QColor, QPalette

class FormularioUsuario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Perfil de Usuario (Modo lectura)")
        self.setMinimumSize(400, 300)
        layout_principal = QVBoxLayout()

        nombre = QLabel("Nombre")
        email = QLabel("Email")
        telefono = QLabel("Telefono")

        self.lnombre = QLineEdit()
        self.lemail = QLineEdit()
        self.ltelefono = QLineEdit()

        self.lnombre.setPlaceholderText("Nombre")
        self.lemail.setPlaceholderText("Email")
        self.ltelefono.setPlaceholderText("Telefono")

        self.lnombre.setEnabled(False)
        self.lemail.setEnabled(False)
        self.ltelefono.setEnabled(False)

        self.btn_editar = QPushButton("Editar")
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setEnabled(False)

        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(self.btn_editar)
        layout_horizontal.addWidget(self.btn_guardar)

        layout_principal.addWidget(nombre)
        layout_principal.addWidget(self.lnombre)
        layout_principal.addWidget(email)
        layout_principal.addWidget(self.lemail)
        layout_principal.addWidget(telefono)
        layout_principal.addWidget(self.ltelefono)
        layout_principal.addLayout(layout_horizontal)

        self.btn_editar.clicked.connect(self.habilitar_edicion)
        self.btn_guardar.clicked.connect(self.guardar_cambios)


        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)
        self.show()


    def habilitar_edicion(self):

        self.lnombre.setEnabled(True)
        self.ltelefono.setEnabled(True)
        self.lemail.setEnabled(True)

        self.btn_guardar.setEnabled(True)
        self.btn_editar.setEnabled(False)


    def guardar_cambios(self):
        if not self.lnombre.text().strip() or not self.ltelefono.text().strip() or not self.lemail.text().strip()  :
            QMessageBox.warning(self, "Campos vacíos", "Todos los campos deben estar rellenos.")
        else:
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente.")
            self.lnombre.setEnabled(False)
            self.ltelefono.setEnabled(False)
            self.lemail.setEnabled(False)

            self.btn_guardar.setEnabled(False)
            self.btn_editar.setEnabled(True)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = FormularioUsuario()
    sys.exit(app.exec())






