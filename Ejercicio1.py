import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox

class VentanaPerfil(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Aplicación PyQt6")
        self.setMinimumSize(400, 300)

        layout_principal = QVBoxLayout()

        self.cmb_perfil = QComboBox()
        self.cmb_perfil.setPlaceholderText("Selecciona un perfil...")
        self.cmb_perfil.addItems(["Profesor", "Alumno"])
        self.cmb_perfil.setCurrentIndex(-1)
        layout_principal.addWidget(self.cmb_perfil)

        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPerfil()
    sys.exit(app.exec())