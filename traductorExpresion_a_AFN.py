import copy

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
from Nodo import Nodo

### Funcion que permite determinar si un caracter es un operador
def is_op(a):
    if a == '+' or a == '*' or a == '?' or a == '|':
        return True
    return False

### Funcion que permite contruir un AFN para el OR
def orAFN(nodos, nodo2, correlativo):
    ### Generamos las transiciones y luego guardamos en Nodo
    nodo = Nodo('')

    correlativo = nodo.transicionOrAFN(nodos[0], nodo2, correlativo)

    return nodo, correlativo

### Funcion que permite contruir un AFN para la CONCATENACION
def concatAFN(nodos, nodo2, correlativo):
    ### Generamos las transiciones y luego guardamos en Nodo
    nodo = Nodo('')

    correlativo = nodo.transicionConcatAFN(nodos[0], nodo2, correlativo)

    return nodo, correlativo

### Funcion que permite contruir un AFN para la cerradura KLEEN
def cerraduraAFN(nodos, correlativo):
    ### Generamos las transiciones y luego guardamos en Nodo
    nodo = Nodo('')

    correlativo = nodo.transicionCerraduraAFN(nodos[0], correlativo)

    return nodo, correlativo

### Funcion que permite contruir un AFN para la cerradura POSITIVA
def cerraduraPositivaAFN(nodos, correlativo):
    ### Generamos las transiciones y luego guardamos en Nodo
    nodo = Nodo('')

    correlativo = nodo.transicionCerraduraPositivaAFN(nodos[0], correlativo)

    return nodo, correlativo

### Funcion que permite contruir un AFN para la cerradura INTERROGACION
def cerraduraInterogationAFN(nodos, correlativo):
    ### Generamos las transiciones y luego guardamos en Nodo
    nodo = Nodo('')

    correlativo = nodo.transicionCerraduraInterogationAFN(nodos[0], correlativo)

    return nodo, correlativo

### Funcion que permite tomar una expresion en forma de listas (arbol) y reemplazar los caracteres por Nodos AFN's Base
def traduccionBase(expresion, correlat):
    correlativo = correlat
    
    ### Por cada nodo en la expresion
    for nodo in range(len(expresion)):
        ### Si el elemento es otra lista, llamamos recursivamente al metodo
        if type(expresion[nodo]) == list:
            _, correlativo = traduccionBase(expresion[nodo], correlativo)
        ### En caso el elemento sea un caracter
        else:
            ### Revisar si es un nodo que no es un operador
            if not is_op(expresion[nodo]):
                ### Si es un caracter vamos a crear el nodo y reemplazarlo en el arreglo original
                nuevoNodo = Nodo(expresion[nodo])
                correlativo = nuevoNodo.transicionBase(correlativo)
                expresion[nodo] = nuevoNodo

    ### Se devuelve la expresion con los nodos reemplazados y un correlativo para los estados siguientes en la construccion
    return expresion, correlativo

### Funcion para contruir el AFN a partir de una expresion dada en listas con Nodos y operadores
def traduccionAFN(expresion, correlat, contadorExp):
    correlativo = correlat
    contadorNodos = contadorExp
    nodos = []
    operador = ''

    ### Por cada elemento en la expresion
    for nodo in range(len(expresion)):
        ### Si es una lista entonces hay que hacer el proceso recursivo
        if type(expresion[nodo]) == list:
            nodo, correlativo = traduccionAFN(expresion[nodo], correlativo, 0)

            ### Revisamos la info previa al nodo para revisar si hay que hacer alguna operacion con el nodo devuelto
            if contadorNodos > 0:
                if contadorNodos > 0 and contadorNodos < 2 and operador != '|':
                    ### Vamos a operar Thomson para concatenacion
                    nodoNuevo, correlativo = concatAFN(nodos, nodo, correlativo)
                    nodos = [nodoNuevo]
                    contadorNodos = 1

                elif contadorNodos > 0 and contadorNodos < 2 and operador == '|':
                    ### Vamos a operar Thomson para |
                    nodoNuevo, correlativo = orAFN(nodos, nodo, correlativo)
                    nodos = [nodoNuevo]
                    contadorNodos = 1
                    operador = ''
            ### Si no hay nodo almacenado, solo guardarlo en la lista de nodos
            else:
                nodos.append(nodo)
                contadorNodos = contadorNodos + 1
        ### En caso de ser un nodo o un operador
        else:
            ### Si es un nodo o un operador hay que guardar el nodo, o guardar la expresion, u operar si ya es posible con
            ### los nodos almacenados y el operador
            if contadorNodos > 0:
                if (expresion[nodo] == '+' or expresion[nodo] == '*' or expresion[nodo] == '?') and contadorNodos == 1:
                    ### Vamos a operar Thomson para *
                    if expresion[nodo] == '*':
                        ### Mandamos el nodo con su correlativo
                        nodoNuevo, correlativo = cerraduraAFN(nodos, correlativo)
                        nodos = [nodoNuevo]
                        contadorNodos = 1

                    ### Vamos a operar Thomson para +
                    if expresion[nodo] == '+':
                        ### Mandamos el nodo con su correlativo
                        nodoNuevo, correlativo = cerraduraPositivaAFN(nodos, correlativo)
                        nodos = [nodoNuevo]
                        contadorNodos = 1

                    ### Vamos a operar Thomson para ?
                    if expresion[nodo] == '?':
                        ### Mandamos el nodo con su correlativo
                        nodoNuevo, correlativo = cerraduraInterogationAFN(nodos, correlativo)
                        nodos = [nodoNuevo]
                        contadorNodos = 1

                elif not is_op(expresion[nodo]) and (contadorNodos < 2 and contadorNodos > 0)  and operador != '|':
                    ### Vamos a operar Thomson para concatenacion
                    nodoNuevo, correlativo = concatAFN(nodos, expresion[nodo], correlativo)
                    nodos = [nodoNuevo]
                    contadorNodos = 1
                else:
                    ### Vamos a revisar si ya podemos operar el OR
                    if not is_op(expresion[nodo]) and (contadorNodos < 2 and contadorNodos > 0) and operador == '|':
                        ### Vamos a operar Thomson para |
                        nodoNuevo, correlativo = orAFN(nodos, expresion[nodo], correlativo)
                        nodos = [nodoNuevo]
                        contadorNodos = 1
                        operador = ''
                    else:
                        ### Guardamos el operador | entre los nodos y agregamos la cantidad de nodos
                        operador = '|'
            else:
                ### Si no hay nodo almacenado, solo guardarlo en la lista de nodos
                nodos.append(expresion[nodo])
                contadorNodos = contadorNodos + 1

    ### Se devuelve el ultimo nodo operado (AFN) y su correlativo del siguiente estado
    return nodos[0], correlativo
