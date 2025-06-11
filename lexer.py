from globalTypes import *
import sys

# Variables globales
programa = ''
posicion = 0
progLong = 0
estado= 0
p= 0 #posicion inicial en el tring
l='qwertyuiopñlkjhgfdsazxcvbnmQWERTYUIOPÑLKJHGFDSAZXCVBNM'
n='0123456789'
b=' \t\n$'
linea=1
lastc=""
c=""
# Función para pasar los valores iniciales de las variables globales
def globales(prog, pos, long):
    global programa
    global posicion
    global progLong
    global linea
    programa = prog
    posicion = pos
    progLong = long

# Función que obtiene el siguiente token
def getToken(imprime=True):
    lexema=''
    global programa, posicion, progLong, linea,lastc,c
    lastc=c
    c=""
    while (programa[posicion] != '$' ):
        lexema=''
        c= programa[posicion]
        # Evaluamos el carácter y asignamos el token correspondiente
        if c in l:  # Si es una letra menor o mayuscula, es un identificador (ID)
            col = TokenType.ID
            while programa[posicion] in l:
                lexema += programa[posicion]
                posicion +=1 
            c=lexema
            if programa[posicion] in n:
                col = TokenType.ERROR
                colerror=TokenType.ID
                cerror=programa[posicion]
                posicion +=1            
            elif c=='if':
               col = TokenType.IF
            elif c=='else':
               col = TokenType.ELSE
            elif c=='int':
               col = TokenType.INT
            elif c=='return':
               col = TokenType.RETURN
            elif c=='void':
               col = TokenType.VOID
            elif c=='while':
               col = TokenType.WHILE
            posicion -=1
            
        elif c in n:  # Si es un número, es un número (NUM)
            col = TokenType.NUM
            while programa[posicion] in n:
                lexema += programa[posicion]
                posicion +=1
            if programa[posicion] in l:
                col = TokenType.ERROR
                colerror=TokenType.ID
                cerror=programa[posicion]
                posicion +=1 
            posicion -=1 
            c=lexema
            
        elif c == '+':  # Si es un '+', es el operador de suma
            col = TokenType.PLUS
            
        elif c == '-':  # Si es un '-', es el operador de resta
            col = TokenType.MINUS
            
        elif c == '*' and programa[posicion - 1] != '/':  # Si es un '*', es el operador de multiplicación
            col = TokenType.TIMES
            
        elif c == '/' and programa[posicion + 1] != '*':  # Si es un '/', es el operador de división
            col = TokenType.DIVIDE
            
        elif c == '<':  # Si es un '<', es el operador menor que
            col = TokenType.LT
            if programa[posicion + 1] == '=':  # Si es un '<=', es el operador de menor o igual que
                col = TokenType.LTEQ
                lexema += programa[posicion]
                posicion +=1
                lexema += programa[posicion]
                c=lexema
            
        elif c == '>':  # Si es un '>', es el operador menor que
            col = TokenType.GT
            if programa[posicion + 1] == '=':  # Si es un '>=', es el operador menor o igual que
                col = TokenType.GTEQ
                lexema += programa[posicion]
                posicion +=1
                lexema += programa[posicion]
                c=lexema
            
        elif c == '=':  # Si es un '=', es una asignación
            col = TokenType.ASSIGN
            if programa[posicion + 1] == '=':  # Si es un '==', es el operador exactamente igual que
                col = TokenType.EQ
                lexema += programa[posicion]
                posicion +=1
                lexema += programa[posicion]
                c=lexema
            
        elif c == '!' and programa[posicion + 1] == '=':  # Si es un '==', es el operador  diferente a
            col = TokenType.NEQ
            lexema += programa[posicion]
            posicion +=1
            lexema += programa[posicion]
            c=lexema
            
        elif c == ';':  # Si es un ';', es un punto y coma
            col = TokenType.SEMI
            
        elif c == ',':  # Si es una coma, es un delimitador
            col = TokenType.COMMA
            
        elif c == '(':  # Si es un '(', es un paréntesis izquierdo
            col = TokenType.LPAREN
            
        elif c == ')':  # Si es un ')', es un paréntesis derecho
            col = TokenType.RPAREN
            
        elif c == '{':  # Si es un '{', es una llave izquierda
            col = TokenType.LBRACE
            
        elif c == '}':  # Si es un '}', es una llave derecha
            col = TokenType.RBRACE
            
        elif c == '[':  # Si es un '[', es una corteche izquierdo
            col = TokenType.LBRACKET
            
        elif c == ']':  # Si es un ']', es un corchete derecha
            col = TokenType.RBRACKET     
               
        elif c == '/' and programa[posicion + 1] == '*': # Si es un '/*', es un inicio de comentario
            col = TokenType.COMMENT
            lexema = '/*'
            posicion += 2 
            while posicion < progLong and (programa[posicion] != '*' or programa[posicion + 1] != '/'):  # Mientras no sea el final del comentario
                lexema += programa[posicion]  # Agregar el contenido al comentario
                posicion += 1  
            lexema += '*/'  
            posicion += 2
            c=lexema
            
        elif c == ' ' or c == '\t':  # Si es espacio o tabulación
            # Verificar si el siguiente carácter es espacio, tabulación o salto de línea
            if (programa[posicion + 1] == ' ' or programa[posicion + 1] == '\t' or programa[posicion + 1] == '\n') or (programa[posicion - 1] == ' ' or programa[posicion - 1] == '\t' or programa[posicion - 1] == '\n'):
                col = TokenType.ENDLINE
            else:
                col = TokenType.SPACE
            
        elif c =='\n':  # Si es un salto de linea lo ignoramos
            linea+=1
            col = TokenType.ENDLINE
            
        else:  # Si el carácter no coincide con ninguno de los anteriores, es un error
            col = TokenType.ERROR
        
        # Muestra el token que se ha identificado
        if col==TokenType.ENDLINE:
            # Ignora el token
            pass
        elif col==TokenType.ERROR:
            # Impresión del error
            print('\n')
            print(f"Linea {linea}: Error en la formación de: {colerror.name}:")
            print(f"{c}={c}+{cerror}")
            espacioerror=" " * (1 + len(c) * 2)
            print(f"{espacioerror}^^")
            print('\n')
        else:
            # Impresión del token
            if imprime==True:
                #print(f"Token: {col.name}, Carácter: {c}")
                pass
            if not imprime:
             pass
        # Avanzamos a la siguiente posición
        posicion += 1
        if col == TokenType.SPACE or col==TokenType.ENDLINE or col==TokenType.ERROR:
            pass
        else:
            return col, c, linea

    return TokenType.ENDFILE, "$",linea


def peekToken():
    global programa, posicion, progLong, linea
    saved_pos = posicion
    saved_linea = linea
    token_peek, tokenString_peek,linea_peek = getToken(imprime=False)
    posicion = saved_pos
    linea = saved_linea
    return token_peek, tokenString_peek, linea_peek

def lookahead_is(expected_token):
    token_peek, _, _= peekToken()
    return token_peek == expected_token
