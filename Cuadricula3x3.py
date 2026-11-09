import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QCheckBox, \
    QStackedLayout, QHBoxLayout, QPushButton, QMessageBox, QGridLayout

from PyQt6.QtGui import QColor, QPalette

class TableroGrid(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tablero Buscaminas 3x3")
        grid_layout = QGridLayout()

        self.botones = []
        for fila in range(3):
            for col in range(3):
                boton = QPushButton()
                grid_layout.addWidget(boton, fila, col)
                boton.setFixedSize(60, 60)
                boton.clicked.connect(self.revelar_casilla)
                self.botones.append(boton)


        layout_principal = QVBoxLayout()
        layout_principal.addLayout(grid_layout)
        self.btn_reiniciar = QPushButton("Reiniciar Tablero")
        self.btn_reiniciar.clicked.connect(self.reiniciar_tablero)
        layout_principal.addWidget(self.btn_reiniciar)





        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)
        self.show()


    def revelar_casilla(self):
        boton_pulsado = self.sender()
        boton_pulsado.setText("X")
        boton_pulsado.setEnabled(False)

    def reiniciar_tablero(self):
        for boton in self.botones:
            boton.setText("")
            boton.setEnabled(True)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TableroGrid()
    sys.exit(app.exec())