import sys
# Importaciones necesarias de PyQt6 para widgets y diseños de la interfaz gráfica
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox,
    QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout, QPushButton,
    QMessageBox, QGridLayout
)
# Importaciones de interfaz gráfica (no utilizadas en esta implementación específica)
from PyQt6.QtGui import QColor, QPalette


class TableroGrid(QMainWindow):
    """
    Clase que representa un tablero de juego básico de 3x3 utilizando QGridLayout.
    Hereda de QMainWindow para definir la ventana principal.
    """

    def __init__(self):
        super().__init__()

        # Configuración del título de la ventana
        self.setWindowTitle("Tablero Buscaminas 3x3")

        # Creación del layout en cuadrícula para distribuir los botones en filas y columnas
        grid_layout = QGridLayout()

        # Lista para mantener la referencia de los 9 botones creados
        self.botones = []

        # Bucle anidado para generar una cuadrícula de 3x3 (3 filas x 3 columnas)
        for fila in range(3):
            for col in range(3):
                boton = QPushButton()
                # Añade el botón al grid layout en la posición (fila, columna) correspondiente
                grid_layout.addWidget(boton, fila, col)
                # Define el tamaño fijo del botón en píxeles (ancho, alto)
                boton.setFixedSize(60, 60)
                # Conecta el evento de clic de cada casilla con la función reveladora
                boton.clicked.connect(self.revelar_casilla)
                # Guarda el botón en la lista para poder manipularlo más tarde (ej. al reiniciar)
                self.botones.append(boton)

        # Layout vertical principal para apilar la cuadrícula y el botón de reinicio
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(grid_layout)

        # Creación y configuración del botón de reinicio
        self.btn_reiniciar = QPushButton("Reiniciar Tablero")
        self.btn_reiniciar.clicked.connect(self.reiniciar_tablero)
        layout_principal.addWidget(self.btn_reiniciar)

        # Contenedor central requerido por QMainWindow para albergar la estructura de layouts
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Muestra la ventana en pantalla
        self.show()

    def revelar_casilla(self):
        """
        Manejador que se ejecuta al hacer clic en cualquiera de las casillas de la cuadrícula.
        Identifica qué botón disparó la señal usando 'self.sender()'.
        """
        # Identifica el objeto QPushButton específico que ha emitido la señal de clic
        boton_pulsado = self.sender()

        # Marca la casilla con una "X" y la inhabilita para impedir nuevos clics
        boton_pulsado.setText("X")
        boton_pulsado.setEnabled(False)

    def reiniciar_tablero(self):
        """
        Restablece el estado inicial de todas las casillas del tablero.
        """
        # Recorre la lista guardada de botones limadolos y volviéndolos a habilitar
        for boton in self.botones:
            boton.setText("")
            boton.setEnabled(True)


# Bloque de ejecución principal
if __name__ == '__main__':
    # Instancia la aplicación ejecutable de PyQt
    app = QApplication(sys.argv)

    # Crea e inicializa la ventana del tablero
    window = TableroGrid()

    # Inicia el bucle de eventos de la aplicación
    sys.exit(app.exec())