from globalTypes import *
from lexer import *
from parser import *
from semantica import check_semantics
from cgen import *

# Abrir y leer el archivo a compilar
f = open('sample.txt', 'r')
programa = f.read()  # Lee todo el archivo
progLong = len(programa)  # Longitud original del programa
programa = programa + '$'  # Agregar un caracter $ que representa EOF
posicion = 0  # Posición del caracter actual del string

# Llamar a la función para inicializar las variables globales
globales(programa, posicion, progLong)

# Llamamos a la función parse() 
root, symbol_table = parse()
#AST
root.print_ast()
#semantica
check_semantics(root, symbol_table)
codeGen(root, 'output.asm')