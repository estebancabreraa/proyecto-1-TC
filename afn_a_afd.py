import copy

from Nodo import Nodo
    
def there_is_unmarked(d_states):
    for i in d_states:
        if i[1] == 0:
            return True
    return False

def return_first_unmarked(d_states):
    for i in d_states:
        if i[1] == 0:
            return i
    return False

def return_states_D( d_states):       
    return [the_state[0] for the_state in d_states]

def state_in_states( the_state, d_states):
    for d_state in d_states:
        if len(the_state) == len(d_state):
            keep = True
            for the_element in the_state:
                if the_element not in d_state:
                    keep = False
                    break
            if keep:
                return True
    return False

def return_state_in_states( the_state, d_states):
    for d_state in d_states:
        if len(the_state) == len(d_state[0]):
            keep = True
            for the_element in the_state:
                if the_element not in d_state[0]:
                    keep = False
                    break
            if keep:
                return d_state
    return False

def traduccionAFD(afn):
    d_states = []
    d_tran = []
    counter = 0
    d_states.append([afn.cerraduraE(afn.estadoInicial), 0, counter])
    while there_is_unmarked(d_states):
        estado_t = return_first_unmarked(d_states)
        estado_t[1] = 1
        simbolos = copy.deepcopy(afn.simbolos)
        if 'ε' in simbolos:
            simbolos.remove('ε')
        for simbolo in simbolos:
            U = afn.cerraduraE(afn.move(estado_t[0], simbolo))
            d_only_states = return_states_D(d_states)
            nuevo_estado = []
            if U:
                if not state_in_states(U, d_only_states):
                    counter = counter + 1
                    nuevo_estado = [U, 0, counter]
                    d_states.append([U, 0, counter])
                else:
                    nuevo_estado = return_state_in_states(U, d_states)

                d_tran.append([estado_t[2], simbolo, nuevo_estado[2]])

    return d_states, d_tran

def convert_afd_nodo( afn, d_states, d_tran):
    nodo = Nodo('')

    simbolos = copy.deepcopy(afn.simbolos)

    if 'ε' in simbolos:
        simbolos.remove('ε')
    nodo.simbolos = simbolos

    for estado in d_states:
        nodo.estados.append(estado[2])

    for estado in d_states:
        for estadoInicial in afn.estadoInicial:
            if estadoInicial in estado[0]:
                nodo.estadoInicial.append(estado[2])

    for estado in d_states:
        for estadoFinal in afn.estadosFinales:
            if estadoFinal in estado[0]:
                nodo.estadosFinales.append(estado[2])

    nodo.transiciones = copy.deepcopy(d_tran)
    return nodo
