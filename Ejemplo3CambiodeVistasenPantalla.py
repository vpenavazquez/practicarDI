import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QStackedLayout, QComboBox, QLabel, QLineEdit
)

class EjemploTarjetas(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo 3: Pantallas Superpuestas")
        self.resize(350, 200)

        contenedor = QWidget()
        self.setCentralWidget(contenedor)

        layout_principal = QVBoxLayout()
        contenedor.setLayout(layout_principal)

        # 1. Combo Selector en la parte superior
        self.combo_selector = QComboBox()
        self.combo_selector.addItems(["Vista Alumno", "Vista Profesor"])
        # Conectar el cambio de índice a la función
        self.combo_selector.currentIndexChanged.connect(self.cambiar_pantalla)
        layout_principal.addWidget(self.combo_selector)

        # 2. Layout apilado (Stack)
        self.tarxetas = QStackedLayout()

        # Panel 1: Alumno
        panel_alumno = QWidget()
        lay_alumno = QVBoxLayout()
        lay_alumno.addWidget(QLabel("Matrícula del Alumno:"))
        lay_alumno.addWidget(QLineEdit())
        panel_alumno.setLayout(lay_alumno)

        # Panel 2: Profesor
        panel_profesor = QWidget()
        lay_profesor = QVBoxLayout()
        lay_profesor.addWidget(QLabel("Despacho del Profesor:"))
        lay_profesor.addWidget(QLineEdit())
        panel_profesor.setLayout(lay_profesor)

        # Añadir los dos paneles al stack (Panel 1 -> Índice 0, Panel 2 -> Índice 1)
        self.tarxetas.addWidget(panel_alumno)
        self.tarxetas.addWidget(panel_profesor)

        # Añadir el stack al layout principal
        layout_principal.addLayout(self.tarxetas)

    def cambiar_pantalla(self, index):
        # Cambia la tarjeta visible según el índice seleccionado en el QComboBox
        self.tarxetas.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = EjemploTarjetas()
    v.show()
    sys.exit(app.exec())