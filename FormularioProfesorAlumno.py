import sys
# Importaciones del módulo Widgets de PyQt6 para construir la interfaz dinámica
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QCheckBox, QStackedLayout
)


class VentanaPerfil(QMainWindow):
    """
    Clase principal que muestra un formulario dinámico según el perfil seleccionado.
    Utiliza un QComboBox para alternar los paneles dinámicos mediante un QStackedLayout.
    """

    def __init__(self):
        super().__init__()

        # Configuración de título y dimensiones mínimas de la ventana principal
        self.setWindowTitle("Mi Aplicación PyQt6")
        self.setMinimumSize(400, 300)

        # Layout vertical principal para alojar el selector y las tarjetas dinámicas
        layout_principal = QVBoxLayout()

        # Creación y configuración del menú desplegable (QComboBox)
        self.cmb_perfil = QComboBox()
        self.cmb_perfil.setPlaceholderText("Selecciona un perfil...")
        self.cmb_perfil.addItems(["Profesor", "Alumno"])  # Profesor -> Índice 0, Alumno -> Índice 1
        self.cmb_perfil.setCurrentIndex(-1)  # Ninguna opción seleccionada por defecto
        layout_principal.addWidget(self.cmb_perfil)

        # Configuración del widget central contenedor para QMainWindow
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Creación de los paneles de formulario específicos mediante métodos auxiliares
        self.panel_profesor = self.crear_panel_profesores()
        self.panel_alumno = self.crear_panel_alumnos()

        # Layout apilado (QStackedLayout) para intercambiar entre los paneles
        self.tarjetas = QStackedLayout()
        self.tarjetas.addWidget(self.panel_profesor)  # Agregado en el índice 0
        self.tarjetas.addWidget(self.panel_alumno)  # Agregado en el índice 1

        # Anidación del layout apilado dentro del layout vertical principal
        layout_principal.addLayout(self.tarjetas)

        # Conexión directa: la señal emite el nuevo índice del QComboBox (0 o 1),
        # que coincide directamente con los índices de los paneles en el QStackedLayout
        self.cmb_perfil.currentIndexChanged.connect(self.tarjetas.setCurrentIndex)

        # Muestra la ventana en pantalla
        self.show()

    def crear_panel_profesores(self):
        """
        Método auxiliar que construye y devuelve el widget del panel específico para profesores.
        """
        panel = QWidget()
        layout = QVBoxLayout()

        lbl = QLabel("Seccion de profesores")
        le = QLineEdit()
        le.setPlaceholderText("Añade la asignatura")
        ce = QCheckBox("Es tutor")

        # Ensamblado del panel de profesores
        panel.setLayout(layout)
        layout.addWidget(lbl)
        layout.addWidget(le)
        layout.addWidget(ce)

        return panel

    def crear_panel_alumnos(self):
        """
        Método auxiliar que construye y devuelve el widget del panel específico para alumnos.
        """
        panel = QWidget()
        layout = QVBoxLayout()

        lbl = QLabel("Seccion de alumnos")
        le = QLineEdit()
        le.setPlaceholderText("Añade la asignatura")

        # Ensamblado del panel de alumnos
        panel.setLayout(layout)
        layout.addWidget(lbl)
        layout.addWidget(le)

        return panel


# Bloque de ejecución principal del script
if __name__ == '__main__':
    # Creación de la instancia de la aplicación PyQt
    app = QApplication(sys.argv)

    # Instanciación e inicialización de la ventana de perfiles
    ventana = VentanaPerfil()

    # Inicio del bucle de eventos principal
    sys.exit(app.exec())