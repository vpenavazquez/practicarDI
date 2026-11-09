import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout

from PyQt6.QtGui import QColor, QPalette

class CaixaCor(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        paleta = self.palette()
        paleta.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(paleta)

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Aplicación PyQt6")
        self.setMinimumSize(400, 300)

        layout_principal = QHBoxLayout()

        layout_col1 = QVBoxLayout()

        layout_col1.addWidget(CaixaCor("red"))
        layout_col1.addWidget(CaixaCor("yellow"))
        layout_col1.addWidget(CaixaCor("purple"))

        caixa_verde = CaixaCor("green")

        layout_principal.addLayout(layout_col1)

        layout_principal.addWidget(caixa_verde)

        layout_col3 = QVBoxLayout()
        layout_col3.addWidget(CaixaCor("red"))
        layout_col3.addWidget(CaixaCor("purple"))

        layout_principal.addLayout(layout_col3)

        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    sys.exit(app.exec())









