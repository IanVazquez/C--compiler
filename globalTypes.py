from enum import Enum

class TokenType(Enum):
    # Palabras reservadas
    IF = 1
    ELSE = 2
    INT = 3
    RETURN = 4
    VOID = 5
    WHILE = 6

    # Identificadores y números
    ID = 7
    NUM = 8
    # Operadores y símbolos especiales
    PLUS = 9           # +
    MINUS = 10          # -
    TIMES = 11          # *
    DIVIDE = 12         # /
    LT = 13             # <
    LTEQ = 14           # <=            
    GT = 15             # >
    GTEQ = 16           # >=           
    EQ = 17             # ==             
    NEQ = 18            # !=             
    ASSIGN = 19         # =
    SEMI = 20           # ;
    COMMA = 21          # ,
    LPAREN = 22         # (
    RPAREN = 23         # )
    LBRACKET = 24       # [            
    RBRACKET = 25       # ]            
    LBRACE = 26         # {
    RBRACE = 27         # }

    # Comentarios
    COMMENT = 28        # /* comentario */
    #Espacios
    SPACE=29
    ENDLINE =30
    # Fin de archivo y errores
    ENDFILE = 31
    ERROR = 32

class VarType(Enum):
    INT = 1
    VOID = 2

class VarKind(Enum):
    GLOBAL_VAR = 1
    LOCAL_VAR = 2
    PARAM = 3
    FUNCTION = 4