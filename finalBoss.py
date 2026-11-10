import sys
# Importaciones de la API Core de PyQt6 para el modelo de datos personalizado
from PyQt6.QtCore import Qt, QAbstractListModel, QModelIndex
# Importaciones para el manejo de fuentes, color y paletas gráficas en la UI
from PyQt6.QtGui import QPalette, QColor, QFont
# Importaciones de componentes del catálogo de Widgets de PyQt6
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QStackedLayout, QLabel, QLineEdit, QTextEdit,
    QPushButton, QComboBox, QCheckBox, QRadioButton, QGroupBox,
    QMessageBox, QListView, QFrame
)


# ==============================================================================
# SECCIÓN 1: MODELO PERSONALIZADO DE DATOS (ModeloTarefas)
# ==============================================================================
class ModeloTarefas(QAbstractListModel):
    """
    Modelo de datos para QListView siguiendo el patrón de arquitectura Modelo/Vista de Qt.
    Mantiene una lista interna de tuplas con la estructura: (completada: bool, texto: str).
    """

    def __init__(self, tarefas=None):
        super().__init__()
        # Inicializa la lista de tareas recibida o crea una lista vacía por defecto
        self.tarefas = tarefas or []

    def rowCount(self, parent=QModelIndex()):
        """Devuelve el número total de elementos/filas presentes en el modelo de datos."""
        return len(self.tarefas)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        """
        Proporciona los datos correspondientes a un índice de celda según el rol solicitado.
        Formatea visualmente la casilla según si la tarea está completada o no.
        """
        if not index.isValid():
            return None

        # Rol de visualización textual de cada elemento de la lista
        if role == Qt.ItemDataRole.DisplayRole:
            estado, texto = self.tarefas[index.row()]
            marca = "[✓] " if estado else "[ ] "
            return f"{marca}{texto}"

        return None

    def engadir_tarefa(self, texto):
        """
        Añade una nueva tarea al modelo notificando previamente a la vista mediante
        'beginInsertRows' y 'endInsertRows' para asegurar una actualización limpia.
        """
        if not texto.strip():
            return
        posicion = len(self.tarefas)
        # Notifica a Qt que se insertará una nueva fila en una posición determinada
        self.beginInsertRows(QModelIndex(), posicion, posicion)
        self.tarefas.append((False, texto))
        self.endInsertRows()

    def borrar_tarefas(self, posicions):
        """
        Elimina las tareas ubicadas en las posiciones recibidas por parámetro.
        Recorre en orden inverso para evitar desfasar los índices durante el borrado.
        """
        for pos in sorted(posicions, reverse=True):
            self.beginRemoveRows(QModelIndex(), pos, pos)
            del self.tarefas[pos]
            self.endRemoveRows()

    def marcar_como_feito(self, posicions):
        """
        Cambia el estado completado (True) de las tareas seleccionadas y
        emite la señal 'dataChanged' para refrescar la visualización en la UI.
        """
        for pos in posicions:
            _, texto = self.tarefas[pos]
            self.tarefas[pos] = (True, texto)
            idx = self.index(pos)
            # Notifica a la vista que los datos de la fila especificada han cambiado
            self.dataChanged.emit(idx, idx, [Qt.ItemDataRole.DisplayRole])


