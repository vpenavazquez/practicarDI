import sys
# Importaciones necesarias de PyQt6 para la gestión de la aplicación, ventana principal y layouts
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout,
    QPushButton, QMessageBox, QGridLayout
)


class GaleriaTarjetas(QMainWindow):
    """
    Clase principal que implementa una galería dinámica de botones en cuadrícula (3x3).
    Muestra los detalles de la tarjeta seleccionada en una etiqueta lateral.
    """

    def __init__(self):
        super().__init__()

        # Configuración del título y dimensiones mínimas de la ventana
        self.setWindowTitle("Galeria de Tarjetas y Detalles")
        self.setMinimumSize(600, 400)

        # Layout horizontal principal: situará la cuadrícula a la izquierda y el detalle a la derecha
        layout_principal = QHBoxLayout()

        # Layout en cuadrícula (QGridLayout) para organizar los botones del tablero 3x3
        layout_cuadricula = QGridLayout()

        # Etiqueta informativa (QLabel) para mostrar los detalles del botón pulsado
        self.lbl_detalle = QLabel("Selecciona una tarjeta para ver los detalles")

        # Bucle anidado para generar la matriz de 3 filas x 3 columnas
        for fila in range(3):
            for col in range(3):
                # 1. Cálculo del identificador único numérico del 1 al 9
                numero_tarjeta = fila * 3 + col + 1

                # 2. Instanciación del botón individual para la posición actual
                btn = QPushButton(f"Tarjeta {numero_tarjeta}")

                # 3. Ubicación del botón en el layout de cuadrícula en la posición (fila, columna)
                layout_cuadricula.addWidget(btn, fila, col)

                # Vinculación del evento de clic a la función manejadora de detalles
                btn.clicked.connect(self.mostrar_detalle)

        # Ensamblado del layout principal: se añade la cuadrícula y la etiqueta de detalles
        layout_principal.addLayout(layout_cuadricula)
        layout_principal.addWidget(self.lbl_detalle)

        # Configuración del widget contenedor central indispensable en QMainWindow
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Muestra la ventana en pantalla
        self.show()

    def mostrar_detalle(self):
        """
        Slot/Manejador ejecutado al pulsar cualquiera de las tarjetas de la cuadrícula.
        Identifica qué botón emitió la señal mediante 'self.sender()' y actualiza la etiqueta.
        """
        # Identifica el objeto QPushButton específico que disparó el evento clic
        boton = self.sender()
        nombre_tarjeta = boton.text()

        # Actualiza el texto de la etiqueta lateral con la tarjeta seleccionada
        self.lbl_detalle.setText(f"Has seleccionado la **{nombre_tarjeta}**")


# Bloque de punto de entrada y ejecución de la aplicación
if __name__ == "__main__":
    # Instancia de la aplicación ejecutable de PyQt
    app = QApplication(sys.argv)

    # Creación e inicialización de la ventana de la galería
    window = GaleriaTarjetas()

    # Inicio del bucle principal de eventos del sistema (Event Loop)
    sys.exit(app.exec())