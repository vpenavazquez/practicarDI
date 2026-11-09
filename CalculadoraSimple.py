import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout, QPushButton

from PyQt6.QtGui import QColor, QPalette


class Calculadora(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Calculadora")
        self.setMinimumSize(300, 200)

        layout_principal = QVBoxLayout()

        self.num1 = QLineEdit()
        self.num2 = QLineEdit()

        self.num1.setPlaceholderText("Ingrese un numero")
        self.num2.setPlaceholderText("Ingrese otro numero")

        self.lbl_resultado = QLabel("Resultado")

        layout_principal.addWidget(self.num1)
        layout_principal.addWidget(self.num2)
        layout_principal.addWidget(self.lbl_resultado)

        self.btn_sumar = QPushButton("+")
        self.btn_restar = QPushButton("-")
        self.btn_multiplicar = QPushButton("*")
        self.btn_limpiar = QPushButton("Limpiar")

        layout_botones = QHBoxLayout()
        layout_principal.addLayout(layout_botones)
        layout_botones.addWidget(self.btn_sumar)
        layout_botones.addWidget(self.btn_restar)
        layout_botones.addWidget(self.btn_multiplicar)
        layout_botones.addWidget(self.btn_limpiar)

        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        self.btn_sumar.clicked.connect(self.sumar)
        self.btn_restar.clicked.connect(self.restar)
        self.btn_multiplicar.clicked.connect(self.multiplicar)
        self.btn_limpiar.clicked.connect(self.limpiar)

        self.show()

    def sumar(self):
        texto1 = self.num1.text()
        texto2 = self.num2.text()


        try:
            val1 = float(texto1)
            val2 = float(texto2)
            self.lbl_resultado.setText(f"Resultado: {val1 + val2}")
        except ValueError:
            self.lbl_resultado.setText(f"Error: Introduce números válidos")

    def restar(self):
        texto1 = self.num1.text()
        texto2 = self.num2.text()


        try:
            val1 = float(texto1)
            val2 = float(texto2)
            self.lbl_resultado.setText(f"Resultado: {val1 - val2}")
        except ValueError:
            self.lbl_resultado.setText(f"Error: Introduce números válidos")


    def multiplicar(self):
        texto1 = self.num1.text()
        texto2 = self.num2.text()


        try:
            val1 = float(texto1)
            val2 = float(texto2)
            self.lbl_resultado.setText(f"Resultado: {val1 * val2}")
        except ValueError:
            self.lbl_resultado.setText(f"Error: Introduce números válidos")


    def limpiar(self):
        self.num1.clear()
        self.num2.clear()

        self.lbl_resultado.setText(f"Resultado: ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculadora()
    sys.exit(app.exec())

