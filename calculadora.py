import ast
import math
import tkinter as tk

# --- Constantes de configuración visual y seguridad ---
BACKGROUND = "#1C1C1E"  # Color de fondo de la ventana principal (gris oscuro)
DISPLAY_BACKGROUND = "#2C2C2E"  # Color de fondo para la caja de entrada de expresión
BUTTON_BACKGROUND = "#3A3A3C"  # Color estándar para los botones numéricos/operadores
ORANGE = "#FF9500"  # Color destacado para el botón de igual (=)
MAX_EXPRESSION_LENGTH = 200  # Límite de caracteres para evitar bloqueos por expresiones gigantes


def safe_evaluate(expression):
    """
    Evalúa una expresión matemática en formato de texto de forma segura utilizando
    el Árbol de Sintaxis Abstracta (AST) de Python en lugar de la función 'eval()',
    evitando vulnerabilidades de ejecución de código arbitrario.
    """
    # Validación inicial de longitud
    if len(expression) > MAX_EXPRESSION_LENGTH:
        raise ValueError("Expression is too long")

    # Parsea la cadena de texto a un árbol de sintaxis abstracta (AST) en modo evaluación
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):
        """Función recursiva para recorrer y evaluar los nodos del árbol AST permitidos."""
        # Nodo raíz de expresión
        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        # Nodos constantes (números enteros o flotantes)
        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Only numeric values are allowed")
            return node.value

        # Operaciones binarias (ej: suma, resta, multiplicación, división, potencia cuadrada)
        if isinstance(node, ast.BinOp):
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow) and right == 2:
                return left ** 2
            raise ValueError("Unsupported operation")

        # Operaciones unarias (ej: números positivos o negativos +x, -x)
        if isinstance(node, ast.UnaryOp):
            value = evaluate(node.operand)
            if isinstance(node.op, ast.UAdd):
                return value
            if isinstance(node.op, ast.USub):
                return -value
            raise ValueError("Unsupported operation")

        # Llamadas a funciones matemáticas explícitamente permitidas (ej: sqrt(x))
        if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "sqrt"
                and len(node.args) == 1
                and not node.keywords
        ):
            return math.sqrt(evaluate(node.args[0]))

        # Cualquier otro tipo de nodo (ej: importaciones, variables, otras funciones) queda bloqueado
        raise ValueError("Invalid expression")

    # Ejecuta el recorrido del árbol
    result = evaluate(tree)

    # Comprueba que el resultado no sea Infinito o NaN (Not a Number)
    if isinstance(result, float) and not math.isfinite(result):
        raise OverflowError("Result is not finite")
    return result


