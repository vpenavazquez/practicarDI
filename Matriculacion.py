import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QStackedLayout,
    QLabel, QLineEdit, QPushButton, QComboBox,
    QCheckBox, QRadioButton, QGroupBox, QMessageBox
)


class Matriculacion(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Matriculación")
        self.resize(500, 400) # Ancho, Alto

        # 1. Layout Principal donde irá todo
        layout_principal = QVBoxLayout()

        self.cmbTipo = QComboBox()
        self.cmbTipo.addItems(("Alumno","Profesores", "Pas"))
        self.cmbTipo.setCurrentIndex(-1)# Empieza sin ninguna opción seleccionada
        self.cmbTipo.currentIndexChanged.connect(self.on_cmbTipo_setCurrentChanged)

        layout_principal.addWidget(self.cmbTipo)
        self.ventanas = QStackedLayout()

        # Crear vistas
        self.vista_vacia = QWidget()
        self.ventanas.addWidget(self.vista_vacia)
        #----------------------------------------------------

        # Panel Alumno
        self.vista_alumno = QWidget()
        paginaAluno = QGridLayout()

        #desplegable ciclo
        lblCiclo = QLabel("Ciclo")
        self.cmdCiclo = QComboBox()
        ciclos = ("DAM", "ASIR", "SMR", "IEA", "ADF")
        self.cmdCiclo.addItems(ciclos)
        self.cmdCiclo.setCurrentIndex(-1)

        #selectores radio
        self.rbtPrimeiro = QRadioButton("Primeiro")
        self.rbtSegundo = QRadioButton("Segundo")
        caixaRadio = QHBoxLayout()
        caixaRadio.addWidget(self.rbtPrimeiro)
        caixaRadio.addWidget(self.rbtSegundo)

        #selector año
        self.cmbAnoMatricula = QComboBox()
        cursosMatricula = ("25/26", "26/27", "27/28")
        self.cmbAnoMatricula.addItems(cursosMatricula)

        self.vista_profesor = QLabel("Panel de Profesores")
        self.vista_pas = QLabel("Panel de PAS")

        #Añadir nombres de padre y madre
        lblNomeNai = QLabel("Nome Nai")
        self.txtNomeNai = QtWidgets.QLineEdit()
        lblNomePai = QLabel("Nome Pai")
        self.txtNomePai = QtWidgets.QLineEdit()

        # guardar en paginaAluno

        paginaAluno.addWidget(lblCiclo, 0, 0)
        paginaAluno.addWidget(self.cmdCiclo, 0, 1)
        paginaAluno.addLayout(caixaRadio, 1, 0, 1, 2)
        paginaAluno.addWidget(QLabel("Ano Matrícula"), 2, 0)
        paginaAluno.addWidget(self.cmbAnoMatricula, 2, 1)
        paginaAluno.addWidget(lblNomeNai, 3, 0)
        paginaAluno.addWidget(self.txtNomeNai, 3, 1)
        paginaAluno.addWidget(lblNomePai, 4, 0)
        paginaAluno.addWidget(self.txtNomePai, 4, 1)
        self.vista_alumno.setLayout(paginaAluno)

        # ----------------------------------------------------
        # Paneles Profesores
        self.vista_profesor = QWidget()
        paginaProfesor = QVBoxLayout()

        # RadioButton Titor
        self.rbtTitor = QRadioButton("É titor?")
        paginaProfesor.addWidget(self.rbtTitor)

        # Selección de Ciclo
        caixaCicloProf = QHBoxLayout()
        lblCicloProf = QLabel("Ciclo:")
        self.cmbCicloProf = QComboBox()
        self.cmbCicloProf.addItems(ciclos)
        self.cmbCicloProf.setCurrentIndex(-1)
        caixaCicloProf.addWidget(lblCicloProf)
        caixaCicloProf.addWidget(self.cmbCicloProf)
        paginaProfesor.addLayout(caixaCicloProf)

        # Anos (Primeiro / Segundo)
        grupoAnos = QGroupBox("Curso")
        caixaAnos = QHBoxLayout()
        self.rbtPrimeiroAno = QRadioButton("1º Ano")
        self.rbtSegundoAno = QRadioButton("2º Ano")
        caixaAnos.addWidget(self.rbtPrimeiroAno)
        caixaAnos.addWidget(self.rbtSegundoAno)
        grupoAnos.setLayout(caixaAnos)
        paginaProfesor.addWidget(grupoAnos)

        # Nivel do Ciclo
        grupoNivel = QGroupBox("Nivel do ciclo")
        caixaNivel = QHBoxLayout()
        self.rbtBasico = QRadioButton("Ciclo Básico")
        self.rbtMedio = QRadioButton("Ciclo Medio")
        self.rbtSuperior = QRadioButton("Ciclo Superior")
        caixaNivel.addWidget(self.rbtBasico)
        caixaNivel.addWidget(self.rbtMedio)
        caixaNivel.addWidget(self.rbtSuperior)
        grupoNivel.setLayout(caixaNivel)
        paginaProfesor.addWidget(grupoNivel)

        self.vista_profesor .setLayout(paginaProfesor)


        # ----------------------------------------------------
        # PAS
        self.vista_pas = QWidget()
        paginaPAS = QVBoxLayout()
        Ocupaciones = ("Secretario", "Vedel")

        # Selección de PAS
        caixaOcupacionPAS = QHBoxLayout()
        lblOcupacion = QLabel("Ocupación: ")
        self.cmbOcupacion = QComboBox()
        self.cmbOcupacion.addItems(Ocupaciones)
        self.cmbOcupacion.setCurrentIndex(-1)
        caixaOcupacionPAS.addWidget(lblOcupacion)
        caixaOcupacionPAS.addWidget(self.cmbOcupacion)
        paginaPAS.addLayout(caixaOcupacionPAS)

        # Nome PAS
        caixaNomePAS = QHBoxLayout()
        lblNome = QLabel("Nome: ")
        self.txtNomePAS = QtWidgets.QLineEdit()
        caixaNomePAS.addWidget(lblNome)
        caixaNomePAS.addWidget(self.txtNomePAS)
        paginaPAS.addLayout(caixaNomePAS)

        # Apelido PAS
        caixaApelidoPAS = QHBoxLayout()
        lblApelido = QLabel("Apelido: ")
        self.txtApelidoPAS = QtWidgets.QLineEdit()
        caixaApelidoPAS.addWidget(lblApelido)
        caixaApelidoPAS.addWidget(self.txtApelidoPAS)
        paginaPAS.addLayout(caixaApelidoPAS)

        self.vista_pas.setLayout(paginaPAS)


        self.ventanas.addWidget(self.vista_alumno)
        self.ventanas.addWidget(self.vista_profesor)
        self.ventanas.addWidget(self.vista_pas)

        # Mostrar la pantalla vacía por defecto
        self.ventanas.setCurrentIndex(0)
        # Añadir el QStackedLayout al layout principal
        layout_principal.addLayout(self.ventanas)


        # 2. Widget Contenedor Central (OBLIGATORIO en QMainWindow)
        contenedor = QWidget()
        contenedor.setLayout(layout_principal)
        self.setCentralWidget(contenedor)

    #Cambia la pantalla visible al seleccionar una opción
        # Cambia la pantalla visible al seleccionar una opción
    def on_cmbTipo_setCurrentChanged(self, index):
        if index == -1:
            self.ventanas.setCurrentIndex(0)  # Muestra la vista vacía
        else:
            self.ventanas.setCurrentIndex(index + 1)  # Alumno (0) -> Vista Alumno (1)

    #def on_cmbTipo_setCurrentChanged(self, index):
     #   if index >= 0:
      #      self.tarxetas.setCurrentIndex(index)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Matriculacion()
    window.show()
    sys.exit(app.exec())