import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QCheckBox, QPushButton
)

class EjemploFormulario(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo 1: Formulario de Registro")
        self.resize(350, 200)

        # 1. Contenedor central obligatorio
        contenedor = QWidget()
        self.setCentralWidget(contenedor)

        # 2. Layout principal vertical
        layout_principal = QVBoxLayout()
        contenedor.setLayout(layout_principal)

        # 3. Formulario en rejilla (Grid)
        grid = QGridLayout()
        grid.addWidget(QLabel("Usuario:"), 0, 0)
        grid.addWidget(QLineEdit(), 0, 1)
        grid.addWidget(QLabel("Email:"), 1, 0)
        grid.addWidget(QLineEdit(), 1, 1)

        # 4. Checkbox
        chk_terminos = QCheckBox("Acepto los términos y condiciones")
        chk_terminos.setChecked(True)  # Aparece marcada por defecto

        # 5. Fila horizontal para botones
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(QPushButton("Cancelar"))
        layout_botones.addWidget(QPushButton("Guardar"))

        # 6. Ensamblar todo en el layout principal
        layout_principal.addLayout(grid)
        layout_principal.addWidget(chk_terminos)
        layout_principal.addLayout(layout_botones)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = EjemploFormulario()
    v.show()
    sys.exit(app.exec())