class Calculator:
    """
    Clase que gestiona la interfaz gráfica de usuario (GUI) con Tkinter
    y la lógica de la calculadora.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        self.root.configure(bg=BACKGROUND)
        self.root.minsize(320, 420)

        # Variables de control de Tkinter para actualizar texto dinámicamente
        self.expression = tk.StringVar()  # Muestra la expresión introducida
        self.result = tk.StringVar(value="0")  # Muestra el resultado de la operación
        self.just_calculated = False  # Bandera para saber si se acaba de presionar '='

        # --- Componente 1: Pantalla de entrada/expresión ---
        display = tk.Entry(
            root,
            textvariable=self.expression,
            state="readonly",  # Campo en modo solo lectura para evitar edición directa con cursor
            readonlybackground=DISPLAY_BACKGROUND,
            disabledforeground="#FFFFFF",
            foreground="#FFFFFF",
            insertbackground="#FFFFFF",
            font=("Arial", 20),
            justify="right",
            relief="flat",
            bd=0,
        )
        display.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=12, pady=(14, 4), ipady=12)

        # --- Componente 2: Pantalla de resultado ---
        result_label = tk.Label(
            root,
            textvariable=self.result,
            bg=BACKGROUND,
            fg="#FFFFFF",
            font=("Arial", 30),
            anchor="e",
            padx=12,
        )
        result_label.grid(row=1, column=0, columnspan=6, sticky="nsew", pady=(0, 12))

        # --- Definición y posicionamiento de botones (Texto, Fila, Columna, [ColumnSpan opcional]) ---
        buttons = [
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("/", 2, 3), ("(", 2, 4), (")", 2, 5),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("*", 3, 3), ("√x", 3, 4), ("x²", 3, 5),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("-", 4, 3), ("C", 4, 4), ("⌫", 4, 5),
            ("0", 5, 0, 2), (".", 5, 2), ("+", 5, 3), ("=", 5, 4, 2),
        ]

        # Bucle para crear dinámicamente cada botón según la configuración anterior
        for item in buttons:
            label, row, column, *span = item
            columnspan = span[0] if span else 1

            # Asignación de color según el tipo de botón
            color = ORANGE if label == "=" else "#32CD32" if label == "0" else BUTTON_BACKGROUND

            button = tk.Button(
                root,
                text=label,
                command=lambda value=label: self.press(value),  # Callback genérico que envía la etiqueta del botón
                bg=color,
                fg="#FFFFFF",
                activebackground=(
                    "#CC7A00" if label == "=" else "#228B22" if label == "0" else "#545456"
                ),
                activeforeground="#FFFFFF",
                relief="flat",
                bd=0,
                font=("Arial", 18, "bold"),
                takefocus=False,  # Evita que los botones capturen el foco del teclado
            )
            button.grid(
                row=row,
                column=column,
                columnspan=columnspan,
                sticky="nsew",
                padx=5,
                pady=5,
                ipadx=4,
                ipady=10,
            )

        # --- Configuración de adaptabilidad (Responsive design) para la cuadrícula ---
        for row in range(2, 6):
            root.rowconfigure(row, weight=1, minsize=52)
        for column in range(6):
            root.columnconfigure(column, weight=1, minsize=42)
        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=0)

        # Captura de eventos del teclado físico
        root.bind_all("<Key>", self.handle_key)

    def press(self, key):
        """Manejador central para la interacción con los botones gráficos."""
        if key == "C":
            self.clear()
        elif key == "⌫":
            self.backspace()
        elif key == "=":
            self.calculate()
        elif key == "√x":
            self.append("sqrt(")
        elif key == "x²":
            self.append("**2")
        else:
            self.append(key)

    def append(self, text):
        """Añade texto o caracteres a la expresión actual gestionando el reinicio tras un cálculo."""
        current = self.expression.get()
        if self.just_calculated:
            # Si se presiona un número u operador inicial justo después de calcular, reinicia la expresión
            if text in "0123456789.(" or text == "sqrt(":
                current = ""
            elif self.result.get() != "Error":
                current = self.result.get()
            self.just_calculated = False

        self.expression.set(current + text)
        self.result.set("0")

    def clear(self):
        """Limpia las pantallas y reinicia el estado."""
        self.expression.set("")
        self.result.set("0")
        self.just_calculated = False

    def backspace(self):
        """Elimina el último carácter introducido."""
        self.expression.set(self.expression.get()[:-1])
        self.result.set("0")
        self.just_calculated = False

    def calculate(self):
        """Dispara la evaluación segura de la expresión actual y muestra el resultado o error."""
        expression = self.expression.get()
        if not expression:
            return
        try:
            value = safe_evaluate(expression)
            # Formatea la precisión de los números flotantes a 12 dígitos significativos
            if isinstance(value, float):
                displayed = format(value, ".12g")
            else:
                displayed = str(value)
            self.result.set(displayed)
        except (ArithmeticError, SyntaxError, ValueError, TypeError):
            self.result.set("Error")
        self.just_calculated = True

    def handle_key(self, event):
        """Intercepta pulsaciones del teclado físico y las mapea hacia las funciones correspondientes."""
        if event.keysym in ("Return", "KP_Enter"):
            self.calculate()
            return "break"
        if event.keysym == "BackSpace":
            self.backspace()
            return "break"
        if event.keysym == "Escape":
            self.clear()
            return "break"
        if event.char and event.char in "0123456789.+-*/()":
            self.append(event.char)
            return "break"
        return None


def main():
    """Función de entrada para instanciar e iniciar la aplicación Tkinter."""
    root = tk.Tk()
    Calculator(root)
    root.mainloop()


# Bloque de ejecución principal del script
if __name__ == "__main__":
    main()