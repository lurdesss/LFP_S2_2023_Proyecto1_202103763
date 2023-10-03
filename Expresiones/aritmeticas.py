from Expresiones.expresion import *
from Graficas.Arbol import *
import math


class ExpresionAritmetica(Expresion):
    def __init__(self, tipo, valor1, valor2, linea, columna):
        self.tipo = tipo
        self.valor1 = valor1
        self.valor2 = valor2
        self.linea = linea
        self.columna = columna

    def interpretar(self):
        global arbol

        valor1 = self.valor1
        valor2 = self.valor2

        # nombre de las etiquetas
        nodo1 = None
        nodo2 = None

        # validar si es un numero o una expresion
        if isinstance(self.valor1, Expresion):
            valor1 = self.valor1.interpretar()
            nodo1 = arbol.obtenerUltimoNodo()
        else:
            valor1 = self.valor1
            nodo1 = arbol.agregarNodo(str(valor1))
        if isinstance(self.valor2, Expresion):
            valor2 = self.valor2.interpretar()
            nodo2 = arbol.obtenerUltimoNodo()
        else:
            valor2 = self.valor2
            nodo2 = arbol.agregarNodo(str(valor2))

        resultado = None
        if self.tipo == "suma":
            resultado = valor1 + valor2
        elif self.tipo == "resta":
            resultado = valor1 - valor2
        elif self.tipo == "multiplicacion":
            resultado = valor1 * valor2
        elif self.tipo == "potencia":
            resultado = math.pow(valor1, valor2)
        elif self.tipo == "raiz":
            try:
                resultado = math.pow(valor1, 1 / valor2)
            except ZeroDivisionError:
                resultado = "Error: División por cero en valor 2 de .pow"
                print(resultado)
        elif self.tipo == "division":
            try:
                resultado = valor1/valor2
            except ZeroDivisionError:
                resultado = "Error: division por cero"
                print(resultado)
        elif self.tipo == "inverso":
            try:
                resultado = 1 / valor1
            except ZeroDivisionError:
                resultado = "Error: División por cero en inverso"
                print(resultado)
        elif self.tipo == "mod":
            try:
                resultado = valor1 % valor2
            except ZeroDivisionError:
                resultado = "Error: División por cero en mod"
                print(resultado)
                resultado = math.pow(valor1, 1)

        # GRAFICAR
        if arbol == None:
            print("arbol es None")
        raiz = arbol.agregarNodo(
            f"{self.tipo}\\n{str('{:.2f}'.format(resultado))}")
        arbol.agregarArista(raiz, nodo1)
        if self.valor2 != None:
            arbol.agregarArista(raiz, nodo2)

        return round(resultado, 2)
