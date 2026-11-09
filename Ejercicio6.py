import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QCheckBox, \
    QStackedLayout, QHBoxLayout, QPushButton, QMessageBox, QGridLayout

from PyQt6.QtGui import QColor, QPalette

class PanelAdministracion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 400)
        layout_principal = QHBoxLayout()
        layout_menu = QVBoxLayout()
        self.stack_layout = QStackedLayout()

        self.btn_inicio = QPushButton("Inicio")
        self.btn_perfil = QPushButton("Perfil")
        self.btn_ajustes = QPushButton("Ajustes")

        vista_inicio = QLabel("Bienvenido a la pantalla de incio")
        vista_perfil = QLabel("Perfil del usuario")
        vista_ajustes = QLabel("Configuracion del sistema")

        layout_menu.addWidget(self.btn_inicio)
        layout_menu.addWidget(self.btn_perfil)
        layout_menu.addWidget(self.btn_ajustes)

        self.stack_layout.addWidget(vista_inicio)
        self.stack_layout.addWidget(vista_perfil)
        self.stack_layout.addWidget(vista_ajustes)

        self.btn_inicio.clicked.connect(self.mostrar_inicio)
        self.btn_perfil.clicked.connect(self.mostrar_perfil)
        self.btn_ajustes.clicked.connect(self.mostrar_ajustes)

        layout_principal.addLayout(layout_menu)
        layout_principal.addLayout(self.stack_layout)
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)
        self.show()


    def mostrar_inicio(self):
        self.stack_layout.setCurrentIndex(0)

    def mostrar_perfil(self):
        self.stack_layout.setCurrentIndex(1)

    def mostrar_ajustes(self):
        self.stack_layout.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PanelAdministracion()
    sys.exit(app.exec())


