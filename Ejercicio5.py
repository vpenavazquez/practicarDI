import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QLineEdit, QCheckBox, \
    QStackedLayout, QHBoxLayout, QPushButton, QMessageBox, QGridLayout

from PyQt6.QtGui import QColor, QPalette

class TableroGrid(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tablero Buscaminas 3x3")
        grid_layout = QGridLayout()

        for fila in range(3):
            for col in range(3):
                boton = QPushButton()
                grid_layout.addWidget(boton, fila, col)
                boton.setFixedSize(60, 60)
                boton.clicked.connect(self.revelar_casilla)


        contenedor = QWidget()
        contenedor.setLayout(grid_layout)
        self.setCentralWidget(contenedor)
        self.show()


    def revelar_casilla(self):
        boton_pulsado = self.sender()
        boton_pulsado.setText("X")
        boton_pulsado.setEnabled(False)






if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TableroGrid()
    sys.exit(app.exec())