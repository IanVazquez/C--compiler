from globalTypes import *

# Clase que representa un símbolo en la tabla
class Symbol:
    def __init__(self, name, var_type, var_kind, lineno):
        self.name = name           # Nombre del símbolo (identificador)
        self.var_type = var_type   # Tipo (VarType.INT, VarType.VOID)
        self.var_kind = var_kind   # GLOBAL_VAR, LOCAL_VAR, PARAM, FUNCTION
        self.lineno = lineno       # Línea donde se declaró

# Clase que representa una tabla de símbolos (por bloque)
class SymbolTable:
    def __init__(self, scope_name, parent=None):
        self.scope_name = scope_name   # Nombre del ámbito (por ejemplo, 'global', nombre de función)
        self.symbols = {}              # Diccionario: nombre → Symbol
        self.parent = parent           # Tabla padre (para buscar en ámbitos superiores)
        self.children = []
    
    def add_child(self, child_table):
        self.children.append(child_table)
        
    def add_symbol(self, name, var_type, var_kind, lineno):
        if name in self.symbols:
            print(f"Error: '{name}' ya declarado en este ámbito.")
            return False
        self.symbols[name] = Symbol(name, var_type, var_kind, lineno)
        return True

    def get_child_by_name(self, name):
        for child in self.children:
            if child.scope_name == name:
                return child
        return None


def print_symbol_tables(table, indent=0):
    prefix = "  " * indent
    print(f"{prefix}Tabla de símbolos: {table.scope_name}")
    for sym in table.symbols.values():
        print(f"{prefix}  {sym.name} ({sym.var_kind.name}, {sym.var_type.name}) en línea {sym.lineno +1}")
    for child in table.children:
        print_symbol_tables(child, indent + 1)

def lookup(table, name):
    current = table
    while current:
        if name in current.symbols:
            return current.symbols[name]
        current = current.parent
    return None

def find_function_symbol_table(table, function_name):
    for sym in table.symbols.values():
        if sym.name == function_name:
            return sym
    table=table.parent
    for sym in table.symbols.values():
        if sym.name == function_name:
            return sym
    return None
