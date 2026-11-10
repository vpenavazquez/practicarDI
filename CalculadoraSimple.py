import sys
# Importaciones de widgets de PyQt6 para la construcción de la interfaz gráfica
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout, QPushButton
)
# Importaciones de interfaz gráfica (no utilizadas en esta implementación específica)
from PyQt6.QtGui import QColor, QPalette


class Calculadora(QMainWindow):
    """
    Clase principal que implementa una mini calculadora de operaciones básicas.
    Hereda de QMainWindow para estructurar la ventana principal de la aplicación.
    """

    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal (título y tamaño mínimo)
        self.setWindowTitle("Mini Calculadora")
        self.setMinimumSize(300, 200)

        # Layout principal vertical para apilar los campos de texto, el resultado y la botonera
        layout_principal = QVBoxLayout()

        # Campos de entrada de texto de una sola línea (QLineEdit) para los operandos
        self.num1 = QLineEdit()
        self.num2 = QLineEdit()

        # Texto indicativo de sugerencia (placeholder) cuando los campos están vacíos
        self.num1.setPlaceholderText("Ingrese un numero")
        self.num2.setPlaceholderText("Ingrese otro numero")

        # Etiqueta (QLabel) para mostrar el resultado o posibles errores de validación
        self.lbl_resultado = QLabel("Resultado")

        # Añadir los inputs y la etiqueta al layout vertical principal
        layout_principal.addWidget(self.num1)
        layout_principal.addWidget(self.num2)
        layout_principal.addWidget(self.lbl_resultado)

        # Botones para realizar las operaciones y limpiar los datos
        self.btn_sumar = QPushButton("+")
        self.btn_restar = QPushButton("-")
        self.btn_multiplicar = QPushButton("*")
        self.btn_limpiar = QPushButton("Limpiar")

        # Layout horizontal para alinear los botones de acción uno al lado del otro
        layout_botones = QHBoxLayout()
        layout_principal.addLayout(layout_botones)  # Anidar el layout horizontal dentro del vertical
        layout_botones.addWidget(self.btn_sumar)
        layout_botones.addWidget(self.btn_restar)
        layout_botones.addWidget(self.btn_multiplicar)
        layout_botones.addWidget(self.btn_limpiar)

        # Widget contenedor genérico requerido por QMainWindow para sostener la disposición de layouts
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Vinculación de los eventos de clic de los botones (Signals) con sus respectivas funciones (Slots)
        self.btn_sumar.clicked.connect(self.sumar)
        self.btn_restar.clicked.connect(self.restar)
        self.btn_multiplicar.clicked.connect(self.multiplicar)
        self.btn_limpiar.clicked.connect(self.limpiar)

        # Mostrar la ventana en pantalla
        self.show()

    def sumar(self):
        """
        Obtiene el texto de los dos campos, los convierte a flotante y calcula la suma.
        Captura errores de conversión en caso de entradas no numéricas.
        """
        texto1 = self.num1.text()
        texto2 = self.num2.text()

        try:
            val1 = float(texto1)
            val2 = float(texto2)
            self.lbl_resultado.setText(f"Resultado: {val1 + val2}")
        except ValueError:
            self.lbl_resultado.setText("Error: Introduce números válidos")

    def restar(self):
        """
        Obtiene el texto de los dos campos, los convierte a flotante y calcula la resta.
        """
        texto1 = self.num1.text()
        texto2 = self.num2.text()

        try:
            val1 = float(texto1)
            val2 = float(texto2)
            self.lbl_resultado.setText(f"Resultado: {val1 - val2}")
        except ValueError:
            self.lbl_resultado.setText("Error: Introduce números válidos")

    def multiplicar(self):
        """
        Obtiene el texto de los dos campos, los convierte a flotante y calcula la multiplicación.
        """
        texto1 = self.num1.text()
        texto2 = self.num2.text()

        try:
            val1 = float(texto1)
            val2 = float(texto2)
            self.lbl_resultado.setText(f"Resultado: {val1 * val2}")
        except ValueError:
            self.lbl_resultado.setText("Error: Introduce números válidos")

    def limpiar(self):
        """
        Vacía los campos de entrada de texto y restablece la etiqueta de resultado.
        """
        self.num1.clear()
        self.num2.clear()
        self.lbl_resultado.setText("Resultado: ")


# Bloque de ejecución principal
if __name__ == '__main__':
    # Creación de la instancia de la aplicación PyQt
    app = QApplication(sys.argv)

    # Instanciación e inicialización de la calculadora
    window = Calculadora()

    # Inicio del bucle principal de eventos de la interfaz gráfica
    sys.exit(app.exec())