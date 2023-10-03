from collections import namedtuple
from Expresiones import *
from Expresiones.aritmeticas import ExpresionAritmetica
from Expresiones.trigonometricas import ExpresionTrigonometrica
from Graficas.Arbol import *

Token = namedtuple("Token", ["valor", "linea", "columna"])
Error = namedtuple("Error", ["valor", "linea", "columna"])

# numero de linea
linea = 1
# numero de columna
columna = 1
errores = []
tokens = []


configuracion = {
    "texto": None,
    "fondo": None,
    "fuente": None,
    "forma": None,
}


# formar un string
def tokenize_string(input_str, i):
    token = ""
    for char in input_str:
        if char == '"':
            return [token, i]
        token += char
        i += 1
    # errores.append(token)
    print("Error: string no cerrado")


# formar un numero
def tokenize_number(input_str, i):
    token = ""
    isDecimal = False
    for char in input_str:
        if char.isdigit():
            token += char
            i += 1
        elif char == "." and not isDecimal:
            token += char
            i += 1
            isDecimal = True
        else:
            break
    if isDecimal:
        return [float(token), i]
    return [int(token), i]


# formar los tokens
def tokenize_input(input_str):
    # referenciar las variables globales
    global linea, columna, tokens, errores
    # iterar sobre cada caracter del input
    i = 0
    # mientras no se llegue al final del input
    while i < len(input_str):
        # obtener el caracter actual
        char = input_str[i]
        if char.isspace():
            # si es un salto de linea
            if char == "\n":
                # print({"char": char, "linea": linea, "columna": columna, "i": i})
                # tokens.append("EOL")
                linea += 1
                columna = 1
            # si es un tabulador
            elif char == "\t":
                columna += 4
            # si es un espacio
            else:
                columna += 1
            # incrementar el indice
            i += 1
        # si es un string formar el token
        elif char == '"':
            string, pos = tokenize_string(input_str[i + 1:], i)
            columna += len(string) + 1
            i = pos + 2
            token = Token(string, linea, columna)
            tokens.append(token)
        elif char in ["{", "}", "[", "]", ",", ":"]:
            columna += 1
            i += 1
            token = Token(char, linea, columna)
            tokens.append(token)
        elif char.isdigit():
            number, pos = tokenize_number(input_str[i:], i)
            columna += pos - i
            i = pos
            token = Token(number, linea, columna)
            tokens.append(token)
        elif char == "-":
            number, pos = tokenize_number(input_str[i+1:], i+1)
            numero = number - number
            number = numero - number
            columna += pos - (i+1)
            i = pos
            token = Token(number, linea, columna)
            tokens.append(token)
        else:
            i += 1
            columna += 1
            token = Error(char, linea, columna)
            errores.append(token)


# crear las instrucciones a partir de los tokens
def get_instruccion():
    global tokens
    operacion = None
    valor1 = None
    valor2 = None
    while tokens:
        token = tokens.pop(0)
        # print("\033[1;32;40m Token reconocido:", token, "\033[0m")
        if token.valor == "operacion":
            # eliminar el :
            tokens.pop(0)
            operacion = tokens.pop(0).valor
        elif token.valor == "valor1":
            # eliminar el :
            tokens.pop(0)
            valor1 = tokens.pop(0).valor
            if valor1 == "[":
                valor1 = get_instruccion()
        elif token.valor == "valor2":
            # eliminar el :
            tokens.pop(0)
            valor2 = tokens.pop(0).valor
            if valor2 == "[":
                valor2 = get_instruccion()
        elif token.valor in ["texto", "fondo", "fuente", "forma"]:
            tokens.pop(0)
            configuracion[token.valor] = tokens.pop(0).valor

        if operacion and valor1 and valor2:
            return ExpresionAritmetica(operacion, valor1, valor2, 0, 0)
        if operacion and operacion in ["seno", "coseno", "tangente"] and valor1:
            return ExpresionTrigonometrica(operacion, valor1, 0, 0)
    return None


# entrada = open("ejemplo_entrada.json", "r").read()


def create_instructions():
    global tokens
    global arbol
    instrucciones = []
    while tokens:
        instruccion = get_instruccion()
        if instruccion:
            instrucciones.append(instruccion)
    arbol.agregarConfiguracion(configuracion)
    return instrucciones


def genera_reporte(entrada):
    arbol.dot.clear()
    arbol.agregarConfiguracion(configuracion)
    instrucciones = create_instructions()
    for i in instrucciones:
        i.interpretar()

    return arbol


def analizar(entrada):
    global tokens
    tokenize_input(entrada)
    tkn = str(tokens)
    return tkn


def errores_en(entrada):
    err = str(errores)
    return err


# class Error():
#     def __init__(self, lexema, columna, fila):
#         self.lexema = lexema
#         self.columna = columna
#         self.fila = fila

#     def __str__(self):
#         return f'Lexema: {self.lexema}, fila: {self.fila}, columna: {self.columna}'
