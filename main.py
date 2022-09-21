from graphviz import Digraph
import random
import copy

import lectorExpresiones
import traductorExpresion_a_AFN
import afn_a_afd
import traductorExpresion_a_AFD
import minimizacion_afd
import simulaciones

### Se importa el modulo Nodo para utilizar la estructura definida para nodos
from Nodo import Nodo

### Iniciamos con las entradas del usuario
pasar = False

while not pasar:
    ### Ingreso de la expresion
    expresion = input('Ingrese su expresion: ')

    ### Ingreso de cadena de caracteres a evaluar
    cadena = input('Ingrese su input de caracteres a evaluar: ')
    cadena = cadena.replace(' ', '')

    ### Se convierte la expresion regular a una estructura de arbol (listas agrupadas)
    arbolExpresionRegular, pasar, mensaje = lectorExpresiones.conversionExpresionRegular('(' + expresion + ')')
    ### Se convierte la expresion regular aumentada a una estructura de arbol (listas agrupadas)
    arbolExpresionRegularAFD, pasar, mensaje = lectorExpresiones.conversionExpresionRegular('(' + expresion + ')#')

    if not pasar:
        print(mensaje)

#print(arbolExpresionRegularAFD)

###---------------------------------------------AFN---------------------------------------------###
### Se convierten los nodos que no son operandos en Nodos para almacenar
### Conjunto estados, transiciones, estado inicial, estado final
arbolNodosExpresionRegular, correlativo = traductorExpresion_a_AFN.traduccionBase(arbolExpresionRegular, 0)

### Uso de Thomson para generar un nodo final con el conjunto de estados, simbolos, transiciones, estado inicial y estados finales
afn, correlativo = traductorExpresion_a_AFN.traduccionAFN(arbolNodosExpresionRegular, correlativo, 0)


### Simulacion AFN
resultadoAFN = simulaciones.simulacionAFN(afn, cadena)
if resultadoAFN:
    print(f"AFN: La cadena de caracteres ingresada \'{cadena}\' SI es parte del lenguaje generado por la expresion \'{expresion}\'")
else:
    print(f"AFN: La cadena de caracteres ingresada \'{cadena}\' NO es parte del lenguaje generado por la expresion \'{expresion}\'")

### Generar diagrama AFN
f = Digraph('Automata Finito No Determinista', filename='AFN'+str(random.random()))
f.attr(rankdir='LR', size='8,5')

f.attr('node', shape='doublecircle')
for estadoFinal in afn.estadosFinales:
    f.node(str(estadoFinal))

f.attr('node', shape='circle')
for estadoInicial in afn.estadoInicial:
    f.node(str(estadoInicial))

f.attr('node', shape='none')
f.node('')
for estadoInicial in afn.estadoInicial:
    f.edge('', str(estadoInicial), label='')

f.attr('node', shape='circle')
for transicion in afn.transiciones:
    f.edge(str(transicion[0]), str(transicion[2]), label=str(transicion[1]))

f.view()

###---------------------------------------------AFD---------------------------------------------###
### Creacion de subconjuntos para pasar de AFN -> AFD 
dStates, dTrans = afn_a_afd.traduccionAFD(afn)

### Creamos una estructura de Nodo para simular el AFD
afd = afn_a_afd.convertirAFDNodo(afn, dStates, dTrans)


### Simulacion AFD
resultadoAFD = simulaciones.simulacionAFD(afd, cadena)
if resultadoAFD:
    print(f"AFD: La cadena de caracteres ingresada \'{cadena}\' SI es parte del lenguaje generado por la expresion \'{expresion}\'")
else:
    print(f"AFD: La cadena de caracteres ingresada \'{cadena}\' NO es parte del lenguaje generado por la expresion \'{expresion}\'")

### Generar diagrama AFD
f = Digraph('Automata Finito Determinista', filename='AFD'+str(random.random()))
f.attr(rankdir='LR', size='8,5')

f.attr('node', shape='doublecircle')
for estadoFinal in afd.estadosFinales:
    f.node(str(estadoFinal))

f.attr('node', shape='circle')
for estadoInicial in afd.estadoInicial:
    f.node(str(estadoInicial))

f.attr('node', shape='none')
f.node('')
for estadoInicial in afd.estadoInicial:
    f.edge('', str(estadoInicial), label='')

f.attr('node', shape='circle')
for transicion in afd.transiciones:
    f.edge(str(transicion[0]), str(transicion[2]), label=str(transicion[1]))

f.view()

