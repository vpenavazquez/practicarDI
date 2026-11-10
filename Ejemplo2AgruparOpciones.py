import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QGroupBox, QRadioButton, QComboBox, QLabel
)

class EjemploOpciones(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ejemplo 2: Desplegable y Grupos de Radio")
        self.resize(350, 250)

        contenedor = QWidget()
        self.setCentralWidget(contenedor)

        layout_principal = QVBoxLayout()
        contenedor.setLayout(layout_principal)

        # 1. Desplegable
        layout_principal.addWidget(QLabel("Selecciona Ciclo:"))
        combo = QComboBox()
        combo.addItems(["DAM", "DAW", "ASIR"])
        layout_principal.addWidget(combo)

        # 2. Grupo 1: Curso (Los radio buttons dentro de este marco son exclusivos entre sí)
        grupo_curso = QGroupBox("Curso")
        layout_curso = QHBoxLayout()
        rb_1 = QRadioButton("1º Curso")
        rb_2 = QRadioButton("2º Curso")
        rb_1.setChecked(True)  # Marcar el primero por defecto
        layout_curso.addWidget(rb_1)
        layout_curso.addWidget(rb_2)
        grupo_curso.setLayout(layout_curso)

        # 3. Grupo 2: Turno (Funciona de forma independiente al grupo de arriba)
        grupo_turno = QGroupBox("Turno")
        layout_turno = QHBoxLayout()
        rb_manana = QRadioButton("Mañana")
        rb_tarde = QRadioButton("Tarde")
        rb_manana.setChecked(True)
        layout_turno.addWidget(rb_manana)
        layout_turno.addWidget(rb_tarde)
        grupo_turno.setLayout(layout_turno)

        # 4. Añadir marcos al layout principal
        layout_principal.addWidget(grupo_curso)
        layout_principal.addWidget(grupo_turno)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = EjemploOpciones()
    v.show()
    sys.exit(app.exec())