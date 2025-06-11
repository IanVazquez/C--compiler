from lexer import *
from globalTypes import *
from symboltable import *
from cgen import *

# Inicializar variables globales
token = None
tokenString = None
linea=1
posfun=""

def advance():
    global token, tokenString, linea
    # Llamamos a getToken para obtener el siguiente token
    token, tokenString,linea = getToken(True)
    
# Función para manejar errores
def error(msg):
    if tokenString=="$":
        print(f"Error de sintaxis. Línea {linea}: {msg} antes de terminar el programa")
        print("Endfile")
    else:
        print(f"Error de sintaxis. Línea {linea}: {msg} antes de:")
        print(tokenString)
    print("^^")
    advance()

#AST
class ASTNode:
    def __init__(self, kind, name=None, var_type=None, lineno=None):
        self.kind = kind            # Tipo de nodo (declaración, expresión, etc.)
        self.name = name            # Nombre de la variable o función (si aplica)
        self.var_type = var_type    # Tipo de la variable (INT, VOID, etc.)
        self.lineno = lineno        # Número de línea donde se encuentra
        self.children = []          # Lista de hijos del nodo
    
    def add_child(self, child):
        self.children.append(child)
    
    def print_ast(self, indent=0):
        """
        Función recursiva para imprimir el AST de manera legible.
        """
        indent_str = "  " * indent
        info = f"{self.kind}"
        if self.name is not None:
            info += f" name='{self.name}'"
        if self.var_type is not None:
            info += f" type='{self.var_type}'"
        if self.lineno is not None:
            info += f" line={self.lineno}"
        print(f"{indent_str}- {info}")
        for child in self.children:
            child.print_ast(indent + 1)



# Función principal del parser
def parse():
    global symbol_table
    symbol_table = SymbolTable("global")
    symbol_table.add_symbol("input", VarType.INT, VarKind.FUNCTION, lineno=0)
    symbol_table.add_symbol("output", VarType.VOID, VarKind.FUNCTION, lineno=0)
    root = ASTNode("root")  # Creamos el nodo raíz del árbol
    # Aquí puedes hacer el ciclo que va obteniendo los tokens uno por uno
    advance()  # Primer token
    #Llamar a la función que maneja el análisis de "program"
    while token != TokenType.ENDFILE:
        advance()  # Avanzamos al siguiente token
        program(root)
    print_symbol_tables(symbol_table)
    return root,symbol_table
def program(parent_node):
    var_node = ASTNode("program")
    parent_node.add_child(var_node)
    declaration_list(var_node)

def declaration_list(parent_node):
    while token in (TokenType.INT, TokenType.VOID):
        declaration(parent_node)

def declaration(parent_node):
    global posfun
    global postype
    if token in (TokenType.INT, TokenType.VOID):
        decl_node = ASTNode("declaration", name=tokenString, var_type=token.name,lineno=linea)
        parent_node.add_child(decl_node)  # Se añade al árbol de sintaxis
        advance()
        if token == TokenType.ID:
            var_name = tokenString  # Nombre de la variable
            var_type = VarType.INT if token == TokenType.INT else VarType.VOID
            var_kind = VarKind.GLOBAL_VAR 
            if symbol_table.add_symbol(var_name, var_type, var_kind, linea):
                posfun=var_name
                postype=var_type
                advance()
            else:
                error(f"Error al declarar la variable {var_name}.")
            if token == TokenType.LPAREN:
                fun_declaration(decl_node)
            elif token in (TokenType.SEMI, TokenType.LBRACKET):
                var_declaration(decl_node,var_kind)
            else:
                error("Se esperaba '(' o ';' o '[' después del identificador.")
        else:
            error("Se esperaba un identificador después del tipo.")
    else:
        error("Se esperaba tipo 'int' o 'void' al inicio de una declaración.")

def var_declaration(parent_node,var_kind=VarKind.LOCAL_VAR):
    if token == TokenType.SEMI:
        if var_kind==VarKind.GLOBAL_VAR:
            glvar_node = ASTNode("glvar_declaration",name=posfun, var_type=postype,lineno=linea)
            parent_node.add_child(glvar_node)  # Añadimos al árbol de sintaxis
        advance()  # Caso: int x;       
    elif token == TokenType.LBRACKET:
        advance()  # int x[
        if token == TokenType.NUM:
            advance()
            if token == TokenType.RBRACKET:
                advance()  # int x[10];
                if token == TokenType.SEMI:
                    advance()
                else:
                    error("Se esperaba ';' después de ']' en var_declaration.")
            else:
                error("Se esperaba ']' en var_declaration.")
        else:
            error("Se esperaba un número después de '[' en var_declaration.")
    else:
        error("Se esperaba ';' o '[' en var_declaration.")
    