###------------------------------------------AFD-DIRECTO----------------------------------------###
### Se hace una sustitucion previa para las expresiones 
arbolNodosExpresionRegularSustituido = traductorExpresion_a_AFD.sustitucionPrevia(arbolExpresionRegularAFD)

arbolNodosExpresionRegularAFD, _, correspondencias = traductorExpresion_a_AFD.traduccionBase(arbolNodosExpresionRegularSustituido, 1, [])

### Obtenemos los nodos hojas que ya poseen sus posiciones
nodosHoja = traductorExpresion_a_AFD.devolverNodosHoja(arbolNodosExpresionRegularAFD, [])

### Se realiza la definicion de nodos que no son hojas con sus operaciones nullable, firstpos, lastpos
nodoRoot, nodos = traductorExpresion_a_AFD.definirNodosAFD(arbolNodosExpresionRegularAFD, 0, [])

### Unimos los nodos en un solo arreglo
nodosFinales = nodosHoja + nodos


### Se calcula la tabla de followpos con los nodosFinales resultantes
tablaFollowpos = traductorExpresion_a_AFD.followpos(nodosFinales, correspondencias)


### Obtener el conjunto de simbolos
simbolos = traductorExpresion_a_AFD.simbolosAFDDirecta(correspondencias)

### Obtener las transiciones y estados (el primer estado es el estado inicial)
dStatesAFD, dTransAFD  = traductorExpresion_a_AFD.traduccionAFDDirecta(nodoRoot, simbolos, tablaFollowpos, correspondencias)

### Posicion para determinar que estados son finales
posicionFinal = correspondencias[-1][1]

### Creamos una estructura de Nodo para simular el AFD
afdd = traductorExpresion_a_AFD.convertirAFDDirectaNodo(dStatesAFD, dTransAFD, simbolos, posicionFinal)


### Simulacion AFD Directa
resultadoAFDD = simulaciones.simulacionAFD(afdd, cadena)
if resultadoAFDD:
    print(f"AFD Directa: La cadena de caracteres ingresada \'{cadena}\' SI es parte del lenguaje generado por la expresion \'{expresion}\'")
else:
    print(f"AFD Directa: La cadena de caracteres ingresada \'{cadena}\' NO es parte del lenguaje generado por la expresion \'{expresion}\'")

### Generar diagrama AFD
f = Digraph('Automata Finito Determinista (Directa)', filename='AFD_Directa'+str(random.random()))
f.attr(rankdir='LR', size='8,5')

f.attr('node', shape='doublecircle')
for estadoFinal in afdd.estadosFinales:
    f.node(str(estadoFinal))

f.attr('node', shape='circle')
for estadoInicial in afdd.estadoInicial:
    f.node(str(estadoInicial))

f.attr('node', shape='none')
f.node('')
for estadoInicial in afdd.estadoInicial:
    f.edge('', str(estadoInicial), label='')

f.attr('node', shape='circle')
for transicion in afdd.transiciones:
    f.edge(str(transicion[0]), str(transicion[2]), label=str(transicion[1]))

f.view()

###------------------------------------------MINIMIZACION-AFD---------------------------------------###
### Minimizar el AFD generado a partir del AFN
afdmStates = minimizacion_afd.traduccionAFDMinimizado(afd)

### Ordenar el AFD minimizado con la estructura de Nodos
afdm = minimizacion_afd.convertirAFDMinimizadoNodo(afdmStates, afd)

### Simulacion AFD Minimizado
resultadoAFDM = simulaciones.simulacionAFD(afdm, cadena)
if resultadoAFDM:
    print(f"AFD Minimizado: La cadena de caracteres ingresada \'{cadena}\' SI es parte del lenguaje generado por la expresion \'{expresion}\'")
else:
    print(f"AFD Minimizado: La cadena de caracteres ingresada \'{cadena}\' NO es parte del lenguaje generado por la expresion \'{expresion}\'")

### Generar diagrama AFD Minimizado
f = Digraph('Automata Finito Determinista (Minimizado)', filename='AFD_Minimizado'+str(random.random()))
f.attr(rankdir='LR', size='8,5')

f.attr('node', shape='doublecircle')
for estadoFinal in afdm.estadosFinales:
    f.node(str(estadoFinal))

f.attr('node', shape='circle')
for estadoInicial in afdm.estadoInicial:
    f.node(str(estadoInicial))

f.attr('node', shape='none')
f.node('')
for estadoInicial in afdm.estadoInicial:
    f.edge('', str(estadoInicial), label='')

f.attr('node', shape='circle')
for transicion in afdm.transiciones:
    f.edge(str(transicion[0]), str(transicion[2]), label=str(transicion[1]))

f.view()
