import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QCheckBox, QStackedLayout


class VentanaPerfil(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Aplicación PyQt6")
        self.setMinimumSize(400, 300)

        layout_principal = QVBoxLayout()

        self.cmb_perfil = QComboBox()
        self.cmb_perfil.setPlaceholderText("Selecciona un perfil...")
        self.cmb_perfil.addItems(["Profesor", "Alumno"])
        self.cmb_perfil.setCurrentIndex(-1)
        layout_principal.addWidget(self.cmb_perfil)

        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        self.panel_profesor = self.crear_panel_profesores()
        self.panel_alumno = self.crear_panel_alumnos()

        self.tarjetas = QStackedLayout()
        self.tarjetas.addWidget(self.panel_profesor)
        self.tarjetas.addWidget(self.panel_alumno)

        layout_principal.addLayout(self.tarjetas)

        self.cmb_perfil.currentIndexChanged.connect(self.tarjetas.setCurrentIndex)


        self.show()

    def crear_panel_profesores(self):
        panel = QWidget()
        layout = QVBoxLayout()
        lbl = QLabel("Seccion de profesores")
        le = QLineEdit()
        le.setPlaceholderText("Añade la asignatura")
        ce = QCheckBox("Es tutor")
        panel.setLayout(layout)
        layout.addWidget(lbl)
        layout.addWidget(le)
        layout.addWidget(ce)

        return panel

    def crear_panel_alumnos(self):

        panel = QWidget()
        layout = QVBoxLayout()
        lbl = QLabel("Seccion de alumnos")
        le = QLineEdit()
        le.setPlaceholderText("Añade la asignatura")
        panel.setLayout(layout)
        layout.addWidget(lbl)
        layout.addWidget(le)

        return panel






if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPerfil()
    sys.exit(app.exec())