def fun_declaration(parent_node):
    global symbol_table, posfun
    fun_node = ASTNode("fun_declaration",name=posfun, var_type=postype,lineno=linea)
    parent_node.add_child(fun_node)  # Añadimos al árbol de sintaxis
    if token == TokenType.LPAREN:
        advance()
        # Creamos tabla temporal para esta función
        temp_table = SymbolTable(posfun, symbol_table)
        symbol_table.add_child(temp_table)
        # Pasamos temporalmente la tabla temporal al parser de params
        previous_table = symbol_table
        symbol_table = temp_table

        params(fun_node)
        if token == TokenType.RPAREN:
            advance()
            # Al finalizar la función, dejamos activa la tabla global nuevamente
            compound_stmt(fun_node,create_table=False)
            symbol_table = previous_table
        else:
            error("Se esperaba ')' después de los parámetros.")
    else:
        error("Se esperaba '(' después del nombre de función.")
def params(parent_node):
    if token == TokenType.VOID:
        advance()
    else:
        param_list(parent_node)
def param_list(parent_node):
    param(parent_node)
    while token == TokenType.COMMA:
        advance()
        param(parent_node)
def param(parent_node):
    if token in (TokenType.INT, TokenType.VOID):
        tipo_token = token
        param_node = ASTNode("param", name=tokenString, var_type=token.name,lineno=linea)
        parent_node.add_child(param_node)  # Añadimos al árbol de sintaxis
        advance()
        if token == TokenType.ID:
            nombre_var = tokenString
            tipo_var = VarType.INT if tipo_token == TokenType.INT else VarType.VOID
            # Asegurarse de agregar solo a la tabla local
            if symbol_table.parent is not None:  # Solo si la tabla tiene una tabla padre (local)
                symbol_table.add_symbol(nombre_var, tipo_var, VarKind.LOCAL_VAR, linea)
                parvar_node = ASTNode("param", name=nombre_var, var_type=tipo_var,lineno=linea)
                param_node.add_child(parvar_node)  # Añadimos al árbol de sintaxis
            advance()
            if token == TokenType.LBRACKET:
                advance()  # [
                if token == TokenType.RBRACKET:
                    advance()  # ]
                else:
                    error("Se esperaba ']' después de '[' en param.")
        else:
            error("Se esperaba un identificador después del tipo en param.")
    else:
        error("Se esperaba tipo 'int' o 'void' en param.")
def compound_stmt(parent_node,create_table=False):
    global symbol_table,posfun
    if token == TokenType.LBRACE:
        advance()
        previous_table = symbol_table  
        if create_table==True:
            temp_table = SymbolTable(posfun, symbol_table)
            symbol_table.add_child(temp_table)
            symbol_table = temp_table
        local_declarations(parent_node)
        statement_list(parent_node)
        if lookahead_is(TokenType.RBRACE):
            advance()
        if token == TokenType.RBRACE:
            # Al finalizar la función, dejamos activa la tabla global nuevamente
            symbol_table = previous_table
            advance()
        else:
            error("Se esperaba '}' al final de compound_stmt.")
    else:
        error("Se esperaba '{' al inicio de compound_stmt.")
        
def local_declarations(parent_node):
    while token in (TokenType.INT, TokenType.VOID):
        tipo_token = token
        tipo_var = VarType.INT if tipo_token == TokenType.INT else VarType.VOID
        advance()  # Consumimos INT o VOID
        if token == TokenType.ID:
            var_name = tokenString
            # Asegurarse de agregar solo a la tabla local
            if symbol_table.parent is not None:  # Solo si la tabla tiene una tabla padre (local)
                symbol_table.add_symbol(var_name, tipo_var, VarKind.LOCAL_VAR, linea)
            advance()
            var_declaration(parent_node)
        else:
            error("Se esperaba identificador después del tipo en declaración local.")
def statement_list(parent_node):
    while token in (
        TokenType.ID, TokenType.NUM, TokenType.LPAREN,
        TokenType.SEMI, TokenType.LBRACE, TokenType.IF,
        TokenType.WHILE, TokenType.RETURN
    ):
        statement(parent_node)
