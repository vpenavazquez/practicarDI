import sys
# Importaciones necesarias de PyQt6 para la construcción de la interfaz y ventanas emergentes
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QComboBox, QLineEdit, QCheckBox, QStackedLayout, QHBoxLayout,
    QPushButton, QMessageBox
)
# Importaciones gráficas de paletas (no utilizadas en este código específico)
from PyQt6.QtGui import QColor, QPalette


class FormularioRegistro(QMainWindow):
    """
    Clase principal que implementa un formulario completo de registro de usuario.
    Incluye validación de campos vacíos, formato básico de email y aceptación de términos.
    """

    def __init__(self):
        super().__init__()

        # Configuración de título y dimensiones mínimas de la ventana
        self.setWindowTitle("Registro Usuario")
        self.setMinimumSize(350, 250)

        # Layout vertical principal para disponer los elementos del formulario en columna
        layout = QVBoxLayout()

        # Creación de las etiquetas y campos de entrada de texto
        nombre = QLabel("Nombre")
        self.txt_nombre = QLineEdit()

        email = QLabel("Email")
        self.txt_email = QLineEdit()

        password = QLabel("Password")
        self.txt_password = QLineEdit()

        # Configuración de los textos de sugerencia (placeholders) en los campos
        self.txt_nombre.setPlaceholderText("Ingrese un nombre")
        self.txt_email.setPlaceholderText("Ingrese un email")
        self.txt_password.setPlaceholderText("Ingrese un password")

        # Oculta los caracteres introducidos en el campo de contraseña por motivos de seguridad
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)

        # Creación y llenado del menú desplegable de selección de perfil
        perfil = QLabel("Perfil")
        self.combo_perfil = QComboBox()
        self.combo_perfil.addItems(["Estudiante", "Profesor", "Invitado"])

        # Casilla de verificación (QCheckBox) para la aceptación de términos
        self.chk_terminos = QCheckBox("Acepto los términos y condiciones")

        # Botón para procesar el registro
        self.btn_registrar = QPushButton("Registrar")

        # Inserción secuencial de todos los elementos dentro del layout vertical
        layout.addWidget(nombre)
        layout.addWidget(self.txt_nombre)
        layout.addWidget(email)
        layout.addWidget(self.txt_email)
        layout.addWidget(password)
        layout.addWidget(self.txt_password)
        layout.addWidget(perfil)
        layout.addWidget(self.combo_perfil)
        layout.addWidget(self.chk_terminos)
        layout.addWidget(self.btn_registrar)

        # Creación del widget contenedor central requerido por QMainWindow
        contenedor = QWidget()
        contenedor.setLayout(layout)
        self.setCentralWidget(contenedor)

        # Vinculación del evento clic del botón con el método de validación
        self.btn_registrar.clicked.connect(self.validar_registro)

        # Muestra la ventana en pantalla
        self.show()

    def validar_registro(self):
        """
        Método manejador que realiza las comprobaciones de validación de los datos ingresados.
        Muestra mensajes de advertencia o éxito según corresponda.
        """
        # Obtiene el texto de los campos limpiando espacios en blanco al inicio y final
        nombre = self.txt_nombre.text().strip()
        email = self.txt_email.text().strip()
        password = self.txt_password.text().strip()

        # Validación 1: Verificar que ninguno de los campos de texto esté vacío
        if not nombre or not email or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return False

        # Validación 2: Comprobación básica de formato de correo electrónico
        if "@" not in email:
            QMessageBox.warning(self, "Error", "El email debe ser válido (debe incluir '@')")
            return

        # Validación 3: Verificar que la casilla de términos y condiciones esté marcada
        if not self.chk_terminos.isChecked():
            QMessageBox.warning(self, "Error", "Debes aceptar los términos y condiciones.")
            return

        # Obtención de la opción seleccionada actualmente en el QComboBox
        perfil_elegido = self.combo_perfil.currentText()

        # Muestra un mensaje emergente de éxito tras superar todas las validaciones
        QMessageBox.information(self, "LETSGO", "Registro perfe")


# Bloque de ejecución principal
if __name__ == '__main__':
    # Instancia de la aplicación PyQt
    app = QApplication(sys.argv)

    # Creación e inicialización del formulario
    window = FormularioRegistro()

    # Ejecución del bucle principal de eventos
    sys.exit(app.exec())