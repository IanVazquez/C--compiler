from symboltable import *
from parser import *
def check_semantics(ast_root, symbol_table):
    global root
    root=ast_root
    errors = []
    check_main_function_exists(symbol_table, errors)
    check_node(ast_root, symbol_table, errors)
    if errors:
        print("Errores semánticos encontrados:")
        for error in errors:
            print(error)
    else:
        print("No se encontraron errores semánticos.")

def check_node(node, current_table, errors):
    # CASO 1: Uso de variable en un factor
    if node.kind == "factor":
        if node.name is not None:
            # Ignorar literales numéricos
            if node.name.isdigit():
                return
            
            # Buscar símbolo usando lookup_symbol_recursive
            symbol = lookup(current_table, node.name)
            if symbol is None:
                errors.append(f"Error: Variable '{node.name}' usada pero no declarada en línea {node.lineno}")

    # CASO 2: Cambio de ámbito por función
    elif node.kind == "fun_declaration":
        print(f"Buscando tabla hija para función '{node.name}' en ámbito '{current_table.scope_name}'")
        child_table = current_table.get_child_by_name(node.name)
        if child_table is None:
            errors.append(f"Error: No se encontró tabla de símbolos para función '{node.name}'")
            child_table = current_table  # para continuar sin crash

        for child_node in node.children:
            check_node(child_node, child_table, errors)
        return
    # CASO 3: Llamada a función (verificar cantidad de argumentos)
    elif node.kind == "call":
        function_name = node.name
        if function_name is None:
            errors.append(f"Error: Llamada a función sin nombre (línea {node.lineno})")
            return

        # Verificar que la función está declarada
        function_entry = lookup(current_table, function_name)
        if function_entry is None:
            errors.append(f"Error: Llamada a función '{function_name}' no declarada (línea {node.lineno})")
            return

        # Obtener cantidad de parámetros declarados desde el AST
        funcs_info = extract_all_function_parameters(root)
        func_info = next((f for f in funcs_info if f["nombre_funcion"] == function_name), None)
        num_declared = len(func_info["parametros"]) if func_info else 0

        # Contar argumentos pasados
        num_passed = 0
        passed_args_nodes = []
        for child in node.children:
            if child.kind == "args":
                for args_child in child.children:
                    if args_child.kind == "arg_list":
                        num_passed = len(args_child.children)
                        passed_args_nodes = args_child.children
        if function_name=="output":
            num_declared=1
            func_info = {"parametros": [{"tipo": "ANY"}]}
        if num_declared != num_passed:
            errors.append(
                f"Error: Llamada a '{function_name}' con {num_passed} argumento(s), "
                f"se esperaban {num_declared} (línea {node.lineno})"
            )
        else:
            for i, arg_node in enumerate(passed_args_nodes):
                tipo_esperado = func_info["parametros"][i]["tipo"]
                if not arg_node.name.isnumeric():
                    nombredevar=find_function_symbol_table(current_table,arg_node.name)
                    tipo_recibido=nombredevar.var_type.name
                else:
                    tipo_recibido="INT"
                if tipo_esperado != "ANY" and tipo_esperado != tipo_recibido:
                    errors.append(
                        f"Error: argumento {i+1} de '{function_name}' debe ser '{tipo_esperado}', "
                        f"pero se recibió '{tipo_recibido}' (línea {node.lineno})"
                    )


#------
    # Para todos los demás nodos, recorremos con la tabla actual
    for child_node in node.children:
        check_node(child_node, current_table, errors)

def check_main_function_exists(global_table, errors):
    main_symbol = global_table.symbols.get("main")
    if main_symbol is None or main_symbol.var_kind != VarKind.GLOBAL_VAR:
        errors.append("Error: No se encontró la función 'main' en la tabla global.")
