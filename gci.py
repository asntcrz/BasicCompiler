# -*- coding: utf-8 -*-
###*******************************************************************************
### COMPILADORES 2009-2010****IMPLEMENTACION DEL GENERADOR DE CODIGO INTERMEDIO **
###*******************************************************************************
###
###*******************************************************************************
import os

class CCuarteto(object):
    def __init__(self, op, op_1, op_2, dest):
        self.operador = op
        self.operando1 = op_1
        self.operando2 = op_2
        self.result = dest      #destino de la operacion

        #print "Codigo Intermedio:",self.operador,self.operando1, self.operando2,self.result

global cuarteto
cuarteto = CCuarteto(None,None,None,None)

def DarOperador(self):
    if self.operador == None :
        return 'None'
    else:
        return self.operador

def DarResultado(self):
    return self.result
    
def DarOperando1(self):
    return self.operando1

def DarOperando2(self):
     return self.operando2

def EscribirCuarteto(fd, cuarteto):
    os.write(fd, "CUARTETO: ")
    os.write(fd,'( ')
    os.write(fd, DarOperador(cuarteto))
    os.write(fd,' , ')
    os.write(fd, str(DarOperando1(cuarteto)))
    os.write(fd,', ')
    os.write(fd, str(DarOperando2(cuarteto)))
    os.write(fd,', ')
    os.write(fd, str(DarResultado(cuarteto)))
    os.write(fd,')\n')

def Abrir_fichero():
    descp = os.open("cuartetos.txt", os.O_CREAT |os.O_RDWR|os.O_TRUNC)
    return descp

def Cerrar_fichero(fd):
    os.close(fd)
    
######################################################
#
#   REGISTRO DE ACTIVACION DEL COMPILADOR
#
######################################################
#
#       |¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯|
#       |           EM          |
#       |      -----------      |
#       |   Datos Temporales    |
#       |   Variables Locales   |
#       |       Parametros      |
#       |      ------------     |
#       |   Valor Devuelto      |
#       |_______________________|
#       | Puntero de Acceso: R9 |
#
#
#