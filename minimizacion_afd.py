import copy
import itertools

from Nodo import Nodo

class Minimitation_AFD:
    
    def __init__(self):
        pass
    
    def get_key(self, dic, val):
        for key, value in dic.items():
             if val == value:
                 return key
    
        return "key doesn't exist"
    
    def traduccionAFDMinimizado(self, afd):
        Panterior = []
        Pactual = []

        transiciones = copy.deepcopy(afd.transiciones)

        simbolos = copy.deepcopy(afd.simbolos)

        estadosNoFinales = []
        estadosFinales = []

        for estado in afd.estados:
            if estado not in afd.estadosFinales:
                estadosNoFinales.append(estado)
            else:
                estadosFinales.append(estado)

        Pactual.append(copy.deepcopy(estadosFinales))
        Pactual.append(copy.deepcopy(estadosNoFinales))

        primeraVuelta = True
        while Pactual != Panterior:
            if primeraVuelta:
                primeraVuelta = False
                Panterior = copy.deepcopy(Pactual)

            for particion in range(len(Pactual)):
                combinaciones = itertools.combinations(Pactual[particion], 2)

                distinguibles = []
                for combinacion in combinaciones:
                    if (combinacion[0] not in distinguibles) and (combinacion[1] not in distinguibles):
                        for simbolo in simbolos:
                            estadoF1 = None
                            estadoF2 = None
                            for transicion in transiciones:
                                if (transicion[0] == combinacion[0]) and (transicion[1] == simbolo):
                                    estadoF1 = transicion[2]
                                if (transicion[0] == combinacion[1]) and (transicion[1] == simbolo):
                                    estadoF2 = transicion[2]

                            if (estadoF1 != None) and (estadoF2 != None):
                                for particion2 in Panterior:
                                    if (estadoF1 in particion2) and (estadoF2 not in particion2):
                                        distinguibles.append(combinacion[1])
                                else:
                                    estadoF1 = None
                                    estadoF2 = None

                Panterior = copy.deepcopy(Pactual)

                final = []
                for estado in Pactual[particion]:
                    if estado not in distinguibles:
                        final.append(estado)

                Pactual[particion] = final

                if distinguibles:
                    Pactual.append(distinguibles)

        return Pactual

    def convertirAFDMinimizadoNodo(self, Mstates, afd):
        diccionarioAFDM = {}
        contador = 0
        nodo = Nodo('')

        nodo.simbolos = copy.deepcopy(afd.simbolos)

        for estadoAFDM in Mstates:
            diccionarioAFDM[contador] = estadoAFDM
            nodo.estados.append(contador)
            contador = contador + 1

        for estadoAFDM in Mstates:
            for estadoInicial in afd.estadoInicial:
                if estadoInicial in estadoAFDM:
                    estado = self.get_key(diccionarioAFDM, estadoAFDM)
                    nodo.estadoInicial.append(estado)

        for estadoAFDM in Mstates:
            for estadoFinal in afd.estadosFinales:
                if estadoFinal in estadoAFDM:
                    estado = self.get_key(diccionarioAFDM, estadoAFDM)
                    nodo.estadosFinales.append(estado)

        for estadoAFDM in Mstates:
            for transicion in afd.transiciones:
                if transicion[0] in estadoAFDM:
                    for estadoAFDM2 in Mstates:
                        if transicion[2] in estadoAFDM2: 
                            estadoI = self.get_key(diccionarioAFDM, estadoAFDM)
                            estadoF = self.get_key(diccionarioAFDM, estadoAFDM2)
                            if [estadoI, transicion[1], estadoF] not in nodo.transiciones:
                                nodo.transiciones.append([estadoI, transicion[1], estadoF])

        return nodo
