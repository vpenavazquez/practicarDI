import random
import sys

# Importaciones del módulo Core de PyQt6 para manejo de eventos globales y constantes del sistema
from PyQt6.QtCore import QEvent, Qt
# Importaciones del módulo Widgets para la construcción de la interfaz gráfica
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QMainWindow,
    QPushButton,
    QWidget,
)


class FiestraPrincipal(QMainWindow):
    """
    Clase principal que implementa el juego del Buscaminas.
    Hereda de QMainWindow para hacer uso de elementos como la barra de estado (statusBar).
    """

    def __init__(self):
        super().__init__()

        # --- Configuración inicial de las dimensiones y parámetros del juego ---
        self.filas = 8
        self.columnas = 8
        self.numeroMinas = 10
        self.juegoTerminado = False
        self.casillasAbiertas = 0

        # Configuración de la ventana principal
        self.setWindowTitle("Buscaminas")
        self.setFixedSize(400, 430)  # Fija un tamaño de ventana no redimensionable

        # --- Creación del tablero y estructuras de datos ---
        # 1. Matriz de widgets (QPushButton) y su QGridLayout asociado
        self.botons, layout = self.crearBotonsGrid()

        # 2. Matriz lógica de minas: -1 representa una mina; 0-8 representa el número de minas vecinas
        self.campoDeMinas = [
            [0 for _ in range(self.columnas)] for _ in range(self.filas)
        ]
        # 3. Matriz de estado: indica qué casillas se han revelado/abierto
        self.pulsados = [
            [False for _ in range(self.columnas)] for _ in range(self.filas)
        ]
        # 4. Matriz de banderas: indica qué casillas tienen colocada una marca de bandera
        self.bandeiras = [
            [False for _ in range(self.columnas)] for _ in range(self.filas)
        ]

        # Distribución aleatoria inicial de minas y cálculo numérico de vecinas
        self.minarCampo()
        self.contarMinas()

        # Ensamblado del contenedor central requerido en QMainWindow
        contedor = QWidget()
        contedor.setLayout(layout)
        self.setCentralWidget(contedor)

        # Muestra la información inicial de minas restantes en la barra de estado
        self.actualizar_estado()

    def crearBotonsGrid(self):
        """
        Crea la matriz de botones visuales (QPushButton) organizados en una cuadrícula (QGridLayout).
        Retorna la matriz bidimensional de botones y el objeto layout.
        """
        layout = QGridLayout()
        layout.setSpacing(4)  # Espaciado de 4 píxeles entre los botones
        botons = []

        for fila in range(self.filas):
            fila_botons = []
            for columna in range(self.columnas):
                boton = QPushButton()
                boton.setFixedSize(42, 42)

                # Conexión del evento clic izquierdo (Signal -> Slot) usando un lambda para capturar las coordenadas actuales
                boton.clicked.connect(
                    lambda checked=False, f=fila, c=columna: self.abrir_casilla(f, c)
                )

                # Propiedades dinámicas almacenadas en el widget para poder identificarse dentro del filtro de eventos
                boton.setProperty("fila", fila)
                boton.setProperty("columna", columna)

                # Instala un filtro de eventos en cada botón para interceptar el clic derecho (bandera)
                boton.installEventFilter(self)

                fila_botons.append(boton)
                layout.addWidget(boton, fila, columna)
            botons.append(fila_botons)

        return botons, layout

    def eventFilter(self, objeto, evento):
        """
        Filtro de eventos de PyQt6 para capturar el clic con el botón derecho sobre cualquier QPushButton.
        Permite gestionar las banderas sin necesidad de crear una subclase personalizada de QPushButton.
        """
        if (
                evento.type() == QEvent.Type.MouseButtonPress
                and evento.button() == Qt.MouseButton.RightButton
                and isinstance(objeto, QPushButton)
        ):
            # Obtiene las coordenadas previamente guardadas en las propiedades del botón
            fila = objeto.property("fila")
            columna = objeto.property("columna")
            self.alternar_bandera(fila, columna)
            return True  # Indica que el evento fue procesado y cancela su propagación

        # Si no es el evento buscado, delega el evento al comportamiento original por defecto
        return super().eventFilter(objeto, evento)

    def vecinos(self, fila, columna):
        """
        Generador que produce las coordenadas (f, c) de las casillas adyacentes a una dada.
        Controla los límites del tablero usando max() y min().
        """
        for f in range(max(0, fila - 1), min(self.filas, fila + 2)):
            for c in range(max(0, columna - 1), min(self.columnas, columna + 2)):
                if (f, c) != (fila, columna):
                    yield f, c

    def minarCampo(self):
        """
        Selecciona posiciones aleatorias en el tablero y las establece como minas (-1).
        """
        posiciones = random.sample(
            range(self.filas * self.columnas), self.numeroMinas
        )
        for posicion in posiciones:
            fila, columna = divmod(posicion, self.columnas)
            self.campoDeMinas[fila][columna] = -1

    def contarMinas(self):
        """
        Calcula para cada casilla que no contenga una mina el número total de minas adyacentes.
        """
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.campoDeMinas[fila][columna] != -1:
                    self.campoDeMinas[fila][columna] = sum(
                        self.campoDeMinas[f][c] == -1
                        for f, c in self.vecinos(fila, columna)
                    )

    def preparar_primer_clic(self, fila, columna):
        """
        Garantiza que el primer clic del jugador nunca sea una mina.
        Si la casilla seleccionada o sus vecinas son minas, las relocaliza a casillas libres fuera de esa zona.
        """
        # Define un conjunto de casillas seguras (la casilla pulsada + sus 8 adyacentes)
        zona_segura = {
            (f, c)
            for f in range(max(0, fila - 1), min(self.filas, fila + 2))
            for c in range(max(0, columna - 1), min(self.columnas, columna + 2))
        }

        # Identifica minas existentes que hayan caído dentro de la zona segura
        minas_en_zona = [
            (f, c)
            for f, c in zona_segura
            if self.campoDeMinas[f][c] == -1
        ]

        # Lista casillas disponibles fuera de la zona segura para reubicar las minas
        destinos = [
            (f, c)
            for f in range(self.filas)
            for c in range(self.columnas)
            if (f, c) not in zona_segura and self.campoDeMinas[f][c] != -1
        ]
        random.shuffle(destinos)

        # Mueve cada mina de la zona segura hacia un nuevo destino
        for (f_mina, c_mina), (f_destino, c_destino) in zip(
                minas_en_zona, destinos
        ):
            self.campoDeMinas[f_mina][c_mina] = 0
            self.campoDeMinas[f_destino][c_destino] = -1

        # Re-calcula la cantidad de minas vecinas tras la reubicación
        self.contarMinas()

    def abrir_casilla(self, fila, columna):
        """
        Manejador principal invocado al hacer clic izquierdo en un botón del tablero.
        """
        # Ignora la acción si el juego terminó, o si la casilla ya está abierta o tiene bandera
        if (
                self.juegoTerminado
                or self.pulsados[fila][columna]
                or self.bandeiras[fila][columna]
        ):
            return

        # Si es la primera casilla que se abre, asegura que la zona sea 100% segura
        if self.casillasAbiertas == 0:
            self.preparar_primer_clic(fila, columna)

        # Derrota: si la casilla abierta es una mina (-1)
        if self.campoDeMinas[fila][columna] == -1:
            self.finalizar_partida(ganada=False)
            return

        # Expansión recursiva / iterativa de la zona libre
        self.abrir_zona_segura(fila, columna)

        # Victoria: si las casillas abiertas equivalen al área total menos las minas
        if self.casillasAbiertas == self.filas * self.columnas - self.numeroMinas:
            self.finalizar_partida(ganada=True)
        else:
            self.actualizar_estado()

    def abrir_zona_segura(self, fila, columna):
        """
        Algoritmo de expansión (Flood Fill) mediante una pila iterativa.
        Abre casillas adyacentes automáticamente cuando se pulsa sobre una casilla sin minas vecinas (0).
        """
        pendientes = [(fila, columna)]
        while pendientes:
            f, c = pendientes.pop()

            # Condición de parada para esta iteración
            if (
                    self.pulsados[f][c]
                    or self.bandeiras[f][c]
                    or self.campoDeMinas[f][c] == -1
            ):
                continue

            self.pulsados[f][c] = True
            self.casillasAbiertas += 1
            self.actualizar_aspecto_boton(f, c)

            # Si la casilla no tiene minas adyacentes (0), se añaden sus vecinas a la pila de exploración
            if self.campoDeMinas[f][c] == 0:
                pendientes.extend(self.vecinos(f, c))

    def alternar_bandera(self, fila, columna):
        """
        Coloca o quita una bandera en la posición especificada al pulsar botón derecho.
        """
        if self.juegoTerminado or self.pulsados[fila][columna]:
            return

        # Alterna el estado booleano de la bandera
        self.bandeiras[fila][columna] = not self.bandeiras[fila][columna]
        self.actualizar_aspecto_boton(fila, columna)
        self.actualizar_estado()

    def actualizar_aspecto_boton(self, fila, columna):
        """
        Actualiza el texto, color y estilo (QSS / CSS) del QPushButton según el estado lógico de la casilla.
        """
        boton = self.botons[fila][columna]
        valor = self.campoDeMinas[fila][columna]

        # Estado 1: Casilla marcada con bandera
        if self.bandeiras[fila][columna]:
            boton.setText("P")
            boton.setStyleSheet("background-color: white; color: red;")

        # Estado 2: Casilla sin revelar
        elif not self.pulsados[fila][columna]:
            boton.setText("")
            boton.setStyleSheet("background-color: white;")

        # Estado 3: Casilla pulsada que contenía una mina
        elif valor == -1:
            boton.setText("*")
            boton.setStyleSheet("background-color: black; color: white;")

        # Estado 4: Casilla pulsada vacía (0 minas alrededor)
        elif valor == 0:
            boton.setText("")
            boton.setStyleSheet("background-color: lightgrey;")

        # Estado 5: Casilla pulsada con número de minas adyacentes
        else:
            colores = {
                1: "lightgreen",
                2: "lightyellow",
                3: "orange",
                4: "salmon",
                5: "tomato",
                6: "red",
                7: "red",
                8: "red",
            }
            boton.setText(str(valor))
            boton.setStyleSheet(
                f"background-color: {colores[valor]}; color: black;"
            )

    def finalizar_partida(self, ganada):
        """
        Maneja la lógica de fin del juego (victoria o derrota). Revela la posición de todas las minas.
        """
        self.juegoTerminado = True

        # Revela/actualiza la apariencia de todas las minas del tablero
        for fila in range(self.filas):
            for columna in range(self.columnas):
                if self.campoDeMinas[fila][columna] == -1:
                    if ganada:
                        self.bandeiras[fila][columna] = True
                    else:
                        self.pulsados[fila][columna] = True
                        self.bandeiras[fila][columna] = False
                    self.actualizar_aspecto_boton(fila, columna)

        # Muestra el mensaje final en la barra de estado de la ventana (statusBar)
        if ganada:
            mensaje = "¡Ganaste! Has encontrado todas las casillas seguras."
        else:
            mensaje = "¡Has perdido! Has encontrado una mina."
        self.statusBar().showMessage(mensaje)

    def actualizar_estado(self):
        """
        Calcula y muestra la cantidad estimada de minas restantes (Minas totales - Banderas colocadas)
        en la barra de estado inferior.
        """
        banderas = sum(sum(fila) for fila in self.bandeiras)
        self.statusBar().showMessage(
            f"Minas restantes: {self.numeroMinas - banderas}"
        )


# --- Bloque de arranque de la aplicación ---
if __name__ == "__main__":
    aplicacion = QApplication(sys.argv)
    fiestra = FiestraPrincipal()
    fiestra.show()
    sys.exit(aplicacion.exec())