import sys
# Importaciones necesarias de PyQt6 para controles de interfaz gráfica y la ventana principal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox,
    QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout, QPushButton,
    QMessageBox, QGridLayout, QTextEdit
)
# Importaciones de GUI gráficas (QIcon, QColor, QPalette)
from PyQt6.QtGui import QColor, QPalette, QIcon


class VisorTexto(QMainWindow):
    """
    Clase principal que implementa un visor y editor de texto multilínea.
    Incluye una barra de herramientas básica (mayúsculas, borrado, bloqueo)
    y una barra inferior con un contador en tiempo real de caracteres.
    """

    def __init__(self):
        super().__init__()

        # Configuración del título de la ventana y dimensiones mínimas
        self.setWindowTitle("Visor de texto y herramientas")
        self.setMinimumSize(500, 400)

        # Layout vertical principal para apilar la botonera superior, el editor y el contador inferior
        layout_principal = QVBoxLayout()

        # Creación de los botones de interacción y herramientas
        self.btn_mayus = QPushButton("Mayusculas")
        self.btn_limpiar = QPushButton("Limpiar")
        self.btn_bloquear = QPushButton("Bloquear/Desbloquear")

        # Conexión de las señales de clic ('clicked') de los botones a sus funciones manejadoras (slots)
        self.btn_mayus.clicked.connect(self.convertir_mayusculas)
        self.btn_limpiar.clicked.connect(self.limpiar_texto)
        self.btn_bloquear.clicked.connect(self.alternar_bloqueo)

        # Layout horizontal para alinear la botonera superior en fila
        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(self.btn_mayus)
        layout_horizontal.addWidget(self.btn_limpiar)
        layout_horizontal.addWidget(self.btn_bloquear)

        # Creación del control para la edición de texto multilínea (QTextEdit)
        self.txt_editor = QTextEdit()

        # Etiqueta informativa inferior (QLabel) para mostrar el número de caracteres
        self.lbl_estado = QLabel("Caracteres: 0")

        # Conexión de la señal 'textChanged': se activa automáticamente cada vez que cambia el contenido del editor
        self.txt_editor.textChanged.connect(self.actualizar_contador)

        # Añadir sub-layout de botones, el editor multilínea y la etiqueta al layout principal
        layout_principal.addLayout(layout_horizontal)
        layout_principal.addWidget(self.txt_editor)
        layout_principal.addWidget(self.lbl_estado)

        # Widget contenedor central genérico requerido por QMainWindow
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Muestra la ventana en pantalla
        self.show()

    def convertir_mayusculas(self):
        """
        Extrae el contenido en texto plano del QTextEdit utilizando '.toPlainText()',
        lo convierte totalmente a mayúsculas y lo vuelve a volcar en el editor.
        """
        texto = self.txt_editor.toPlainText().upper()
        self.txt_editor.setPlainText(texto)

    def limpiar_texto(self):
        """Borra todo el contenido escrito en el QTextEdit."""
        self.txt_editor.clear()

    def alternar_bloqueo(self):
        """
        Alterna el estado de edición del campo de texto.
        Si está en modo lectura (read-only), lo habilita; de lo contrario, lo bloquea.
        """
        if self.txt_editor.isReadOnly():
            self.txt_editor.setReadOnly(False)
        else:
            self.txt_editor.setReadOnly(True)

    def actualizar_contador(self):
        """
        Slot ejecutado automáticamente tras cada modificación de texto en el QTextEdit.
        Calcula la longitud del texto actual e imprime la cuenta en la etiqueta de estado.
        """
        texto = self.txt_editor.toPlainText()
        contador = len(texto)
        self.lbl_estado.setText(f"Caracteres totales: {contador}")


# Bloque de ejecución principal del script
if __name__ == '__main__':
    # Inicialización de la aplicación global de PyQt
    app = QApplication(sys.argv)

    # Creación e instanciación de la ventana principal del visor
    texto = VisorTexto()

    # Arranca el bucle de eventos principal (Event Loop) y gestiona un cierre limpio
    sys.exit(app.exec())