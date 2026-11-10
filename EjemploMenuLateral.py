import sys
# Importaciones necesarias de PyQt6 para estructurar la ventana y sus componentes
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout,
    QPushButton, QMessageBox, QGridLayout
)
# Importaciones de paletas gráficas (no se utilizan en este código específico)
from PyQt6.QtGui import QColor, QPalette


class PanelAdministracion(QMainWindow):
    """
    Clase que representa un panel de administración con navegación por pestañas/vistas.
    Utiliza QStackedLayout para alternar entre diferentes pantallas al pulsar los botones del menú.
    """

    def __init__(self):
        super().__init__()

        # Configuración del tamaño mínimo de la ventana
        self.setMinimumSize(600, 400)

        # Layout horizontal principal: dividirá la pantalla en menú lateral (izquierda) y contenido (derecha)
        layout_principal = QHBoxLayout()

        # Layout vertical para organizar los botones del menú de navegación
        layout_menu = QVBoxLayout()

        # QStackedLayout para apilar las vistas (solo una vista se muestra a la vez)
        self.stack_layout = QStackedLayout()

        # Creación de los botones de navegación del menú lateral
        self.btn_inicio = QPushButton("Inicio")
        self.btn_perfil = QPushButton("Perfil")
        self.btn_ajustes = QPushButton("Ajustes")

        # Creación de los widgets que representan las distintas vistas o páginas del panel
        vista_inicio = QLabel("Bienvenido a la pantalla de incio")
        vista_perfil = QLabel("Perfil del usuario")
        vista_ajustes = QLabel("Configuracion del sistema")

        # Añadir los botones al layout vertical del menú
        layout_menu.addWidget(self.btn_inicio)
        layout_menu.addWidget(self.btn_perfil)
        layout_menu.addWidget(self.btn_ajustes)

        # Añadir los widgets de las vistas al QStackedLayout (asigna índices automáticos 0, 1, 2)
        self.stack_layout.addWidget(vista_inicio)  # Índice 0
        self.stack_layout.addWidget(vista_perfil)  # Índice 1
        self.stack_layout.addWidget(vista_ajustes)  # Índice 2

        # Conectar los eventos de clic de los botones con sus