# ==============================================================================
# SECCIÓN 2: VENTANA PRINCIPAL Y NAVEGACIÓN DIVERSIFICADA (QStackedLayout)
# ==============================================================================
class AplicacionIntegrada(QMainWindow):
    """
    Ventana principal que unifica todos los módulos de ejemplo en una única interfaz.
    Integra una barra lateral de menú y un área apilada (QStackedLayout) gestionada por QPalette.
    """

    def __init__(self):
        super().__init__()

        # Configuración básica de ventana
        self.setWindowTitle("Suite de Formularios PyQt6 (Configuración mediante QPalette)")
        self.setMinimumSize(950, 650)

        # Contenedor central principal con distribución horizontal (Menú lateral + Vistas)
        contenedor_principal = QWidget()
        layout_principal = QHBoxLayout(contenedor_principal)
        layout_principal.setContentsMargins(0, 0, 0, 0)
        layout_principal.setSpacing(0)

        # ----------------------------------------------------------------------
        # MENÚ LATERAL (Panel con QFrame y QPalette personalizada)
        # ----------------------------------------------------------------------
        self.panel_lateral = QFrame()
        # setAutoFillBackground permite que el widget aplique el color asignado en su QPalette
        self.panel_lateral.setAutoFillBackground(True)
        self._configurar_paleta_panel_lateral()  # Aplica la paleta en tonos oscuros

        layout_menu = QVBoxLayout(self.panel_lateral)
        layout_menu.setContentsMargins(15, 20, 15, 20)
        layout_menu.setSpacing(10)

        # Etiqueta de título del menú
        lbl_titulo_menu = QLabel("PANEL DE CONTROL")
        fuente_titulo = QFont("Segoe UI", 11, QFont.Weight.Bold)
        lbl_titulo_menu.setFont(fuente_titulo)
        layout_menu.addWidget(lbl_titulo_menu)

        # Creación de los botones de navegación entre las vistas
        self.btn_nav_registro = QPushButton("Registro de Usuario")
        self.btn_nav_bloqueo = QPushButton("Perfil (Bloqueo/Edición)")
        self.btn_nav_matricula = QPushButton("Formulario Dinámico")
        self.btn_nav_wizard = QPushButton("Asistente Paso a Paso")
        self.btn_nav_galeria = QPushButton("Galería de Tarjetas")
        self.btn_nav_editor = QPushButton("Editor de Texto")
        self.btn_nav_tareas = QPushButton("Gestión de Tareas")

        self.lista_botones_nav = [
            self.btn_nav_registro, self.btn_nav_bloqueo, self.btn_nav_matricula,
            self.btn_nav_wizard, self.btn_nav_galeria, self.btn_nav_editor, self.btn_nav_tareas
        ]

        # Estilización e interconexión individual para cada botón del menú
        for idx, btn in enumerate(self.lista_botones_nav):
            btn.setCheckable(True)
            self._aplicar_paleta_boton_menu(btn)
            layout_menu.addWidget(btn)
            # Conexión mediante lambda con el índice correspondiente a la vista
            btn.clicked.connect(lambda _, i=idx: self.cambiar_pagina(i))

        # Espaciador vertical para empujar los botones hacia la parte superior
        layout_menu.addStretch()

        # ----------------------------------------------------------------------
        # ÁREA DE CONTENIDO PRINCIPAL (QStackedLayout)
        # ----------------------------------------------------------------------
        self.stack_layout = QStackedLayout()

        # Inserción ordenada de las 7 páginas/vistas de la suite al layout apilado
        self.stack_layout.addWidget(self._crear_vista_registro())  # Índice 0
        self.stack_layout.addWidget(self._crear_vista_bloqueo())  # Índice 1
        self.stack_layout.addWidget(self._crear_vista_matriculacion())  # Índice 2
        self.stack_layout.addWidget(self._crear_vista_wizard())  # Índice 3
        self.stack_layout.addWidget(self._crear_vista_galeria())  # Índice 4
        self.stack_layout.addWidget(self._crear_vista_editor())  # Índice 5
        self.stack_layout.addWidget(self._crear_vista_tareas())  # Índice 6

        contenedor_contenido = QWidget()
        contenedor_contenido.setLayout(self.stack_layout)

        # Proporción de ancho: 1 para la barra lateral y 4 para el contenido
        layout_principal.addWidget(self.panel_lateral, 1)
        layout_principal.addWidget(contenedor_contenido, 4)

        self.setCentralWidget(contenedor_principal)

        # Selección inicial del primer módulo (Página 0)
        self.cambiar_pagina(0)

    def cambiar_pagina(self, index):
        """
        Alterna la página activa dentro del QStackedLayout
        y actualiza visualmente el estado del botón correspondiente.
        """
        self.stack_layout.setCurrentIndex(index)
        for i, btn in enumerate(self.lista_botones_nav):
            btn.setChecked(i == index)
            # Actualiza colores y apariencia del botón según si está activo o inactivo
            self._actualizar_estado_boton_menu(btn, i == index)

    # ==========================================================================
    # SECCIÓN DE GESTIÓN Y CONFIGURACIÓN DE PALETAS DE COLOR (QPalette)
    # ==========================================================================
    def _configurar_paleta_panel_lateral(self):
        """Aplica la combinación de colores oscuros para la barra lateral mediante QPalette."""
        paleta = self.panel_lateral.palette()
        paleta.setColor(QPalette.ColorRole.Window, QColor(30, 30, 46))  # Fondo azul noche
        paleta.setColor(QPalette.ColorRole.WindowText, QColor(205, 214, 244))  # Texto en tono pastel claro
        self.panel_lateral.setPalette(paleta)

    def _aplicar_paleta_boton_menu(self, boton: QPushButton):
        """Asigna la paleta de colores base para los botones del menú lateral."""
        boton.setAutoFillBackground(True)
        paleta = boton.palette()
        paleta.setColor(QPalette.ColorRole.Button, QColor(45, 45, 68))
        paleta.setColor(QPalette.ColorRole.ButtonText, QColor(205, 214, 244))
        boton.setPalette(paleta)

    def _actualizar_estado_boton_menu(self, boton: QPushButton, seleccionado: bool):
        """Actualiza la paleta de un botón alternando entre el estado activo e inactivo."""
        paleta = boton.palette()
        if seleccionado:
            paleta.setColor(QPalette.ColorRole.Button, QColor(137, 180, 250))  # Azul celeste brillante
            paleta.setColor(QPalette.ColorRole.ButtonText, QColor(17, 17, 27))  # Texto contrastante oscuro
        else:
            paleta.setColor(QPalette.ColorRole.Button, QColor(45, 45, 68))
            paleta.setColor(QPalette.ColorRole.ButtonText, QColor(205, 214, 244))
        boton.setPalette(paleta)

    # ==========================================================================
    # PÁGINA 1: FORMULARIO DE REGISTRO CON VALIDACIÓN
    # ==========================================================================
    def _crear_vista_registro(self):
        """Construye la vista de registro de usuario con validaciones de campos."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        lbl_titulo = QLabel("Formulario de Registro de Usuario")
        lbl_titulo.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        self.txt_reg_nombre = QLineEdit()
        self.txt_reg_nombre.setPlaceholderText("Ingrese su nombre")

        self.txt_reg_email = QLineEdit()
        self.txt_reg_email.setPlaceholderText("ejemplo@correo.com")

        self.txt_reg_password = QLineEdit()
        self.txt_reg_password.setPlaceholderText("Ingrese su contraseña")
        self.txt_reg_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.combo_reg_perfil = QComboBox()
        self.combo_reg_perfil.addItems(["Estudiante", "Profesor", "Invitado"])

        self.chk_reg_terminos = QCheckBox("Acepto los términos y condiciones de uso")

        btn_registrar = QPushButton("Registrar Usuario")
        # Personalización del botón primario con QPalette
        paleta_btn = btn_registrar.palette()
        paleta_btn.setColor(QPalette.ColorRole.Button, QColor(67, 97, 238))
        paleta_btn.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        btn_registrar.setPalette(paleta_btn)
        btn_registrar.clicked.connect(self._validar_registro)

        layout.addWidget(lbl_titulo)
        layout.addWidget(QLabel("Nombre completo:"))
        layout.addWidget(self.txt_reg_nombre)
        layout.addWidget(QLabel("Correo Electrónico:"))
        layout.addWidget(self.txt_reg_email)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.txt_reg_password)
        layout.addWidget(QLabel("Perfil de Usuario:"))
        layout.addWidget(self.combo_reg_perfil)
        layout.addWidget(self.chk_reg_terminos)
        layout.addWidget(btn_registrar)
        layout.addStretch()

        return widget

    def _validar_registro(self):
        """Comprueba la integridad de los datos de registro antes de confirmar la entrada."""
        nombre = self.txt_reg_nombre.text().strip()
        email = self.txt_reg_email.text().strip()
        password = self.txt_reg_password.text().strip()

        if not nombre or not email or not password:
            QMessageBox.warning(self, "Campos Vacíos", "Todos los campos de texto son obligatorios.")
            return

        if "@" not in email:
            QMessageBox.warning(self, "Formato Incorrecto", "El email debe incluir el carácter '@'.")
            return

        if not self.chk_reg_terminos.isChecked():
            QMessageBox.warning(self, "Términos Requeridos", "Debes aceptar los términos y condiciones.")
            return

        QMessageBox.information(
            self, "Registro Exitoso",
            f"¡Usuario '{nombre}' registrado correctamente como {self.combo_reg_perfil.currentText()}!"
        )

    # ==========================================================================
    # PÁGINA 2: MODO LECTURA / EDICIÓN (BLOQUEO Y DESBLOQUEO)
    # ==========================================================================
    def _crear_vista_bloqueo(self):
        """Construye la vista de datos de perfil con conmutación de estado de edición."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        lbl_titulo = QLabel("Perfil de Usuario (Modo Lectura / Edición)")
        lbl_titulo.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        self.lnombre_bloq = QLineEdit("Juan Pérez")
        self.lemail_bloq = QLineEdit("juan.perez@dominio.com")
        self.ltelefono_bloq = QLineEdit("600123456")

        # Inicia con los campos bloqueados para edición
        for input_field in [self.lnombre_bloq, self.lemail_bloq, self.ltelefono_bloq]:
            input_field.setEnabled(False)

        self.btn_editar_bloq = QPushButton("Editar Campos")
        self.btn_guardar_bloq = QPushButton("Guardar Cambios")
        self.btn_guardar_bloq.setEnabled(False)

        self.btn_editar_bloq.clicked.connect(self._habilitar_edicion_bloq)
        self.btn_guardar_bloq.clicked.connect(self._guardar_cambios_bloq)

        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.btn_editar_bloq)
        layout_botones.addWidget(self.btn_guardar_bloq)

        layout.addWidget(lbl_titulo)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(self.lnombre_bloq)
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.lemail_bloq)
        layout.addWidget(QLabel("Teléfono:"))
        layout.addWidget(self.ltelefono_bloq)
        layout.addLayout(layout_botones)
        layout.addStretch()

        return widget

    def _habilitar_edicion_bloq(self):
        """Habilita la edición en todos los inputs y conmuta el estado de la botonera."""
        for input_field in [self.lnombre_bloq, self.lemail_bloq, self.ltelefono_bloq]:
            input_field.setEnabled(True)
        self.btn_guardar_bloq.setEnabled(True)
        self.btn_editar_bloq.setEnabled(False)

    def _guardar_cambios_bloq(self):
        """Valida que los campos no estén vacíos y bloquea la edición nuevamente."""
        if not self.lnombre_bloq.text().strip() or not self.lemail_bloq.text().strip() or not self.ltelefono_bloq.text().strip():
            QMessageBox.warning(self, "Error de Validación", "Todos los campos deben estar rellenos.")
        else:
            QMessageBox.information(self, "Éxito", "Datos de perfil actualizados correctamente.")
            for input_field in [self.lnombre_bloq, self.lemail_bloq, self.ltelefono_bloq]:
                input_field.setEnabled(False)
            self.btn_guardar_bloq.setEnabled(False)
            self.btn_editar_bloq.setEnabled(True)

    # ==========================================================================
    # PÁGINA 3: FORMULARIO DINÁMICO DE MATRICULACIÓN
    # ==========================================================================
    def _crear_vista_matriculacion(self):
        """Construye un formulario dinámico que conmuta subpaneles según la selección del QComboBox."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        lbl_titulo = QLabel("Formulario Dinámico de Matriculación")
        lbl_titulo.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        self.cmb_tipo_mat = QComboBox()
        self.cmb_tipo_mat.addItems(["Alumno", "Profesor", "PAS (Personal de Administración)"])
        self.cmb_tipo_mat.setCurrentIndex(-1)
        self.cmb_tipo_mat.setPlaceholderText("Seleccione un tipo de perfil...")

        # Layout apilado para alternar dinámicamente entre subpaneles
        self.stack_mat = QStackedLayout()
        self.stack_mat.addWidget(QLabel("Selecciona una opción en el menú desplegable superior."))
        self.stack_mat.addWidget(self._crear_subpanel_alumno())
        self.stack_mat.addWidget(self._crear_subpanel_profesor())
        self.stack_mat.addWidget(self._crear_subpanel_pas())

        # Vincula la posición del combo box con el índice correspondiente en el QStackedLayout
        self.cmb_tipo_mat.currentIndexChanged.connect(
            lambda idx: self.stack_mat.setCurrentIndex(idx + 1 if idx >= 0 else 0)
        )

        layout.addWidget(lbl_titulo)
        layout.addWidget(self.cmb_tipo_mat)
        layout.addLayout(self.stack_mat)
        layout.addStretch()

        return widget

    def _crear_subpanel_alumno(self):
        """Genera los campos específicos para el perfil de Alumno mediante un QGridLayout."""
        panel = QWidget()
        grid = QGridLayout(panel)

        cmb_ciclo = QComboBox()
        cmb_ciclo.addItems(["DAM", "ASIR", "SMR", "IEA", "ADF"])

        rbt_1 = QRadioButton("Primer Curso")
        rbt_2 = QRadioButton("Segundo Curso")
        layout_radio = QHBoxLayout()
        layout_radio.addWidget(rbt_1)
        layout_radio.addWidget(rbt_2)

        grid.addWidget(QLabel("Ciclo Formativo:"), 0, 0)
        grid.addWidget(cmb_ciclo, 0, 1)
        grid.addWidget(QLabel("Curso:"), 1, 0)
        grid.addLayout(layout_radio, 1, 1)
        grid.addWidget(QLabel("Nombre Madre:"), 2, 0)
        grid.addWidget(QLineEdit(), 2, 1)
        grid.addWidget(QLabel("Nombre Padre:"), 3, 0)
        grid.addWidget(QLineEdit(), 3, 1)

        return panel

    def _crear_subpanel_profesor(self):
        """Genera el panel de opciones avanzadas para el perfil de Profesor con QGroupBox."""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        chk_tutor = QCheckBox("¿Es Tutor del grupo?")

        grp_curso = QGroupBox("Curso Asignado")
        layout_c = QHBoxLayout(grp_curso)
        layout_c.addWidget(QRadioButton("1º Año"))
        layout_c.addWidget(QRadioButton("2º Año"))

        grp_nivel = QGroupBox("Nivel Educativo")
        layout_n = QHBoxLayout(grp_nivel)
        layout_n.addWidget(QRadioButton("Ciclo Básico"))
        layout_n.addWidget(QRadioButton("Ciclo Medio"))
        layout_n.addWidget(QRadioButton("Ciclo Superior"))

        layout.addWidget(chk_tutor)
        layout.addWidget(grp_curso)
        layout.addWidget(grp_nivel)

        return panel

    def _crear_subpanel_pas(self):
        """Genera el panel de formulario básico para el personal de administración (PAS)."""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        cmb_ocupacion = QComboBox()
        cmb_ocupacion.addItems(["Secretario/a", "Conserje/Bedel", "Administración"])

        layout.addWidget(QLabel("Puesto / Ocupación:"))
        layout.addWidget(cmb_ocupacion)
        layout.addWidget(QLabel("Nombre:"))
        layout.addWidget(QLineEdit())
        layout.addWidget(QLabel("Apellidos:"))
        layout.addWidget(QLineEdit())

        return panel

    # ==========================================================================
    # PÁGINA 4: ASISTENTE PASO A PASO (WIZARD)
    # ==========================================================================
    def _crear_vista_wizard(self):
        """Construye un asistente por pasos utilizando tarjetas coloreadas por QPalette."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        lbl_titulo = QLabel("Asistente de Configuración (Wizard)")
        lbl_titulo.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        self.stack_wizard = QStackedLayout()

        pasos_texto = [
            "Paso 1: Configuración Inicial de Datos Personales",
            "Paso 2: Selección de Preferencias de Usuario",
            "Paso 3: Confirmación y Resumen Final"
        ]

        # Creación y aplicación de QPalette distintiva para cada pantalla del wizard
        for texto in pasos_texto:
            lbl_paso = QLabel(texto)
            lbl_paso.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_paso.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
            lbl_paso.setAutoFillBackground(True)

            paleta_card = lbl_paso.palette()
            paleta_card.setColor(QPalette.ColorRole.Window, QColor(230, 240, 255))
            paleta_card.setColor(QPalette.ColorRole.WindowText, QColor(41, 128, 185))
            lbl_paso.setPalette(paleta_card)

            self.stack_wizard.addWidget(lbl_paso)

        self.btn_wiz_anterior = QPushButton("Anterior")
        self.btn_wiz_siguiente = QPushButton("Siguiente")
        self.btn_wiz_anterior.setEnabled(False)

        self.btn_wiz_siguiente.clicked.connect(self._avanzar_wizard)
        self.btn_wiz_anterior.clicked.connect(self._retroceder_wizard)

        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.btn_wiz_anterior)
        layout_botones.addWidget(self.btn_wiz_siguiente)

        layout.addWidget(lbl_titulo)
        layout.addLayout(self.stack_wizard)
        layout.addLayout(layout_botones)

        return widget

    def _actualizar_botones_wizard(self):
        """Evalúa el índice activo para habilitar/deshabilitar la navegación del asistente."""
        idx = self.stack_wizard.currentIndex()
        total = self.stack_wizard.count()
        self.btn_wiz_anterior.setEnabled(idx > 0)
        self.btn_wiz_siguiente.setEnabled(idx < total - 1)

    def _avanzar_wizard(self):
        """Avanza al siguiente paso del asistente."""
        idx = self.stack_wizard.currentIndex()
        if idx < self.stack_wizard.count() - 1:
            self.stack_wizard.setCurrentIndex(idx + 1)
            self._actualizar_botones_wizard()

    def _retroceder_wizard(self):
        """Retrocede al paso anterior del asistente."""
        idx = self.stack_wizard.currentIndex()
        if idx > 0:
            self.stack_wizard.setCurrentIndex(idx - 1)
            self._actualizar_botones_wizard()

    # ==========================================================================
    # PÁGINA 5: GALERÍA DE TARJETAS EN CUADRÍCULA 3x3
    # ==========================================================================
    def _crear_vista_galeria(self):
        """Genera una matriz dinámica de botones 3x3 que actualiza un panel de detalles."""
        widget = QWidget()
        layout = QHBoxLayout(widget)

        grid_cuadricula = QGridLayout()
        self.lbl_detalle_galeria = QLabel("Selecciona una tarjeta para ver sus detalles")
        self.lbl_detalle_galeria.setWordWrap(True)
        self.lbl_detalle_galeria.setAutoFillBackground(True)
        self.lbl_detalle_galeria.setFont(QFont("Segoe UI", 11))

        # Personalización de la paleta para la tarjeta explicativa lateral
        paleta_detalle = self.lbl_detalle_galeria.palette()
        paleta_detalle.setColor(QPalette.ColorRole.Window, QColor(240, 243, 246))
        paleta_detalle.setColor(QPalette.ColorRole.WindowText, QColor(44, 62, 80))
        self.lbl_detalle_galeria.setPalette(paleta_detalle)

        # Generación iterativa de la matriz 3x3 de tarjetas/botones
        for fila in range(3):
            for col in range(3):
                num = fila * 3 + col + 1
                btn = QPushButton(f"Tarjeta {num}")

                # Estilo individual de color para cada botón mediante QPalette
                paleta_tarjeta = btn.palette()
                paleta_tarjeta.setColor(QPalette.ColorRole.Button, QColor(255, 255, 255))
                paleta_tarjeta.setColor(QPalette.ColorRole.ButtonText, QColor(52, 152, 219))
                btn.setPalette(paleta_tarjeta)

                grid_cuadricula.addWidget(btn, fila, col)
                # Conexión del clic hacia el método de detalle dinámico
                btn.clicked.connect(self._mostrar_detalle_tarjeta)

        layout.addLayout(grid_cuadricula, 2)
        layout.addWidget(self.lbl_detalle_galeria, 1)

        return widget

    def _mostrar_detalle_tarjeta(self):
        """Captura dinámicamente cuál botón emitió la señal mediante self.sender()."""
        boton_pulsado = self.sender()
        if boton_pulsado:
            self.lbl_detalle_galeria.setText(
                f"Has seleccionado la **{boton_pulsado.text()}**.\n\n"
                f"Capturado dinámicamente mediante el método 'self.sender()'."
            )

    # ==========================================================================
    # PÁGINA 6: VISOR Y EDITOR DE TEXTO MULTILÍNEA
    # ==========================================================================
    def _crear_vista_editor(self):
        """Crea el editor multilínea con funciones de formato y conteo dinámico."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        lbl_titulo = QLabel("Visor y Editor de Texto Multilínea")
        lbl_titulo.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        btn_mayus = QPushButton("Convertir a Mayúsculas")
        btn_limpiar = QPushButton("Limpiar Texto")
        btn_bloquear = QPushButton("Bloquear / Desbloquear")

        layout_herramientas = QHBoxLayout()
        layout_herramientas.addWidget(btn_mayus)
        layout_herramientas.addWidget(btn_limpiar)
        layout_herramientas.addWidget(btn_bloquear)

        self.txt_editor = QTextEdit()
        self.lbl_contador_texto = QLabel("Caracteres totales: 0")

        # Conexión directa mediante expresiones lambda a las acciones del editor
        btn_mayus.clicked.connect(lambda: self.txt_editor.setPlainText(self.txt_editor.toPlainText().upper()))
        btn_limpiar.clicked.connect(self.txt_editor.clear)
        btn_bloquear.clicked.connect(lambda: self.txt_editor.setReadOnly(not self.txt_editor.isReadOnly()))
        self.txt_editor.textChanged.connect(
            lambda: self.lbl_contador_texto.setText(f"Caracteres totales: {len(self.txt_editor.toPlainText())}")
        )

        layout.addWidget(lbl_titulo)
        layout.addLayout(layout_herramientas)
        layout.addWidget(self.txt_editor)
        layout.addWidget(self.lbl_contador_texto)

        return widget

    # ==========================================================================
    # PÁGINA 7: GESTIÓN DE TAREAS (MODELO / VISTA CON QListView)
    # ==========================================================================
    def _crear_vista_tareas(self):
        """Construye el panel de gestión de tareas utilizando la arquitectura Modelo/Vista."""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        lbl_titulo = QLabel("Gestión de Tareas (Arquitectura Modelo / Vista)")
        lbl_titulo.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        # Instanciación del modelo de datos personalizado con valores por defecto
        tareas_iniciales = [(True, "Aprender PyQt6"), (False, "Configurar QPalette"), (False, "Probar QListView")]
        self.modelo_tareas = ModeloTarefas(tareas_iniciales)

        # Configuración de la vista de lista (QListView) vinculada al modelo
        self.lst_tareas = QListView()
        self.lst_tareas.setModel(self.modelo_tareas)
        self.lst_tareas.setSelectionMode(QListView.SelectionMode.MultiSelection)

        self.txt_nueva_tarea = QLineEdit()
        self.txt_nueva_tarea.setPlaceholderText("Escriba una nueva tarea...")

        btn_agregar = QPushButton("Añadir Tarea")
        btn_completar = QPushButton("Marcar Como Hecha")
        btn_borrar = QPushButton("Eliminar Seleccionadas")

        # Vinculación de botones a métodos manipuladores del modelo
        btn_agregar.clicked.connect(self._agregar_tarea)
        btn_completar.clicked.connect(self._completar_tarea)
        btn_borrar.clicked.connect(self._borrar_tarea)

        layout_acc = QHBoxLayout()
        layout_acc.addWidget(btn_completar)
        layout_acc.addWidget(btn_borrar)

        layout.addWidget(lbl_titulo)
        layout.addWidget(self.lst_tareas)
        layout.addWidget(self.txt_nueva_tarea)
        layout.addWidget(btn_agregar)
        layout.addLayout(layout_acc)

        return widget

    def _agregar_tarea(self):
        """Inserta un nuevo elemento en el modelo de datos."""
        texto = self.txt_nueva_tarea.text()
        if texto:
            self.modelo_tareas.engadir_tarefa(texto)
            self.txt_nueva_tarea.clear()

    def _completar_tarea(self):
        """Marca como completadas las tareas seleccionadas en el QListView."""
        filas = [idx.row() for idx in self.lst_tareas.selectedIndexes()]
        if filas:
            self.modelo_tareas.marcar_como_feito(filas)

    def _borrar_tarea(self):
        """Elimina las tareas seleccionadas del modelo."""
        filas = [idx.row() for idx in self.lst_tareas.selectedIndexes()]
        if filas:
            self.modelo_tareas.borrar_tarefas(filas)


# ==============================================================================
# CONFIGURACIÓN GENERAL DE LA PALETA GLOBAL (QPalette + Fusion Style)
# ==============================================================================
def aplicar_paleta_global(app: QApplication):
    """
    Define y establece la paleta de colores global de la aplicación.
    Se utiliza el estilo 'Fusion' para asegurar compatibilidad multiplataforma.
    """
    app.setStyle("Fusion")

    paleta_global = QPalette()

    # 1. Colores para el fondo general de la ventana (Window y WindowText)
    paleta_global.setColor(QPalette.ColorRole.Window, QColor(245, 246, 250))
    paleta_global.setColor(QPalette.ColorRole.WindowText, QColor(44, 62, 80))

    # 2. Colores de áreas editables, listas y entradas (Base y Text)
    paleta_global.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    paleta_global.setColor(QPalette.ColorRole.Text, QColor(44, 62, 80))

    # 3. Colores por defecto para botones (Button y ButtonText)
    paleta_global.setColor(QPalette.ColorRole.Button, QColor(236, 240, 241))
    paleta_global.setColor(QPalette.ColorRole.ButtonText, QColor(44, 62, 80))

    # 4. Colores para estados seleccionados o destacados (Highlight y HighlightedText)
    paleta_global.setColor(QPalette.ColorRole.Highlight, QColor(52, 152, 219))
    paleta_global.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))

    # 5. Colores para el grupo de elementos deshabilitados (Disabled)
    paleta_global.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, QColor(149, 165, 166))
    paleta_global.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, QColor(149, 165, 166))
    paleta_global.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, QColor(149, 165, 166))
    paleta_global.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, QColor(230, 233, 237))

    app.setPalette(paleta_global)


# ==============================================================================
# BLOQUE DE EJECUCIÓN PRINCIPAL
# ==============================================================================
if __name__ == "__main__":
    # Inicialización de la aplicación global PyQt
    app = QApplication(sys.argv)

    # Configuración de la paleta de colores global y el estilo Fusion
    aplicar_paleta_global(app)

    # Creación e inicio de la ventana de la aplicación unificada
    ventana = AplicacionIntegrada()
    ventana.show()

    # Bucle de eventos principal (Event Loop)
    sys.exit(app.exec())