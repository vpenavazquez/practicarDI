import sys
# Importaciones de widgets de PyQt6 requeridos para la ventana y los controles
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout,
    QPushButton, QMessageBox, QGridLayout
)


class AsistenteFormulario(QMainWindow):
    """
    Clase principal que implementa un asistente de configuración paso a paso (Wizard).
    Utiliza QStackedLayout para alternar entre las distintas fases y controla la navegación
    mediante lógica de activación/desactivación de botones de navegación.
    """

    def __init__(self):
        super().__init__()

        # Configuración del título y dimensiones mínimas de la ventana
        self.setWindowTitle("Asistente de configuracion(Wizard)")
        self.setMinimumSize(450, 300)

        # Layout apilado (QStackedLayout) para almacenar las distintas páginas o pasos del asistente
        self.stack_layout = QStackedLayout()

        # Creación de los componentes/vistas que representan cada paso del asistente
        paso1 = QLabel("Paso 1: Datos Personales")
        paso2 = QLabel("Paso 2: Preferencias de Usuario")
        paso3 = QLabel("Paso 3: Confirmación y Resumen")

        # Inserción de los pasos en el layout apilado (asigna automáticamente índices 0, 1 y 2)
        self.stack_layout.addWidget(paso1)  # Índice 0
        self.stack_layout.addWidget(paso2)  # Índice 1
        self.stack_layout.addWidget(paso3)  # Índice 2

        # Layout horizontal para ubicar los botones de navegación en la parte inferior
        layout_horizontal = QHBoxLayout()

        # Creación de los botones de control de la secuencia
        self.btn_anterior = QPushButton("Anterior")
        self.btn_siguiente = QPushButton("Siguiente")

        # Deshabilita el botón "Anterior" al inicio, ya que el juego/asistente arranca en la primera vista (índice 0)
        self.btn_anterior.setEnabled(False)

        # Vinculación de los eventos de clic de los botones con los métodos de avance y retroceso
        self.btn_siguiente.clicked.connect(self.avanzar_pasos)
        self.btn_anterior.clicked.connect(self.retroceder)

        # Inserción de los botones en el sub-layout horizontal
        layout_horizontal.addWidget(self.btn_anterior)
        layout_horizontal.addWidget(self.btn_siguiente)

        # Layout vertical principal para apilar las pantallas y la barra inferior de botones
        layout_principal = QVBoxLayout()
        layout_principal.addLayout(self.stack_layout)
        layout_principal.addLayout(layout_horizontal)

        # Widget contenedor central genérico para estructurar la ventana con QMainWindow
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Muestra la ventana en pantalla
        self.show()

    def actualizar_botones(self):
        """
        Método auxiliar que evalúa la posición actual en la pila de vistas.
        Habilita o deshabilita los botones de navegación según se esté en el primer,
        intermedio o último paso del asistente.
        """
        idx = self.stack_layout.currentIndex()
        total = self.stack_layout.count()

        # 'Anterior' solo se habilita si no estamos en el primer paso (índice > 0)
        self.btn_anterior.setEnabled(idx > 0)

        # 'Siguiente' solo se habilita si no hemos llegado al último paso (índice < total - 1)
        self.btn_siguiente.setEnabled(idx < total - 1)

    def avanzar_pasos(self):
        """
        Avanza al siguiente paso del asistente si existe uno disponible
        y refresca el estado de los botones.
        """
        idx = self.stack_layout.currentIndex()
        total = self.stack_layout.count()
        if idx < total - 1:
            self.stack_layout.setCurrentIndex(idx + 1)
            self.actualizar_botones()

    def retroceder(self):
        """
        Retrocede al paso previo del asistente si no se encuentra en el origen
        y refresca el estado de los botones.
        """
        idx = self.stack_layout.currentIndex()
        if idx > 0:
            self.stack_layout.setCurrentIndex(idx - 1)
            self.actualizar_botones()


# Bloque de ejecución principal
if __name__ == "__main__":
    # Instancia de la aplicación ejecutable de PyQt
    app = QApplication(sys.argv)

    # Creación e inicialización de la ventana del asistente
    window = AsistenteFormulario()

    # Arranca el bucle de eventos principal (event loop)
    sys.exit(app.exec())