import sys
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QGridLayout, QLabel, QPushButton, QSizePolicy
)


class BotonColor(QPushButton):
    # Señal personalizada para avisar a la ventana principal cada vez que cambia el color
    color_cambiado = pyqtSignal()

    def __init__(self, texto=""):
        super().__init__(texto)
        self.color = None  # Al inicio no tiene color ("rojo" o "verde")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.color = "rojo"
            self.setStyleSheet("background-color: red; color: white;")
            self.color_cambiado.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            self.color = "verde"
            self.setStyleSheet("background-color: green; color: white;")
            self.color_cambiado.emit()

        super().mousePressEvent(event)


class Enraya(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3 en Raya")
        self.setFixedSize(600, 650)  # Un poco más alto para dar espacio al marcador

        layout_principal = QVBoxLayout()

        # 1. MARCADOR SUPERIOR
        self.lbl_marcador = QLabel("¡Haz 3 en raya!")
        self.lbl_marcador.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_marcador.setStyleSheet("font-size: 22px; font-weight: bold; padding: 10px; color: black;")
        layout_principal.addWidget(self.lbl_marcador)

        # Matriz 3x3 para almacenar las referencias de los botones
        self.matriz_botones = []

        # 2. JUEGO (REJILLA DE BOTONES)
        grid_bottom = QGridLayout()

        for fila in range(3):
            fila_botones = []
            for col in range(3):
                btn = BotonColor(" ")
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                # Al presionar cualquier botón se evalúa si hay un ganador
                btn.color_cambiado.connect(self.comprobar_ganador)
                grid_bottom.addWidget(btn, fila, col)
                fila_botones.append(btn)
            self.matriz_botones.append(fila_botones)

        layout_principal.addLayout(grid_bottom)

        # 3. CONTENEDOR CENTRAL
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

    def comprobar_ganador(self):
        m = self.matriz_botones

        # Lista con todas las combinaciones ganadoras (Filas, Columnas y Diagonales)
        lineas = [
            # Filas
            [m[0][0], m[0][1], m[0][2]],
            [m[1][0], m[1][1], m[1][2]],
            [m[2][0], m[2][1], m[2][2]],
            # Columnas
            [m[0][0], m[1][0], m[2][0]],
            [m[0][1], m[1][1], m[2][1]],
            [m[0][2], m[1][2], m[2][2]],
            # Diagonales
            [m[0][0], m[1][1], m[2][2]],
            [m[0][2], m[1][1], m[2][0]],
        ]

        for b1, b2, b3 in lineas:
            # Comprueba que el primer botón tenga color asignado y que los 3 sean del mismo color
            if b1.color is not None and b1.color == b2.color == b3.color:
                if b1.color == "rojo":
                    self.lbl_marcador.setText("¡GANADOR: ROJO!")
                    self.lbl_marcador.setStyleSheet("font-size: 22px; font-weight: bold; color: red; padding: 10px;")
                elif b1.color == "verde":
                    self.lbl_marcador.setText("¡GANADOR: VERDE!")
                    self.lbl_marcador.setStyleSheet("font-size: 22px; font-weight: bold; color: green; padding: 10px;")
                return  # Detiene la búsqueda al encontrar al primer ganador


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Enraya()
    window.show()
    sys.exit(app.exec())