def statement(parent_node):
    if token != TokenType.LBRACE:
        statement_node = ASTNode("statement",name=tokenString, var_type=token.name,lineno=linea)
        parent_node.add_child(statement_node)  # Añadimos al árbol de sintaxis
    if token == TokenType.SEMI or token in (TokenType.ID, TokenType.NUM, TokenType.LPAREN):
        expression_stmt(statement_node)
    elif token == TokenType.LBRACE:
        compound_stmt(parent_node)
    elif token == TokenType.IF:
        selection_stmt(statement_node)
    elif token == TokenType.WHILE:
        iteration_stmt(statement_node)
    elif token == TokenType.RETURN:
        return_stmt(statement_node)
    else:
        error("Se esperaba una expresión, bloque, if, while o return.")

def expression_stmt(parent_node):
    if token == TokenType.SEMI:
        advance()  # Solo un punto y coma: ;
    else:
        expression(parent_node)
        if token == TokenType.SEMI:
            advance()
        else:
            error("Se esperaba ';' después de la expresión.")
def selection_stmt(parent_node):
    if token == TokenType.IF:
        advance()
        if token == TokenType.LPAREN:
            advance()
            expression(parent_node)
            if token == TokenType.RPAREN:
                advance()
                statement(parent_node)
                if token == TokenType.ELSE:
                    else_node = ASTNode("selection_stmt",name=tokenString, var_type=token.name,lineno=linea)
                    parent_node.add_child(else_node)
                    advance()
                    statement(else_node)
            else:
                error("Se esperaba ')' después de la expresión en 'if'.")
        else:
            error("Se esperaba '(' después de 'if'.")
    else:
        error("Se esperaba 'if' al inicio de una sentencia de selección.")
def iteration_stmt(parent_node):
    if token == TokenType.WHILE:
        advance()
        if token == TokenType.LPAREN:
            advance()
            expression(parent_node)
            if token == TokenType.RPAREN:
                advance()
                statement(parent_node)
            else:
                error("Se esperaba ')' después de la expresión en 'while'.")
        else:
            error("Se esperaba '(' después de 'while'.")
    else:
        error("Se esperaba 'while' al inicio de una sentencia de iteración.")
def return_stmt(parent_node):
    if token == TokenType.RETURN:
        advance()
        if token == TokenType.SEMI:
            advance()  # return ;
        else:
            expression(parent_node)  # return expression ;
            if token == TokenType.SEMI:
                advance()
            else:
                error("Se esperaba ';' después de la expresión en 'return'.")
    else:
        error("Se esperaba 'return' al inicio de una sentencia de retorno.")
def expression(parent_node,nnode=True):
    if nnode:
        expr_node = ASTNode("expression",name=tokenString, var_type=token.name,lineno=linea)
        parent_node.add_child(expr_node)
    else:
        expr_node=parent_node
    # Si el token es un identificador, vamos a buscar si es una asignación o una simple expresión
    if token == TokenType.ID:
        if lookahead_is(TokenType.LBRACKET) or lookahead_is(TokenType.ASSIGN):
            advance()
        if token == TokenType.LBRACKET:
            advance()  # Es un arreglo, procesamos el índice
            expression(expr_node)
            if token == TokenType.RBRACKET:
                advance()
        if token == TokenType.ASSIGN:
            ASSIGN_node = ASTNode("assign",name=tokenString, var_type=token.name,lineno=linea)
            parent_node.add_child(ASSIGN_node)
            advance()  # Asignación '='
            expression(ASSIGN_node,False)  # Procesamos la expresión de la derecha
        else:
            simple_expression(expr_node)  # Si no es una asignación, es una comparación o expresión simple
    else:
        simple_expression(expr_node)  # Si no es un identificador, solo procesamos como expresión simple


def var(parent_node):
    var_node = ASTNode("var",name=tokenString, var_type=token.name,lineno=linea)
    parent_node.add_child(var_node)
    if token == TokenType.ID:
        advance()  # Consumimos el identificador
        if token == TokenType.LBRACKET:
            advance()  # Consumimos '['
            expression(var_node)  # Procesamos la expresión dentro del índice del arreglo
            if token == TokenType.RBRACKET:
                advance()  # Consumimos ']'
            else:
                error("Se esperaba ']' en la expresión con arreglo.")
    else:
        error("Se esperaba un identificador en var.")
def simple_expression(parent_node):
    left = ASTNode("simple_expression", lineno=linea)
    # Procesando una additive_expression
    additive_expression(left)
    # Si encontramos un operador de comparación (relop), procesamos el lado derecho de la comparación
    if token in (TokenType.LTEQ, TokenType.LT, TokenType.GT, TokenType.GTEQ, TokenType.EQ, TokenType.NEQ):
        op_node = ASTNode("comp_op",name=tokenString, lineno=linea)
        advance()

        right = ASTNode("simple_expression", lineno=linea)
        additive_expression(right)

        op_node.add_child(left)
        op_node.add_child(right)
        parent_node.add_child(op_node)
    else:
        parent_node.add_child(left)            
