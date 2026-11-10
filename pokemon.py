import sys
from PyQt6.QtCore import QTime
from PyQt6.QtWidgets import *
from  PyQt6.QtGui import QColor, QPalette

class FiestraPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Registro Pokemon")

        self.setMinimumSize(400, 400)
        self.setMaximumSize(400, 400)

        layout_principal = QGridLayout()

        comun = QGridLayout()

        self.cnombre = QLineEdit()
        self.ctipo1 = QRadioButton()
        self.ctipo2 = QRadioButton()

        self.generacion = QComboBox()
        self.generacion.addItems(["1", "2", "3", "4"])

        self.descripcion = QTextEdit()
        self.etapas_evolutivas = QComboBox()
        self.etapas_evolutivas.addItems(["Primera", "Segunda", "Tercera"])

        comun.addWidget(QLabel("Nombre:"), 0, 0)
        comun.addWidget(self.cnombre, 0, 1)
        comun.addWidget(QLabel("1 Tipo:"), 1, 0)
        comun.addWidget(self.ctipo1, 1, 1)
        comun.addWidget(QLabel("2 Tipos:"), 2, 0)
        comun.addWidget(self.ctipo2, 2, 1)
        comun.addWidget(QLabel("Generación:"), 3, 0)
        comun.addWidget(self.generacion, 3, 1)
        comun.addWidget(QLabel("Descripción:"), 4, 0)
        comun.addWidget(self.descripcion, 4, 1)
        comun.addWidget(QLabel("Etapas Evolutivas:"), 5, 0)
        comun.addWidget(self.etapas_evolutivas, 5, 1)

        # Página del formulario
        widget_comun = QWidget()
        widget_comun.setLayout(comun)

        # Página donde se mostrarán los datos
        widget_resumen = QWidget()
        layout_resumen = QVBoxLayout()

        self.resumen_nombre = QLabel()
        self.resumen_tipo = QLabel()
        self.resumen_generacion = QLabel()
        self.resumen_descripcion = QLabel()
        self.resumen_etapas = QLabel()

        layout_resumen.addWidget(QLabel("<b>Datos del Pokémon</b>"))
        layout_resumen.addWidget(self.resumen_nombre)
        layout_resumen.addWidget(self.resumen_tipo)
        layout_resumen.addWidget(self.resumen_generacion)
        layout_resumen.addWidget(self.resumen_descripcion)
        layout_resumen.addWidget(self.resumen_etapas)

        widget_resumen.setLayout(layout_resumen)

        # QStackedLayout con las dos páginas
        self.stack = QStackedLayout()
        self.stack.addWidget(widget_comun)
        self.stack.addWidget(widget_resumen)

        layout_principal.addLayout(self.stack, 1, 0, 1, 2)

        self.enviar = QPushButton("Enviar")
        self.enviar.clicked.connect(self.mostrar_resumen)
        layout_principal.addWidget(self.enviar, 2, 0)

        self.volver = QPushButton("Volver")
        self.volver.clicked.connect(self.mostrar_formulario)
        self.volver.setVisible(False)
        layout_principal.addWidget(self.volver, 2, 1)

        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)
    def mostrar_resumen(self):
        tipo = "No seleccionado"

        if self.ctipo1.isChecked():
            tipo = "1 tipo"
        elif self.ctipo2.isChecked():
            tipo = "2 tipos"

        descripcion = self.descripcion.toPlainText()

        self.resumen_nombre.setText(
            f"<b>Nombre:</b> {self.cnombre.text()}"
        )
        self.resumen_tipo.setText(
            f"<b>Tipo:</b> {tipo}"
        )
        self.resumen_generacion.setText(
            f"<b>Generación:</b> {self.generacion.currentText()}"
        )
        self.resumen_descripcion.setText(
            f"<b>Descripción:</b> {descripcion}"
        )
        self.resumen_etapas.setText(
            f"<b>Etapas evolutivas:</b> "
            f"{self.etapas_evolutivas.currentText()}"
        )

        self.stack.setCurrentIndex(1)
        self.enviar.setVisible(False)
        self.volver.setVisible(True)

    def mostrar_formulario(self):
        self.stack.setCurrentIndex(0)
        self.enviar.setVisible(True)
        self.volver.setVisible(False)


if __name__ == '__main__':
    aplicacion = QApplication(sys.argv)
    fiestra = FiestraPrincipal()
    fiestra.show()
    aplicacion.exec()