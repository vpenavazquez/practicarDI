import sys
# Importaciones necesarias de PyQt6 para la construcción de interfaces y layouts
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout
)
# Importaciones de GUI para la gestión de colores y paletas gráficas
from PyQt6.QtGui import QColor, QPalette


class CaixaCor(QWidget):
    """
    Widget personalizado de apoyo que representa una caja de color sólido.
    Se utiliza para visualizar de forma gráfica la distribución del espacio en los layouts.
    """

    def __init__(self, color):
        super().__init__()
        # Permite que el fondo del QWidget se pinte automáticamente con el color asignado
        self.setAutoFillBackground(True)

        # Obtiene la paleta de colores actual del widget y asigna un nuevo color al fondo (Window)
        paleta = self.palette()
        paleta.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(paleta)


class VentanaPrincipal(QMainWindow):
    """
    Clase de la ventana principal que demuestra la combinación y anidación
    de layouts horizontales (QHBoxLayout) y verticales (QVBoxLayout).
    """

    def __init__(self):
        super().__init__()

        # Configuración del título y dimensiones mínimas de la ventana
        self.setWindowTitle("Mi Aplicación PyQt6")
        self.setMinimumSize(400, 300)

        # Layout principal horizontal: organiza el espacio en 3 columnas de izquierda a derecha
        layout_principal = QHBoxLayout()

        # --- Columna 1 (Izquierda) ---
        # Layout vertical para apilar tres cajas de colores de arriba a abajo
        layout_col1 = QVBoxLayout()
        layout_col1.addWidget(CaixaCor("red"))
        layout_col1.addWidget(CaixaCor("yellow"))
        layout_col1.addWidget(CaixaCor("purple"))

        # --- Columna 2 (Centro) ---
        # Un único widget central que