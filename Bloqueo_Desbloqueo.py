import sys
# Importaciones necesarias de PyQt6 para la construcción de la interfaz gráfica
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout,
    QPushButton, QMessageBox, QGridLayout
)
# Importaciones de color y paletas (Nota: no se utilizan en este script actual)
from PyQt6.QtGui import QColor, QPalette


class FormularioUsuario(QMainWindow):
    """
    Clase principal que representa la ventana de formulario de perfil de usuario.
    Hereda de QMainWindow para proporcionar la estructura básica de una ventana principal.
    """

    def __init__(self):
        super().__init__()

        # Configuración del título de la ventana y dimensiones mínimas (ancho, alto)
        self.setWindowTitle("Perfil de Usuario (Modo lectura)")
        self.setMinimumSize(400, 300)

        # Layout vertical principal para apilar los elementos de arriba a abajo
        layout_principal = QVBoxLayout()

        # Creación de etiquetas flotantes para identificar cada campo
        nombre = QLabel("Nombre")
        email = QLabel("Email")
        telefono = QLabel("Telefono")

        # Creación de los campos de texto de una sola línea (QLineEdit).
        # Se almacenan en 'self' para poder manipularlos desde otros métodos de la clase.
        self.lnombre = QLineEdit()
        self.lemail = QLineEdit()
        self.ltelefono = QLineEdit()

        # Establece el texto gris de sugerencia que aparece cuando el campo está vacío
        self.lnombre.setPlaceholderText("Nombre")
        self.lemail.setPlaceholderText("Email")
        self.ltelefono.setPlaceholderText("Telefono")

        # Inicialmente la ventana inicia en "Modo lectura", deshabilitando la edición
        self.lnombre.setEnabled(False)
        self.lemail.setEnabled(False)
        self.ltelefono.setEnabled(False)

        # Creación de los botones de interacción
        self.btn_editar = QPushButton("Editar")
        self.btn_guardar = QPushButton("Guardar")
        self.btn_guardar.setEnabled(False)  # El botón guardar inicia desactivado

        # Layout horizontal para ubicar los botones uno al lado del otro
        layout_horizontal = QHBoxLayout()
        layout_horizontal.addWidget(self.btn_editar)
        layout_horizontal.addWidget(self.btn_guardar)

        # Incorporación de etiquetas, campos de entrada y el sub-layout horizontal al layout principal
        layout_principal.addWidget(nombre)
        layout_principal.addWidget(self.lnombre)
        layout_principal.addWidget(email)
        layout_principal.addWidget(self.lemail)
        layout_principal.addWidget(telefono)
        layout_principal.addWidget(self.ltelefono)
        layout_principal.addLayout(layout_horizontal)

        # Vinculación del evento de clic (signal 'clicked') a sus funciones manejadoras (slots)
        self.btn_editar.clicked.connect(self.habilitar_edicion)
        self.btn_guardar.clicked.connect(self.guardar_cambios)

        # En QMainWindow se debe definir un widget contenedor genérico que aloje al layout principal
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

        # Muestra la ventana en pantalla
        self.show()

    def habilitar_edicion(self):
        """
        Cambia el estado del formulario a modo edición:
        habilita las entradas de texto y alterna el estado de los botones.
        """
        # Habilitar la edición de campos de texto
        self.lnombre.setEnabled(True)
        self.ltelefono.setEnabled(True)
        self.lemail.setEnabled(True)

        # Habilitar el botón Guardar y deshabilitar Editar para evitar clics redundantes
        self.btn_guardar.setEnabled(True)
        self.btn_editar.setEnabled(False)

    def guardar_cambios(self):
        """
        Valida que los campos no estén vacíos antes de guardar.
        Si la validación pasa, notifica al usuario y bloquea los campos nuevamente.
        """
        # Comprobar si alguno de los campos contiene solo espacios en blanco o está vacío
        if not self.lnombre.text().strip() or not self.ltelefono.text().strip() or not self.lemail.text().strip():
            # Muestra una alerta emergente de advertencia en caso de que falten datos
            QMessageBox.warning(self, "Campos vacíos", "Todos los campos deben estar rellenos.")
        else:
            # Muestra un mensaje emergente confirmando que la operación fue exitosa
            QMessageBox.information(self, "Éxito", "Datos guardados correctamente.")

            # Bloquear de nuevo los campos para volver al modo lectura
            self.lnombre.setEnabled(False)
            self.ltelefono.setEnabled(False)
            self.lemail.setEnabled(False)

            # Restablecer el estado inicial de los botones
            self.btn_guardar.setEnabled(False)
            self.btn_editar.setEnabled(True)


# Bloque de ejecución principal del script
if __name__ == '__main__':
    # Instancia de la aplicación PyQt (gestiona los eventos del sistema y la configuración de UI)
    app = QApplication(sys.argv)

    # Creación de la ventana principal
    form = FormularioUsuario()

    # Inicia el bucle de eventos (event loop) y asegura un cierre limpio al finalizar
    sys.exit(app.exec())