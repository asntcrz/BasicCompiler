# -*- coding: utf-8 -*-
###******************************************************************
### COMPILADORES 2009-2010*** IMPLEMENTACION DEL GESTOR DE ERRORES **
###******************************************************************
### Aqui podemos hacer lo de las excepciones y demas mielda
### Veamos queremos almacenar los errores, para ello emplearemos
### los siguientes campos:
###       - Numero de linea, en el que se encuentra el error.
###		  - Tipo Error, ENUM('Lexico','Sintactico','Semantico',...)
###		  - Descripcion, una cadena de texto describiendo el problema
###
###*******************************************************************

## INICIALIZACION de errores
def inicializar_errores():
    global errores
    global errno
    errores= []
    errno = 0    

    global errores_internos
    global interno_errno
    errores_internos= []
    interno_errno = 0

## ERRORES INTERNOS
## ===========================================================================
def nuevo_error_interno(num,tipo,desc):
    global errores_internos
    global interno_errno
    errores_internos.append([num,tipo,desc])
    interno_errno = interno_errno + 1

def numero_errores_internos():
    global interno_errno
    return interno_errno

def mostrar_errores_internos():
    global errores_internos
    global interno_errno
    result = ""
    for i in range(interno_errno):
        result = result +" En la linea " + str(errores_internos[i][0]) + ": se produjo un error INTERNO de tipo " + errores_internos[i][1].upper() + "\t" + errores_internos[i][2].lower() +"\n"
    return result

##  ERRORES
## ===========================================================================
def nuevo_error(num,tipo,desc):
# Esta funcion anyade un error, con un maximo de un error por linea
    global errores
    global errno
    encontrado = False
    for i in range(errno):
        if not encontrado:
            if errores[i][0] == num:
                encontrado = True
        else: break

    if not encontrado:
        errores.append([num,tipo,desc])
        errno = errno + 1

def numero_errores():
    global errno
    return errno

def mostrar_errores():
    global errores
    global errno
    result = ""
    for i in range(errno):
        result = result +" En linea " + str(errores[i][0]) + ", error " + errores[i][1].upper() + ":\t" + errores[i][2] +"\n"
    return result