def additive_expression(parent_node):
    left = ASTNode("expression_term")
    term(left)
    current_node = left
    while token in (TokenType.PLUS, TokenType.MINUS):
        op = tokenString
        lineno_op = linea
        advance()
        right = ASTNode("expression_term")
        term(right)

        # Crear nodo binary_op y poner left y right como hijos
        bin_node = ASTNode("binary_op", name=op, lineno=lineno_op)
        bin_node.add_child(current_node)
        bin_node.add_child(right)

        # El nuevo current_node es el binary_op
        current_node = bin_node
    parent_node.add_child(current_node)

def term(parent_node):
    left = ASTNode("term")
    factor(left)
    current_node = left
    while token in (TokenType.TIMES, TokenType.DIVIDE):
        op = tokenString
        lineno_op = linea
        advance()
        right = ASTNode("term")
        factor(right)
        # Crear nodo binary_op y poner left y right como hijos
        bin_node = ASTNode("binary_op", name=op, lineno=lineno_op)
        bin_node.add_child(current_node)
        bin_node.add_child(right)
        # El nuevo current_node es el binary_op
        current_node = bin_node
    parent_node.add_child(current_node)


def factor(parent_node):
    if token == TokenType.LPAREN:
        advance()
        expression(parent_node)
        if token == TokenType.RPAREN:
            advance()
        else:
            error("Se esperaba ')'.")
    elif token == TokenType.ID:
        callfun=tokenString
        calltype=token
        advance()
        if token == TokenType.LPAREN:
            call(parent_node,callfun,calltype)
        elif token == TokenType.LBRACKET:
            # Era acceso a arreglo (var con índice)
            advance()
            expression(parent_node)
            if token == TokenType.RBRACKET:
                advance()
            else:
                error("Se esperaba ']' después de la expresión en arreglo.")
        else:
            # Era simplemente una variable (var normal)
            ID_node = ASTNode("ID",name=callfun, var_type=calltype,lineno=linea)
            parent_node.add_child(ID_node)
    elif token == TokenType.NUM:
        num_node = ASTNode("num",name=tokenString, var_type=token.name,lineno=linea)
        parent_node.add_child(num_node)
        advance()
    else:
        error("Se esperaba una expresión válida.")

def call(parent_node,callfun,calltype):
    call_node = ASTNode("call",name=callfun, var_type=calltype,lineno=linea)
    parent_node.add_child(call_node)
    advance()  # Consumimos '('
    args(call_node)  # Procesamos los argumentos de la función
    if token == TokenType.RPAREN:
        advance()  # Consumimos ')'
    else:
        error("Se esperaba ')' después de los argumentos.")

def args(parent_node):
    
    if token != TokenType.RPAREN:  # Si no es el paréntesis de cierre, hay argumentos
        args_node = ASTNode("args",name=tokenString, var_type=token.name,lineno=linea)
        parent_node.add_child(args_node)
        arg_list(args_node)  # Llamamos a arg_list para procesar los argumentos
    # Si el token es RPAREN, no hay argumentos (caso vacío), por lo que no hacemos nada

def arg_list(parent_node):
    arg_list_node = ASTNode("arg_list",name=tokenString, var_type=token.name,lineno=linea)
    parent_node.add_child(arg_list_node)
    expression(arg_list_node)  # Primero procesamos una expresión
    while token == TokenType.COMMA:  # Mientras haya comas, procesamos más expresiones
        advance()  # Consumimos la coma
        expression(arg_list_node)  # Procesamos la siguiente expresión
        
        
        
def extract_all_function_parameters(ast_root):
    funciones = []

    def recorrer(node):
        if node.kind == "fun_declaration":
            nombre_funcion = node.name
            tipo_retorno = node.var_type
            parametros = []
            for hijo in node.children:
                if hijo.kind == "param":
                    parametros.append({
                        "nombre": hijo.name,
                        "tipo": hijo.var_type,
                        "linea": hijo.lineno
                    })
            funciones.append({
                "nombre_funcion": nombre_funcion,
                "tipo_retorno": tipo_retorno,
                "parametros": parametros
            })

        for child in node.children:
            recorrer(child)

    recorrer(ast_root)
    return funciones
