import copy

class Nodo:
    def __init__(self, expresion):

        self.exp = expresion
        self.tipoCaracter = ''
        self.estados = []
        self.simbolos = [] 
        self.estadoInicial = [] 
        self.estadosFinales = [] 
        self.transiciones = [] 

        self.hijos = []
        self.posicion = None
        self.nullable = None
        self.firstpos = []
        self.lastpos = []
        self.tipoNodo = None

    def transicionBase(self, correlativoEstado):
        estadoFinal = correlativoEstado + 1

        self.simbolos = [self.exp]
        self.estadoInicial = [correlativoEstado]
        self.estadosFinales = [estadoFinal]
        self.estados = [correlativoEstado, estadoFinal]
        self.transiciones = [[
            correlativoEstado, 
            self.exp, 
            estadoFinal 
        ]]

        return estadoFinal + 1

    def operacionesBase(self, correlativoPosicion):

        self.hijos = []

        if self.exp == 'ε':
            self.posicion = None
            correlativoPosicion = correlativoPosicion - 1
        else:
            self.posicion = correlativoPosicion

        if self.exp == 'ε':
            self.nullable = True
        else:
            self.nullable = False

        if self.exp == 'ε':
            self.firstpos = []
        else:
            self.firstpos = [self.posicion]

        if self.exp == 'ε':
            self.lastpos = []
        else:
            self.lastpos = [self.posicion]

        return correlativoPosicion + 1

    def transicionOrAFN(self, nodo1, nodo2, correlativo):
        estadoFinal = correlativo + 1

        self.simbolos = ['ε'] + nodo1.simbolos + nodo2.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))

        self.estadoInicial = [correlativo]
        self.estadosFinales = [correlativo+1]

        self.estados = nodo1.estados + nodo2.estados + [correlativo,correlativo+1]
        self.estados = list(dict.fromkeys(self.estados))

        self.transiciones = nodo1.transiciones + nodo2.transiciones + [[
            self.estadoInicial[0],
            'ε', 
            nodo1.estadoInicial[0]
        ]] + [[
            self.estadoInicial[0],
            'ε', 
            nodo2.estadoInicial[0]
        ]] + [[
            nodo1.estadosFinales[0],
            'ε', 
            self.estadosFinales[0]
        ]] + [[
            nodo2.estadosFinales[0],
            'ε', 
            self.estadosFinales[0]
        ]]

        return estadoFinal + 1

    def transicionConcatAFN(self, nodo1, nodo2, correlativo):
        self.simbolos = nodo1.simbolos + nodo2.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))

        self.estadoInicial = nodo1.estadoInicial
        self.estadosFinales = nodo2.estadosFinales

        self.estados = nodo1.estados + nodo2.estados
        self.estados = list(dict.fromkeys(self.estados))
        self.estados.remove(nodo1.estadosFinales[0])

        self.transiciones = nodo1.transiciones + nodo2.transiciones

        for i in self.transiciones:
            if i[2] == nodo1.estadosFinales[0]:
                i[2] = nodo2.estadoInicial[0]

        return correlativo

    def transicionCerraduraAFN(self, nodo, correlativo):
        estadoFinal = correlativo + 1

        self.simbolos = ['ε'] + nodo.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))

        self.estadoInicial = [correlativo]
        self.estadosFinales = [correlativo + 1]
        self.estados = nodo.estados + [correlativo,correlativo+1]
        self.transiciones = nodo.transiciones + [[
            self.estadoInicial[0],
            'ε', 
            nodo.estadoInicial[0]
        ]] + [[
            nodo.estadosFinales[0],
            'ε', 
            nodo.estadoInicial[0]
        ]] + [[
            self.estadoInicial[0],
            'ε',
            self.estadosFinales[0]
        ]] + [[
            nodo.estadosFinales[0],
            'ε', 
            self.estadosFinales[0]
        ]]

        return estadoFinal + 1

    def transicionCerraduraPositivaAFN(self, nodo, correlativo):

        estadoFinal = correlativo + 1

        nodoCopia = Nodo('')
        nodoCopia.exp = nodo.exp
        nodoCopia.simbolos = copy.deepcopy(nodo.simbolos)
        nodoCopia.estados = copy.deepcopy(nodo.estados)
        nodoCopia.estadoInicial = copy.deepcopy(nodo.estadoInicial)
        nodoCopia.estadosFinales = copy.deepcopy(nodo.estadosFinales)
        nodoCopia.transiciones = copy.deepcopy(nodo.transiciones)

        self.simbolos = ['ε'] + nodo.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))

        self.estadoInicial = [correlativo]
        self.estadosFinales = [correlativo + 1]
        self.estados = nodo.estados + [correlativo,correlativo+1]
        self.transiciones = nodo.transiciones + [[
            self.estadoInicial[0],
            'ε', 
            nodo.estadoInicial[0]
        ]] + [[
            nodo.estadosFinales[0],
            'ε', 
            nodo.estadoInicial[0]
        ]] + [[
            self.estadoInicial[0],
            'ε',
            self.estadosFinales[0]
        ]] + [[
            nodo.estadosFinales[0],
            'ε',
            self.estadosFinales[0]
        ]]


        cantidadExtra = len(nodo.estados)

        arregloX = []
        arregloY = []


        for i in range(cantidadExtra):
            arregloX.append(nodoCopia.estados[i])
            arregloY.append(estadoFinal + 1 + i)
            nodoCopia.estados[i] = estadoFinal + 1 + i

        for j in range(len(nodo.transiciones)):
            s = arregloX.index(nodo.transiciones[j][0])
            nodo.transiciones[j][0] = arregloY[s]

            s = arregloX.index(nodo.transiciones[j][2])
            nodo.transiciones[j][2] = arregloY[s]

        s = arregloX.index(nodoCopia.estadoInicial[0])
        nodoCopia.estadoInicial[0] = arregloY[s]

        s = arregloX.index(nodoCopia.estadosFinales[0])
        nodoCopia.estadosFinales[0] = arregloY[s]

        self.simbolos = self.simbolos + nodoCopia.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))

        self.estadoInicial = self.estadoInicial
        nodoFinal = self.estadosFinales[0]
        self.estadosFinales = nodoCopia.estadosFinales

        self.estados = self.estados + nodoCopia.estados
        self.estados = list(dict.fromkeys(self.estados))
        self.estados.remove(nodoFinal)

        self.transiciones = self.transiciones + nodoCopia.transiciones

        for i in self.transiciones:
            if i[2] == nodoFinal:
                i[2] = nodoCopia.estadoInicial[0]

        return estadoFinal + 1 + cantidadExtra

    def transicionCerraduraInterogationAFN(self, nodo, correlativo):

        nodoEpsilon = Nodo('ε')
        correlativo = nodoEpsilon.transicionBase(correlativo)
        estadoFinal = correlativo + 1

        self.simbolos = ['ε'] + nodo.simbolos + nodoEpsilon.simbolos
        self.simbolos = list(dict.fromkeys(self.simbolos))


        self.estadoInicial = [correlativo]
        self.estadosFinales = [correlativo+1]

        self.estados = nodo.estados + nodoEpsilon.estados + [correlativo,correlativo+1]
        self.estados = list(dict.fromkeys(self.estados))

        self.transiciones = nodo.transiciones + nodoEpsilon.transiciones + [[
            self.estadoInicial[0],
            'ε', 
            nodo.estadoInicial[0]
        ]] + [[
            self.estadoInicial[0],
            'ε', 
            nodoEpsilon.estadoInicial[0]
        ]] + [[
            nodo.estadosFinales[0],
            'ε', 
            self.estadosFinales[0]
        ]] + [[
            nodoEpsilon.estadosFinales[0],
            'ε',
            self.estadosFinales[0]
        ]]

        return estadoFinal + 1

    def cerraduraE(self, estados):
        estados = copy.deepcopy(estados)
        conjuntoS = []
        for i in estados:
            conjuntoS.append(i)
            siguienteEstado = i
            movimientosE = []
            for j in self.transiciones:
                if j[0] == siguienteEstado and j[1] == 'ε':
                    movimientosE.append(copy.deepcopy(j))
            
            while movimientosE:
                siguienteTransicion = movimientosE.pop()
                if siguienteTransicion[1] == 'ε':
                    conjuntoS.append(siguienteTransicion[2])
                    for k in self.transiciones:
                        if k[0] == siguienteTransicion[2] and (k[0] not in conjuntoS or k[2] not in conjuntoS):
                            movimientosE.append(k)
                
        conjuntoS = list(dict.fromkeys(conjuntoS))
        return conjuntoS

    def move(self, S, c):
        conjuntoM = []
        for estado in S:
            for j in self.transiciones:
                if j[0] == estado and j[1] == c:
                    conjuntoM.append(j[2])

        return conjuntoM

    def transicionOrAFD(self, nodo1, nodo2):
        if nodo1.nullable or nodo2.nullable:
            self.nullable = True
        else:
            self.nullable = False

        self.firstpos = list(dict.fromkeys(nodo1.firstpos + nodo2.firstpos))

        self.lastpos = list(dict.fromkeys(nodo1.lastpos + nodo2.lastpos))

        self.tipoNodo = '|'

    def transicionConcatAFD(self, nodo1, nodo2):

        if nodo1.nullable and nodo2.nullable:
            self.nullable = True
        else:
            self.nullable = False

        if nodo1.nullable:
            self.firstpos = list(dict.fromkeys(nodo1.firstpos + nodo2.firstpos))
        else:
            self.firstpos = nodo1.firstpos

        if nodo2.nullable:
            self.lastpos = list(dict.fromkeys(nodo1.lastpos + nodo2.lastpos))
        else:
            self.lastpos = nodo2.lastpos
        

        self.tipoNodo = '.'

        self.hijos = [nodo1, nodo2]

    def transicionCerraduraAFD(self, nodo):

        self.nullable = True

        self.firstpos = nodo.firstpos

        self.lastpos = nodo.lastpos

        self.tipoNodo = '*'