import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class JuegoPiedraPapelTijera(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Piedra, Papel o Tijera - PyQt6")
        self.resize(400, 350)

        # 1. Variables de estado interno (Marcador)
        self.puntos_usuario = 0
        self.puntos_maquina = 0
        self.opciones = ["Piedra", "Papel", "Tijera"]

        # 2. Layout principal
        contenedor = QWidget()
        self.setCentralWidget(contenedor)
        layout_principal = QVBoxLayout(contenedor)

        # 3. Encabezado / Marcador Visual
        self.lbl_marcador = QLabel("Usuario: 0  |  Máquina: 0")
        self.lbl_marcador.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_marcador = QFont("Arial", 14)
        font_marcador.setWeight(QFont.Weight.Bold)
        self.lbl_marcador.setFont(font_marcador)
        layout_principal.addWidget(self.lbl_marcador)

        # Línea separadora decorativa (Sintaxis PyQt6)
        linea = QFrame()
        linea.setFrameShape(QFrame.Shape.HLine)
        linea.setFrameShadow(QFrame.Shadow.Sunken)
        layout_principal.addWidget(linea)

        # 4. Información de la ronda (Elecciones y Resultado)
        self.lbl_usuario = QLabel("Tu elección: -")
        self.lbl_maquina = QLabel("Elección máquina: -")
        self.lbl_resultado = QLabel("¡Elige una opción para empezar!")

        self.lbl_usuario.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_maquina.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)

        font_resultado = QFont("Arial", 12)
        font_resultado.setWeight(QFont.Weight.Bold)
        self.lbl_resultado.setFont(font_resultado)

        layout_principal.addWidget(self.lbl_usuario)
        layout_principal.addWidget(self.lbl_maquina)
        layout_principal.addSpacing(10)
        layout_principal.addWidget(self.lbl_resultado)
        layout_principal.addSpacing(15)

        # 5. Botones de Selección (Layout Horizontal)
        lay_botones = QHBoxLayout()
        self.btn_piedra = QPushButton("🪨 Piedra")
        self.btn_papel = QPushButton("📄 Papel")
        self.btn_tijera = QPushButton("✂️ Tijera")

        lay_botones.addWidget(self.btn_piedra)
        lay_botones.addWidget(self.btn_papel)
        lay_botones.addWidget(self.btn_tijera)
        layout_principal.addLayout(lay_botones)

        # 6. Botón de Reiniciar
        layout_principal.addSpacing(10)
        self.btn_reiniciar = QPushButton("Reiniciar Marcador")
        layout_principal.addWidget(self.btn_reiniciar)

        # CONEXIÓN DE SEÑALES Y SLOTS
        self.btn_piedra.clicked.connect(lambda: self.jugar("Piedra"))
        self.btn_papel.clicked.connect(lambda: self.jugar("Papel"))
        self.btn_tijera.clicked.connect(lambda: self.jugar("Tijera"))
        self.btn_reiniciar.clicked.connect(self.reiniciar_juego)

    def jugar(self, eleccion_usuario):
        # Selección aleatoria de la máquina
        eleccion_maquina = random.choice(self.opciones)

        # Actualizar etiquetas de elecciones
        self.lbl_usuario.setText(f"Tu elección: {eleccion_usuario}")
        self.lbl_maquina.setText(f"Elección máquina: {eleccion_maquina}")

        # Lógica de juego para determinar el ganador
        if eleccion_usuario == eleccion_maquina:
            resultado = "¡Empate! 🤝"
        elif (eleccion_usuario == "Piedra" and eleccion_maquina == "Tijera") or \
                (eleccion_usuario == "Papel" and eleccion_maquina == "Piedra") or \
                (eleccion_usuario == "Tijera" and eleccion_maquina == "Papel"):
            resultado = "¡Has ganado la ronda! 🎉"
            self.puntos_usuario += 1
        else:
            resultado = "¡Gana la máquina! 🤖"
            self.puntos_maquina += 1

        # Actualizar resultado y marcador visual
        self.lbl_resultado.setText(resultado)
        self.actualizar_marcador()

    def actualizar_marcador(self):
        self.lbl_marcador.setText(f"Usuario: {self.puntos_usuario}  |  Máquina: {self.puntos_maquina}")

    def reiniciar_juego(self):
        self.puntos_usuario = 0
        self.puntos_maquina = 0
        self.actualizar_marcador()
        self.lbl_usuario.setText("Tu elección: -")
        self.lbl_maquina.setText("Elección máquina: -")
        self.lbl_resultado.setText("¡Marcador reiniciado! Elige una opción.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    v = JuegoPiedraPapelTijera()
    v.show()
    sys.exit(app.exec())


"""
===============================================================================
EJEMPLO: JUEGO PIEDRA, PAPEL O TIJERA (ADAPTADO A PYQT6)
===============================================================================

ENUNCIADO:
----------
Crear una aplicación gráfica interactiva para jugar a "Piedra, Papel o Tijera" 
contra la máquina utilizando PyQt6.
Requisitos visuales y de lógica:
1. La interfaz dispondrá de 3 botones principales (`QPushButton`) para que el 
   usuario elija su jugada: "🪨 Piedra", "📄 Papel" o "✂️ Tijera".
2. La máquina generará una elección aleatoria utilizando la librería `random`.
3. Mantener una estructura de datos interna (variables Python) para el marcador:
   `self.puntos_usuario` y `self.puntos_maquina`.
4. Mostrar en etiquetas (`QLabel`) la elección del usuario, la elección de la 
   máquina, la resolución de la ronda ("¡Ganaste!", "¡Empate!", "¡Perdiste!") y 
   el marcador actualizado en tiempo real.
5. Incluir un botón "Reiniciar Marcador" que restablezca los puntos a 0.

CAMBIOS CLAVE EN PYQT6:
-----------------------
- En PyQt6, las propiedades de la interfaz usan namespaces completos:
  * `Qt.AlignmentFlag.AlignCenter` (en lugar de `Qt.AlignCenter`).
  * `QFrame.Shape.HLine` y `QFrame.Shadow.Sunken`.
  * `QFont.Weight.Bold` para establecer el peso de las fuentes.
  * El bucle principal se ejecuta con `app.exec()` (en lugar de `app.exec_()`).
===============================================================================
"""