### Programa que permite la simulacion de AFN y AFD dada una cadena de caracteres 

import copy

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
import Nodo

### Funcion para realizar la simulacion de un AFN, dado un AFN en forma de Nodo y un a cadena de caracteres
def simulacionAFN(afn, cadena):
    ### Se obtiene el conjunto de estados S a partir la cerradura E de los estados iniciales del AFN
    S = afn.cerraduraE(afn.estadoInicial)
    ### Iteramos sobre los caracteres de la cadena dada
    for c in cadena:
        ### Se obtiene el move de los estados en S con el caracter c
        ### Al resultado le aplicamos cerradura E y obtenemos el nuevo conjunto de estados S
        S = afn.cerraduraE(afn.move(S, c))

    ### Se procesa la interesccion entre la lista del conjunto de los estados S y la lista del conjunto de estados finales del AFN
    interseccion = set.intersection(set(S), set(afn.estadosFinales))
    interseccion = list(interseccion)

    ### Se determina si existe interesccion
    ### Si la hay entonces la cadena pertenece al Lenguaje representado por el AFN,
    ### Si no hay entonces la cadena no pertenece al Lenguaje representado por el AFN
    if interseccion:
        return True
    else:
        return False

### Funcion para realizar la simulacion de un AFD, dado un AFD en forma de Nodo y un a cadena de caracteres
def simulacionAFD(afd, cadena):
    ### Se obtiene el estado s siendo el estado inicial del AFD
    s = afd.estadoInicial
    ### Iteramos sobre los caracteres de la cadena dada
    for c in cadena:
        ### Se obtiene s atraves del move del estado s con el caracter c
        s = afd.move(s, c)

    ### Se procesa la interesccion entre la lista del estado s y la lista del conjunto de estados finales del AFD
    interseccion = set.intersection(set(s), set(afd.estadosFinales))
    interseccion = list(interseccion)

    ### Se determina si existe interesccion
    ### Si la hay entonces la cadena pertenece al Lenguaje representado por el AFD,
    ### Si no hay entonces la cadena no pertenece al Lenguaje representado por el AFD
    if interseccion:
        return True
    else:
        return False