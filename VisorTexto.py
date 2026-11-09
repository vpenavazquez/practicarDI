import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QCheckBox, \
    QStackedLayout, QHBoxLayout, QPushButton, QMessageBox, QGridLayout, QTextEdit

from PyQt6.QtGui import QColor, QPalette, QIcon


class VisorTexto(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visor de texto y herramientas")
        self.setMinimumSize(500, 400)

        layout_principal = QVBoxLayout()

        self.btn_mayus=QPushButton("Mayusculas")
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_bloquear = QPushButton("Bloquear/Desbloquear")

        self.btn_mayus.clicked.connect(self.convertir_mayusculas)
        self.btn_limpiar.clicked.connect(self.limpiar_texto)
        self.btn_bloquear.clicked.connect(self.alternar_bloqueo)


        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(self.btn_mayus)
        layout_horizontal.addWidget(self.btn_limpiar)
        layout_horizontal.addWidget(self.btn_bloquear)


        self.txt_editor = QTextEdit()
        self.lbl_estado = QLabel("Caracteres: 0")
        self.txt_editor.textChanged.connect(self.actualizar_contador)

        layout_principal.addLayout(layout_horizontal)
        layout_principal.addWidget(self.txt_editor)
        layout_principal.addWidget(self.lbl_estado)

        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)
        self.show()

    def convertir_mayusculas(self):
        texto = self.txt_editor.toPlainText().upper()
        self.txt_editor.setPlainText(texto)

    def limpiar_texto(self):
        self.txt_editor.clear()

    def alternar_bloqueo(self):
        if self.txt_editor.isReadOnly():
            self.txt_editor.setReadOnly(False)
        else:
            self.txt_editor.setReadOnly(True)

    def actualizar_contador(self):
        texto = self.txt_editor.toPlainText()

        contador = len(texto)
        self.lbl_estado.setText(f"Caracteres totales: {contador}")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    texto = VisorTexto()
    sys.exit(app.exec())

