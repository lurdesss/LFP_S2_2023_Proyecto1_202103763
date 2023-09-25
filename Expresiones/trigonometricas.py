from Expresiones.expresion import *
import math
from Graficas.Arbol import *


class ExpresionTrigonometrica(Expresion):
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def interpretar(self):
        # convertir grados a radianes
        if self.valor is not None:
            if not isinstance(self.valor, (int, float)):
                return "Error: valor no numérico"

            radians = math.radians(self.valor)

            # calcular valor trigonométrico
            resultado = None
            if self.tipo.lower() == "seno":
                resultado = math.sin(radians)
            elif self.tipo.lower() == "coseno":
                resultado = math.cos(radians)
            elif self.tipo.lower() == "tangente":
                # verificar para valores indefinidos (90 y 270 grados)
                if self.valor % 180 == 90:
                    return "Indefinido"
                resultado = math.tan(radians)

            # agregar resultado al arbol
            if resultado is not None:
                raiz = arbol.agregarNodo(
                    f"{self.tipo}\\n{str('{:.2f}'.format(resultado))}")
                return resultado
            else:
                return "Error: tipo de operación no reconocida"
        else:
            return "Error: valor nulo"
