import math


def is_op(a):
    if a == '+' or a == '*' or a == '?' or a == '|':
        return True
    return False
    

def there_is_concat(expresion):
    concatenacion = False
    for x in range(len(expresion) -1 ):
        if not is_op(expresion[x]):
            if not is_op(expresion[x + 1]):
                concatenacion = True
                break

    return concatenacion


def group_concat(expresion):
    separacion = []
    saltar = False
    for i in range(len(expresion)):  
        if saltar == False:  
            if i != (len(expresion) - 1):
                if (not is_op(expresion[i])) and (not is_op(expresion[i + 1])):
                    separacion.append([expresion[i], expresion[i + 1]])
                    saltar = True
                else:
                    separacion.append(expresion[i])
            else:
                separacion.append(expresion[i])
                return separacion
        else:
            if i != (len(expresion) - 1): 
                separacion.append(expresion[i + 1])
            else:
                return separacion
    return separacion

def conversionExpresionRegular(expresionString):
    pasar = True
    mensaje = ''
    expresionString = expresionString.replace(' ', '')


    if '||' in expresionString:
        mensaje = 'No puede tener 2 "|" juntos en la expresion'
        pasar = False
        return [], pasar, mensaje

    if ('(|' in expresionString) or ('(*' in expresionString) or ('(?' in expresionString) or ('(+' in expresionString):
        mensaje = 'Un operador no puede estar despues de un parentesis en la expresion'
        pasar = False
        return [], pasar, mensaje
    
    if is_op(expresionString[0]):
        mensaje = 'No puede tener un operador al principio de la expresion'
        pasar = False
        return [], pasar, mensaje

    if expresionString[-1] == '|':
        mensaje = 'No puede tener el operador "|" al final de la expresion'
        pasar = False
        return [], pasar, mensaje

    if '|)' in expresionString:
        mensaje = 'No puede tener el operador "|" antes del cierre de parentesis en la expresion'
        pasar = False
        return [], pasar, mensaje

    expresion = []
    for caracterExpresion in expresionString:
        expresion.append(caracterExpresion)

    expresion = ["("] + expresion + [")"]
    cantidadParentesis = 0
    guardarIzq = []
    guardarDer = []

  
    while ("(" in expresion) or (")" in expresion):
        while "(" in expresion:
            cantidadParentesis = cantidadParentesis + 1
            indice = expresion.index('(')
            guardarIzq = guardarIzq + expresion[:indice+1]
            expresion = expresion[indice+1:]

        while ")" in expresion:
            if cantidadParentesis > 0:
                cantidadParentesis = cantidadParentesis - 1
                indice = expresion.index(')')
                guardarDer = expresion[indice:] + guardarDer
                expresion = expresion[:indice]
            else:
                mensaje = 'Parentesis colocados incorrectamente en la expresion'
                pasar = False
                return [], pasar, mensaje


        while ('+' in expresion) or ('?' in expresion) or ('*' in expresion):
 
            mas = []
            asterisco = []
            interrogacion = []

            orden = []
            primero = None
            indi = math.inf

            if '+' in expresion:
                mas = ['+', expresion.index('+')]
            if '*' in expresion:
                asterisco = ['*', expresion.index('*')]
            if '?' in expresion:
                interrogacion = ['?', expresion.index('?')]

            if mas:
                orden.append(mas)
            if asterisco:
                orden.append(asterisco)
            if interrogacion:
                orden.append(interrogacion)

            for i in orden:
                if i[1] < indi:
                    indi = i[1]
                    primero = i[0]

            index = expresion.index(primero)
            try:
                caracterSeparacion = expresion.pop(index-1)
                operador = expresion.pop(index-1)

                sep1 = expresion[:index-1]
                sep2 = expresion[index-1:]

                if not sep1:
                    sep1 = [caracterSeparacion, operador]
                    expresion = [sep1] + sep2
                else:
                    sep1.append([caracterSeparacion, operador])
                    expresion = sep1 + sep2
            except IndexError:
                mensaje = 'Error en expresion'
                pasar = False
                return [], pasar, mensaje

        while there_is_concat(expresion):

            expresion = group_concat(expresion)

        while '|' in expresion:

            index = expresion.index('|')
            try:
                caracterSeparacion = expresion.pop(index-1)
                operador = expresion.pop(index-1)
                caracterSeparacion2 = expresion.pop(index-1)

                sep1 = expresion[:index-1]
                sep2 = expresion[index-1:]

                if not sep1:
                    sep1 = [caracterSeparacion, operador, caracterSeparacion2]
                    expresion = [sep1] + sep2
                else:
                    sep1.append([caracterSeparacion, operador, caracterSeparacion2])
                    expresion = sep1 + sep2
            except IndexError:
                mensaje = 'Error en expresion'
                pasar = False
                return [], pasar, mensaje

        if ("(" in guardarIzq) and (")" in guardarDer):
            if "(" in guardarIzq:
                guardarIzq.pop(-1)
            if ")" in guardarDer:
                guardarDer.pop(0)
            expresion = guardarIzq + [expresion] + guardarDer
            guardarIzq = []
            guardarDer = []
        else:
            mensaje = 'Parentesis colocados incorrectamente en la expresion'
            pasar = False
            return [], pasar, mensaje

    return expresion, pasar, mensaje
