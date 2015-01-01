# -*- coding: utf-8 -*-
###**********************************************************************
### COMPILADORES 2009-2010****IMPLEMENTACION DEL ANALIZADOR SINTACTICO **
###**********************************************************************
###
###**********************************************************************

from lexico import *
from tablasimbolos import *
from tabladecision import *
from errores import *
import optimizador as opt
import sys
import re
import copy
import gci
import gco

###************************************
### INTRODUCCION ANALISIS SINTACTICO **
###************************************

# Preparar los archivos de salida
salida1 = "Errores.txt"
salida2 = "Tokens.txt"
salida3 = "TablaSimbolos.txt"
salida4 = "codigo.ens"

# Comprobamos si se invoco correctamente el compilador
if len(sys.argv) < 2:
    print '\nUSO: sintactico.py archivo_entrada.bas\n'
    exit()
entrada= sys.argv[1]

if (len(sys.argv) == 3):
	verbose = sys.argv[2] 
else:	
	verbose = ""

if not entrada.endswith(".bas"):
    print '\nUSO: sintactico.py archivo_entrada.bas'
    print 'Recuerde el archivo acabar en .bas\n'
    exit()
try:
    fd1 = open (salida1,"w")
    fd2 = open (salida2,"w")
    fd3 = open (salida3,"w")
    fd = open(entrada,"r")
    fd4 = gci.Abrir_fichero()
except IOError:
    print 'No se encuentra el archivo' 
    exit()

###**********************************
### INVOCAMOS AL ANALIZADOR LEXICO **
###**********************************

inicializar_errores()
#Variables globales que vamos a usar
global linea
linea = 0
global M
M = 0 # contador de variables temporales

data = fd.read()
print '='*30
print 'CODIGO FUENTE:'
print '='*30
print data
print '='*30
lexico(data)			

#print '='*30                                  # Modo -Verbose
#print 'Se producen los siguientes tokens'     # Modo -Verbose
#print '='*30                                  # Modo -Verbose

# Bucle para escribir los tokens en un fichero
j=0
while len(listatokens) > j:
    tokencima = str(listatokens[j])
    j += 1
    fd2.write(tokencima + "\n")

# Funcion Pedir_Token
i = 0              # Inicializamos contador
def pedir_token():
    global i        # Apunta al token actual
    global linea    # El numero de linea del token
    global token    # El token devuelto por el lexico
    global lexema   # El lexema del identificador
    global valor    # Valor del entero o cadena constante

    if i < len(listatokens):
       tokenex = listatokens[i]
       i += 1
       if tokenex[0] == 'NUMBER':
          token = 'int'
          valor = tokenex[1]
       else:
          token = tokenex[1]
       if tokenex[0] == 'APARENT':
          token = '('
       elif tokenex[0] == 'CPARENT':
          token = ')'
       elif tokenex[0] == 'COMA':
          token = ','
       elif tokenex[0] == 'PYC':
          token = ';'
       elif tokenex[0] == 'ID':
          token = 'id'
          lexema = tokenex[1]
       elif tokenex[0] == 'CR':
          token = 'EOL'
       elif tokenex[0] == 'STRING':
          token = 'cadena'
          valor = tokenex[1]
       linea = tokenex[2]

def nuevo_temporal():
    global M
    M += 1
    etq = str(M) + 'temp'
    return etq

def printpila(a,b):
    for i in range(b):
        print a[i]       

###*********************************************
### IMPLEMENTACION DE LAS ACCIONES SEMANTICAS **
###*********************************************


# Atributos de los simbolos
#
#   Simbolo = [tipo,lugar,params,valor,...]
#
#   A falta de concretar mas o de hacerlo mejor!
#######################################################

#Inicializo la estructura de los atributos
Att = {'tipo':['null'], 'lugar':[-1],'params':[], 'valor':[]} # params es la lista de los argumentos de una funcion

# tipo  = Tipo del simbolo
# lugar = Nombre temporal que contendra el valor del simbolo
# params = La lista de parametros para la llamada a una funcion
# valor = guardamos el valor de las constantes enteras y cadenas

###**************************************
#   Axioma (tanto axioma real _S como S)
###**************************************

def _S_Acc():           # _S -> S {acc}
    ts_creartablaglobal()   # Creamos tabla de simbolos global
    global lexemas          # para seguir los identificadores en H
    lexemas = []
    gci.cuarteto = gci.CCuarteto('INICIO',None,None,None)
    gco.GenerarCO(gci.cuarteto, fd4)

def S_Acc1():           # S -> EOL S  {acc1}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] == ['Tipo_error']

def S_Acc2():           # S -> D_Def S {acc2}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error'] or pila_aux[top_a - 2][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] == ['Tipo_error']
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']

def S_Acc3():           # S -> D_Dim S {acc3}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error'] or pila_aux[top_a - 2][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] == ['Tipo_error']
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']

def S_Acc4():           # S -> {acc4} Sent S {acc5}
    gci.cuarteto = gci.CCuarteto('Main',None, None, None)
    gco.GenerarCO(gci.cuarteto, fd4)

def S_Acc5():           # S -> {acc4} Sent S {acc5}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error'] or pila_aux[top_a - 2][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] == ['Tipo_error']
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']

def S1_Acc1():       # S1 -> EOL S1 {acc1}
    if pila_aux[top_a - 1][1]["tipo"] == 'Tipo_error':
        pila_aux[top_a - 3][1]["tipo"] == 'Tipo_error'


def S1_Acc2():           # S1 -> end S2 {acc2}
    if pila_aux[top_a - 1][1]["tipo"] == 'Tipo_error':
        pila_aux[top_a - 3][1]["tipo"] = 'Tipo_error'
    else: 
        pila_aux[top_a - 3][1]["tipo"] = 'Tipo_ok'
    fd3.write(ts_generar_TSG())
    gci.cuarteto = gci.CCuarteto('fin', None, None, None)
    gco.GenerarCO(gci.cuarteto, fd4)
    gci.cuarteto = gci.CCuarteto('Datos', None, None, None)
    gco.GenerarCO(gci.cuarteto, fd4)
    gci.Cerrar_fichero(fd4)
    opt.optimizador_codigo()
    ts_destruirTablaGlobal()


def S1_Acc3():           # S1 -> Sent S1 {acc3}
    if pila_aux[top_a - 1][1]["tipo"] == 'Tipo_error' or pila_aux[top_a - 2][1]["tipo"] == 'Tipo_error':
        pila_aux[top_a - 3][1]["tipo"] == 'Tipo_error'
    else:
        pila_aux[top_a - 3][1]["tipo"] = 'Tipo_ok'

def S1_Acc4():        # S1 -> Sent S1 {acc4}
    if pila_aux[top_a - 1][1]["tipo"] == 'Tipo_error' or pila_aux[top_a - 2][1]["tipo"] == 'Tipo_error':
        pila_aux[top_a - 3][1]["tipo"] == 'Tipo_error'
    else:
        pila_aux[top_a - 3][1]["tipo"] = 'Tipo_ok'

def S1_Acc5():                   # S1 -> Sent S1 {acc5}
    if pila_aux[top_a - 1][1]["tipo"] == 'Tipo_error' or pila_aux[top_a - 2][1]["tipo"] == 'Tipo_error':
        pila_aux[top_a - 3][1]["tipo"] == 'Tipo_error'
    else:
        pila_aux[top_a - 3][1]["tipo"] = 'Tipo_ok'

def S1_Acc6():        # S1 -> Sent S1 {acc6}
    if pila_aux[top_a - 1][1]["tipo"] == 'Tipo_error' or pila_aux[top_a - 2][1]["tipo"] == 'Tipo_error':
        pila_aux[top_a - 3][1]["tipo"] == 'Tipo_error'
    else:
        pila_aux[top_a - 3][1]["tipo"] = 'Tipo_ok'

def S1_Acc7():            # S1 -> Sent S1 {acc7}
    if pila_aux[top_a - 1][1]["tipo"] == 'Tipo_error' or pila_aux[top_a - 2][1]["tipo"] == 'Tipo_error':
        pila_aux[top_a - 3][1]["tipo"] == 'Tipo_error'
    else:
        pila_aux[top_a - 3][1]["tipo"] = 'Tipo_ok'


def S2_Acc0():      # S2 -> / {acc0}
    pila_aux[top_a - 1][1]["tipo"] == ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []
    
def S2_Acc1():       # S2 -> EOL S2 {acc1}
    if pila_aux[top_a - 1][1]["tipo"] == 'Tipo_error':
        pila_aux[top_a - 3][1]["tipo"] == 'Tipo_error'
###**************************************
# zona Declaraciones
###**************************************
        
# FUNCIONES
###**************************************
# Cabecera
def D_Def_Acc():                # D_Def -> def id {acc} T
    global num_tsl
    global aargv
    aargv = []
    global lexema_fun
    if ts_buscar_lexema(lexema) == None:
        ts_insertar_lexema(lexema)
        ts_insertar_entrada(lexema, 'funcion')
        lexema_fun = lexema
        etq = ts_buscar_dir(lexema_fun)
        ts_crearTablaLocal()
        num_tsl += 1
        ts_insertar_lexema(lexema)
        ts_insertar_entrada(lexema, 'entero')
        ts_incrementar_tamra(lexema_fun,1)
        ts_insertar_dir(lexema)
        gci.cuarteto = gci.CCuarteto('DEF', etq, None, None)
        gco.GenerarCO(gci.cuarteto, fd4)
    else:
       nuevo_error(linea,'semantico','Identificador de funcion ya declarado')

# Cuerpo
def T_Acc():            # T -> ( Arg ) EOL BD end def {acc}
    global aargv
    global lexema_fun
    n = ts_tamano_ra("l")
    gci.cuarteto = gci.CCuarteto('EndDEF', None, None, None)
    gco.GenerarCO(gci.cuarteto, fd4)
    fd3.write(ts_generar_TSL())
    ts_destruirTablaLocal()
    ts_insertar_tipo_argc_fun(lexema_fun,aargv)
    ts_insertar_tamra(lexema_fun,n)

#Argumentos de la funcion
def Arg_Acc1():         # Arg -> id Y {acc1} W {acc2}
    global aargv
    if lexema not in aargv:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
        ts_insertar_lexema(lexema)
        if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_vacio']:
            ts_insertar_entrada(lexema,'entero')
            ts_insertar_dir(lexema)
            ts_incrementar_tamra(lexema_fun,1)
        elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:
            ts_insertar_entrada(lexema,'vector')
            ts_insertar_tam(lexema,int(valor))
            ts_insertar_dir(lexema)
            ts_incrementar_tamra(lexema_fun,int(valor))
        tipo = ts_buscar_tipo(lexema)
        aargv.append(tipo)
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Variable ya declarada')

        
def Arg_Acc2():         # Arg -> id Y {acc1} W {acc2}   
    global aargv
    global lexema_fun
    if pila_aux[top_a - 4][1]["tipo"] == ['Tipo_ok']:
        ts_insertar_tipo_argc_fun(lexema_fun,aargv)       

def Y_Acc1():           # Y -> / {acc1}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def Y_Acc2():           # Y -> ( int ) {acc2}
    pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']

def W_Acc1():           # W -> / {acc1}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def W_Acc2():           # W -> , Arg {acc2}
    pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]

#Cuerpo de la funcion
def BD_Acc1():          # BD -> D_Dim BodyDef {acc1}
    if pila_aux[top_a - 2][1]["tipo"] == ['Tipo_ok'] and pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']

def BD_Acc2():          # BD -> Sent BodyDef {acc2}
    if pila_aux[top_a - 2][1]["tipo"] == ['Tipo_ok'] and pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']

def BD_Acc3():          # BD -> D_Static BodyDef {acc3}
    if pila_aux[top_a - 2][1]["tipo"] == ['Tipo_ok'] and pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
    
def BodyDef_Acc1():   # BodyDef -> BD {acc1}
    pila_aux[top_a - 2][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]

def BodyDef_Acc2():    # BodyDef -> / {acc2}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

# VARIABLES ENTERAS
def D_Static_Acc():                             # D_Static -> static id {acc1} A
    if  ts_buscar_lexema(lexema) == None:       # Si no esta en ninguna tabla
       ts_insertar_lexema(lexema)               # Definicion multiple en la accion A
       ts_insertar_entrada(lexema, 'entero')
       ts_insertar_dir(lexema)
       ts_incrementar_tamra(lexema_fun,1)
    else:
       nuevo_error(linea,'semantico','Identificador de variable ya declarado')

def A_Acc():                                    # A ->, id {acc1} A
    if  ts_buscar_lexema(lexema) == None:       # Si no esta en ninguna tabla
       ts_insertar_lexema(lexema)               # Definicion multiple en la accion A
       ts_insertar_entrada(lexema, 'entero')
       ts_insertar_dir(lexema)
       ts_incrementar_tamra(lexema_fun,1)
    else:
       nuevo_error(linea,'semantico','Identificador de variable ya declarado')

# VARIABLES VECTORES
def D_Dim_Acc():                                # D_Dim -> dim id ( int ) {acc} Q
    if ts_buscar_lexema(lexema) == None:        #
        ts_insertar_lexema(lexema)              # Definicion multiple en la accion Q
        ts_insertar_entrada(lexema, 'vector')   #
        ts_insertar_tam(lexema,int(valor))      # Valor de la constante entera
        ts_insertar_dir(lexema)
        if ts_buscar_ts(lexema) == "TSL" :
            ts_incrementar_tamra(lexema_fun,int(valor))
    else:
        nuevo_error(linea,'semantico','Identificador de vector ya declarado')

def Q_Acc():                                    # Q -> , id ( int ) {acc}
    if ts_buscar_lexema(lexema) == None:        # 
        ts_insertar_lexema(lexema)              # Definicion multiple en la accion Q
        ts_insertar_entrada(lexema, 'vector')   #
        ts_insertar_tam(lexema,int(valor))      # Valor de la constante entera
        ts_insertar_dir(lexema)    
        if ts_buscar_ts(lexema) == "TSL" :
            ts_incrementar_tamra(lexema_fun,int(valor))
    else:
        nuevo_error(linea,'semantico','Identificador de vector ya declarado')

###**************************************
#   Sentencias
###**************************************

###************************************** 
#   Generales de sentencias
###**************************************

def Sent_Acc1():     # Sent -> Sent_If EOL {acc}
    pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 2][1]["tipo"]

def Sent_Acc2():     # Sent -> Sent_IO EOL {acc}
    pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 2][1]["tipo"]

def Sent_Acc3():     # Sent-> Sent_Let EOL {acc}
    pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 2][1]["tipo"]

def Sent_Acc4():     # Sent-> Sent_while EOL {acc}
    pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 2][1]["tipo"]

# Condicional if
###**************************************

def Sent_If_Acc1():                 # Sent_if -> if Exp {acc1} then X {acc2}
    gci.cuarteto = gci.CCuarteto('EVALEXPif',pila_aux[top_a - 1][1]["lugar"],None,None)
    gco.GenerarCO(gci.cuarteto, fd4)

def Sent_If_Acc2():                 # Sent_if -> if Exp {acc1} then X {acc2}
    if (pila_aux[top_a - 3][1]["tipo"] == ['bool'] or pila_aux[top_a - 3][1]["tipo"] == ['entero']) :
        if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:
            pila_aux[top_a - 5][1]["tipo"] = ['Tipo_ok']
            gci.cuarteto = gci.CCuarteto('Fin_if',None,None,None)
            gco.GenerarCO(gci.cuarteto, fd4)
        else:
            pila_aux[top_a - 5][1]["tipo"] = ['Tipo_error']
            nuevo_error(linea,'SEMANTICO','Sentencia invalida')
    else:
        pila_aux[top_a - 5][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'SEMANTICO','Condicion del if mal construida')

def X_Acc1():                       # X -> Sent_IO {acc}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:
        pila_aux[top_a - 2][1]["tipo"] = ['Tipo_ok']
    else:
        pila_aux[top_a - 2][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'SEMANTICO','Sentencia de E/S mal contruida')

def X_Acc2():                       # X -> Sent_Let {acc}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:
        pila_aux[top_a - 2][1]["tipo"] = ['Tipo_ok']
    else:
        pila_aux[top_a - 2][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'SEMANTICO','Sentencia de asignacion mal contruida')

# Sent_IO
###**************************************
def Sent_IO_Acc1():         # Sent_IO -> Sent_Input {acc}
    pila_aux[top_a - 2][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]

def Sent_IO_Acc2():         # Sent_IO -> Sent_Print {acc}
    pila_aux[top_a - 2][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
    

#Entrada/Salida input
###**************************************

def Sent_Input_Acc0():              # Sent_Input -> input id {acc0} Z {acc1}
    global lexemas
    #Inserto el elemento en la pila de lexemas
    lexemas = lexemas + [lexema]

def Sent_Input_Acc1():               # Sent_Input -> input id {acc0} Z {acc1}
    global lexemas
    lexe = lexemas[-1]
    tipo_id = ts_buscar_tipo(lexe)
    #Saco el elemento de la pila de lexemas
    lexemas = lexemas[0:-1]
    
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:       # id ha dado error
        pila_aux[top_a - 4][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Indice de variable ' + str(lexe) + ' no entero')
        
    elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_vacio']:     # id debe ser entero
        if tipo_id == 'vector' or tipo_id == 'funcion':
            pila_aux[top_a - 4][1]["tipo"] = ['Tipo_error']
            nuevo_error(linea,'semantico','Debe introducir una variable entera o un elemento del vector ' + str(lexe) + '')
        elif ts_getEstado() == 'Local':
            if tipo_id == None:             # Se declara variable implicitamente, se agrega a TS global
                ts_setEstado('Global')
                ts_insertar_lexema(lexe)
                ts_insertar_entrada(lexe,'entero')
                ts_insertar_dir(lexe)
                ts_setEstado('Local')
            pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']
            gci.cuarteto = gci.CCuarteto('INPUT',None,None,lexe)
            gco.GenerarCO(gci.cuarteto, fd4)
        elif ts_getEstado() == 'Global':
            if tipo_id == None:             # Declaracion implicita
                ts_insertar_lexema(lexe)
                ts_insertar_entrada(lexe,'entero')
                ts_insertar_dir(lexe)
            pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']
            gci.cuarteto = gci.CCuarteto('INPUT',None,None,lexe)
            gco.GenerarCO(gci.cuarteto, fd4)
            
    elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:        # id es un vector y ya debe estar declarado
        if tipo_id == 'funcion' or tipo_id == 'entero':
            pila_aux[top_a - 4][1]["tipo"] = ['Tipo_error']
            nuevo_error(linea,'semantico','La variable ' + str(lexe) + ' ha de ser un vector')
        elif ts_getEstado() == 'Local':
            if ts_buscar_lexema(lexe) == None:
                nuevo_error(linea,'semantico','Identificador ' + str(lexe) + ' no declarado')
            else:
                pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']
                gci.cuarteto = gci.CCuarteto('INPUT',pila_aux[top_a - 1][1]["lugar"],None,lexe)
                gco.GenerarCO(gci.cuarteto, fd4)
        elif ts_getEstado() == 'Global':
            if ts_buscar_lexema(lexe) == None:
                pila_aux[top_a - 4][1]["tipo"] = ['Tipo_error']
                nuevo_error(linea,'semantico','Vector ' + str(lexe) + ' no declarado')
            else:
                pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']
                gci.cuarteto = gci.CCuarteto('INPUT',pila_aux[top_a - 1][1]["lugar"],None,lexe)
                gco.GenerarCO(gci.cuarteto, fd4)
                
    lugar_id_let = ts_buscar_dir(lexe)        
    pila_aux[top_a - 2][1]["lugar"] = [lugar_id_let]


def Z_Acc1():                   # Z -> / {acc1}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def Z_Acc2():                   # Z -> ( Exp ) {acc2}
    if pila_aux[top_a - 2][1]["tipo"] == ['entero']:
        pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']
        pila_aux[top_a - 4][1]["lugar"] = pila_aux[top_a - 2][1]["lugar"]
    else:
        pila_aux[top_a - 4][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','La expresion para el input ha de ser entera')


#Entrada/Salida print
###**************************************
def Sent_Print_Acc():           # Sent_Print -> print P {acc}
    pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
    lugares = pila_aux[top_a - 1][1]["lugar"]
    for i in lugares:
        i_tipo = ts_buscar_tipo(i)
        if i_tipo == 'entero':        # Exp es entero
            t = ts_buscar_dir(i)
            gci.cuarteto = gci.CCuarteto('Print_Ent', t, i, None)
            gco.GenerarCO(gci.cuarteto, fd4)
        elif i[0] == '&':
            gci.cuarteto = gci.CCuarteto('Print_Cad', i, None, None)
            gco.GenerarCO(gci.cuarteto, fd4)
        
def P_Acc():                    # P -> Exp R {acc}
    if pila_aux[top_a - 2][1]["tipo"] == ['entero'] or pila_aux[top_a - 2][1]["tipo"] == ['cadena']:
        if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
            pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
            nuevo_error(linea,'semantico','Alguna expresion del print no es valida')

        elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:
            pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
            pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 2][1]["lugar"] + pila_aux[top_a - 1][1]["lugar"]
            
        elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_vacio']:
            pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
            pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 2][1]["lugar"] + pila_aux[top_a - 1][1]["lugar"]
            
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','La expresion del print debe ser un entero o cadena')  

def R_Acc1():               # R -> / {acc1}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []
    
def R_Acc2():               # R -> ; P {acc2}
    pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
    pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]

# Asigancion let
###**************************************

def Sent_Let_Acc0():                     # Sent_Let -> let id {acc0} M {acc1} = Exp {acc2}
    global lexemas
    lexemas = lexemas + [lexema]

def Sent_Let_Acc1():                     # Sent_Let -> let id {acc0} M {acc1} = Exp {acc2}
    global lexemas
    lexe = lexemas[-1]
    tipo_id_let = ts_buscar_tipo(lexe)
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error'] :# Si M es error
        pila_aux[top_a - 4][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Indice de variable ' + str(lexema) + ' no entero')
    elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_vacio'] :
        if tipo_id_let == 'funcion':         # Si es funcion es un error
            pila_aux[top_a - 4][1]["tipo"] = ['Tipo_error']
            nuevo_error(linea,'semantico','Debe introducir una variable entera o un vector: ' + str(lexema))
        elif tipo_id_let == 'vector': 
            pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']
        elif ts_getEstado() == 'Local':
            if tipo_id_let == None:         # Se declara la variable implicitamente, se inserta en TS global
                ts_setEstado('Global')
                ts_insertar_lexema(lexema)
                ts_insertar_entrada(lexema,'entero')
                ts_insertar_dir(lexema)
                ts_setEstado('Local')
            pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']
        elif ts_getEstado() == 'Global':  
            if tipo_id_let == None:         # Declaracion implicita
                ts_insertar_lexema(lexema)
                ts_insertar_entrada(lexema,'entero')
                ts_insertar_dir(lexema)
            pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']
            
    elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok'] :       # id es un vector y ya debe estar declarado
        if tipo_id_let == 'vector':
            if ts_getEstado() == 'Local':
                if ts_buscar_lexema(lexema) == None:
                    pila_aux[top_a - 4][1]["tipo"] = ['Tipo_error']
                    nuevo_error(linea,'semantico','Vector ' + str(lexema) + ' no declarado')
                else:
                    pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']
            elif ts_getEstado() == 'Global':
                if ts_buscar_lexema(lexema) == None:
                    pila_aux[top_a - 4][1]["tipo"] = ['Tipo_error']
                    nuevo_error(linea,'semantico','Vector ' + str(lexema) + ' no declarado')
                else:
                    pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']
        else:
             pila_aux[top_a - 4][1]["tipo"] = ['Tipo_error']
             nuevo_error(linea,'semantico','Vector ' + str(lexema) + ' no declarado')

    pila_aux[top_a - 2][1]["lugar"] = [str(lexe)]
             
def Sent_Let_Acc2():                     # Sent_Let -> let id {acc0} M {acc1} = Exp {acc2}
    global lexemas
    lexema_id = lexemas[-1]
    # si es entero, el resultado es el de sent_let
    if  pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 6][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','La expresion asignada a ' + str(lexemas[-1]) + ' no es valida.')

    elif pila_aux[top_a - 3][1]["tipo"] != ['Tipo_vacio']: # Es un acceso a un entero del vector
        if  pila_aux[top_a - 1][1]["tipo"] == ['entero']:
            lugar1 = pila_aux[top_a - 1][1]["lugar"][0]
            lugar2 = pila_aux[top_a - 3][1]["lugar"][0]
            gci.cuarteto = gci.CCuarteto('Asignacion',(lugar1,'dir'),lugar2,(lexema_id,'rel')) # (inm, dir)
            gco.GenerarCO(gci.cuarteto, fd4)
        else:
            nuevo_error(linea,'semantico','Al vector ' + str(lexema_id) + ' hay que asignarle un entero')
    else:
        if ts_buscar_tipo(lexema_id) == 'vector':   # Es un vector para asignar otro vector
            if  pila_aux[top_a - 1][1]["tipo"] == ['vector']:
                if ts_buscar_tam(lexema_id) == ts_buscar_tam(lexema):
                    pila_aux[top_a - 6][1]["tipo"] = ["Tipo_ok"]
                    lugar1 = pila_aux[top_a - 1][1]["lugar"][0]
                    lugar3 = pila_aux[top_a - 4][1]["lugar"][0]
                    dimension = ts_buscar_tam(lexema_id)
                    gci.cuarteto = gci.CCuarteto('Asignacion',(lugar1,'dir'),dimension,(lugar3,'dir')) # (inm, dir)
                    gco.GenerarCO(gci.cuarteto, fd4)
                else:
                    pila_aux[top_a - 6][1]["tipo"] = ['Tipo_error']
                    nuevo_error(linea,'semantico','Los vectores han de ser de la misma dimension')
            else:
                pila_aux[top_a - 6][1]["tipo"] = ['Tipo_error']
                nuevo_error(linea,'semantico','A un vector hay que asignar otro vector')   
        elif ts_buscar_tipo(lexema_id) == 'entero': # Es un entero para asignar una expresion entera cualquiera
            if  pila_aux[top_a - 1][1]["tipo"] == ['entero']:
                lugar1 = pila_aux[top_a - 1][1]["lugar"][0]
                lugar4 = lexemas[-1]
                gci.cuarteto = gci.CCuarteto('Asignacion',(lugar1,'dir'),None,(lugar4,'dir')) # (inm, dir)
                gco.GenerarCO(gci.cuarteto, fd4)
            else:
                nuevo_error(linea,'semantico','Al vector ' + str(lexema_id) + ' hay que asignarle una expresion entera')
        else:
            nuevo_error(linea,'semantico','no deberias aparecer')
    lexemas = lexemas[0:-1]
    
    
def M_Acc1():                           # M -> ( Exp ) {acc1}
    if pila_aux[top_a - 2][1]["tipo"] == ['entero']:
        if len(pila_aux[top_a - 2][1]["params"]) == 1:
            pila_aux[top_a - 4][1]["tipo"] = ['Tipo_ok']
            pila_aux[top_a - 4][1]["lugar"] = pila_aux[top_a - 2][1]["lugar"]
            pila_aux[top_a - 4][1]["valor"] = pila_aux[top_a - 2][1]["valor"]
    else:
        pila_aux[top_a - 4][1]["tipo"] = ['Tipo_error']

def M_Acc2():                           # M -> / {acc2}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

# Bucle while
###**************************************
def Sent_While_Acc1():
    gci.cuarteto = gci.CCuarteto('IniWhile',None,None,None)
    gco.GenerarCO(gci.cuarteto, fd4)

def Sent_While_Acc2(): # Sent_While -> while {acc1} Exp {acc2} EOL Sent Sent_Gen {acc3} wend EOL {acc4}
    if (pila_aux[top_a - 1][1]["tipo"] == ['bool'] or pila_aux[top_a - 1][1]["tipo"] == ['entero']) :
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
        gci.cuarteto = gci.CCuarteto('EVALEXPw',pila_aux[top_a - 1][1]["lugar"],None,None)
        gco.GenerarCO(gci.cuarteto, fd4)
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'SEMANTICO','Condicion del while mal construida')

def Sent_While_Acc3():        # Sent_While -> while {acc1} Exp {acc2} EOL Sent Sent_Gen {acc3} wend
    if (pila_aux[top_a - 1][1]["tipo"] == ['Tipo_vacio']) or (pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']):
        if (pila_aux[top_a - 2][1]["tipo"] == ['Tipo_ok']):
            pila_aux[top_a - 6][1]["tipo"] = ['Tipo_ok']
            gci.cuarteto = gci.CCuarteto('FinWhile',None,None,None)
            gco.GenerarCO(gci.cuarteto, fd4)
            
        else:
            pila_aux[top_a - 6][1]["tipo"] = ['Tipo_error']
            nuevo_error(linea,'SEMANTICO','Error en la sentencia del while')
    else:
        pila_aux[top_a - 6][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'SEMANTICO','Sentecia while invalida')

def Sent_Gen_Acc1():        # Sent_Gen -> Sent Sent_Gen {acc1}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
    else:
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 2][1]["tipo"]

def Sent_Gen_Acc2():        # Sent_Gen -> / {acc2}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []


#######################################################################################################
#   Expresiones
#######################################################################################################

###**************************************
#           OR
###**************************************
def Exp_Acc1():          # Exp -> AA {acc1} _Exp {acc2}
    pila_aux[top_a - 2][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
    pila_aux[top_a - 2][1]["params"] = pila_aux[top_a - 1][1]["params"]
    pila_aux[top_a - 2][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
    pila_aux[top_a - 2][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
    Pop1_Acc()

def Exp_Acc2():          # Exp -> AA {acc1} _Exp {acc2}     --  Exp = 'bool' | 'entero' | 'vector' | 'Tipo_error' | 'cadena'
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_vacio']:    # Aplicamos regla lambda
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 2][1]["tipo"]
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 2][1]["params"]
        pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 2][1]["lugar"]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 2][1]["valor"]
    elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:  # Propagamos error
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
    elif (pila_aux[top_a - 2][1]["tipo"] == ['bool'] or pila_aux[top_a - 2][1]["tipo"] == ['entero']) and (pila_aux[top_a - 1][1]["tipo"] == ['bool'] or pila_aux[top_a - 1][1]["tipo"] == ['entero']):
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 2][1]["params"]
        pila_aux[top_a - 3][1]["tipo"] = ['bool']
        temp = nuevo_temporal()
        pila_aux[top_a - 3][1]["lugar"] = [temp]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 2][1]["valor"]
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Solo se admite la operacion OR entre enteros y/o booleanos')
    
def _Exp_Acc0():        # _Exp -> / {acc0}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def _Exp_Acc1():        # _Exp -> OR AA {acc1} _Exp
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Mala construccion en el operador OR.')
        
    elif pila_aux[top_a - 1][1]["tipo"] == ['entero'] or pila_aux[top_a - 1][1]["tipo"] == ['bool']:
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop2_Acc()
        if pila_aux[top_a - 2][1]["tipo"] == ['entero'] or pila_aux[top_a - 2][1]["tipo"] == ['bool']:
            pila_aux[top_a - 2][1]["tipo"] = ['bool']
            lugarExp = pila_aux[top_a - 2][1]["lugar"]
            lugar_Exp = pila_aux[top_a - 1][1]["lugar"]
            temp = nuevo_temporal()
            ts_insertar_lexema(temp)
            ts_insertar_entrada(temp,'entero')
            ts_insertar_dir(temp) 
            if ts_buscar_ts(temp) == "TSL" :
                ts_incrementar_tamra(lexema_fun,1)
            gci.cuarteto = gci.CCuarteto('OPEROR',lugarExp,lugar_Exp,temp)
            gco.GenerarCO(gci.cuarteto, fd4)
            pila_aux[top_a - 2][1]["lugar"] = [temp]
            Pop1_Acc()
        else:
            nuevo_error(linea,'semantico','El primer operando de la operacion OR debe ser entero y/o booleano.')
    else:
        nuevo_error(linea,'semantico','Solo se admite la operacion OR entre enteros y/o booleanos')      
        
        
###**************************************
#           AND
###**************************************

def AA_Acc1():          # AA -> BB {acc1} _AA {acc2}
    pila_aux[top_a - 2][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
    pila_aux[top_a - 2][1]["params"] = pila_aux[top_a - 1][1]["params"]
    pila_aux[top_a - 2][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
    pila_aux[top_a - 2][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
    Pop1_Acc()

def AA_Acc2():          # AA -> BB {acc1} _AA {acc2}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_vacio']:    # Aplicamos regla lambda
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 2][1]["tipo"]
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 2][1]["params"]
        pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 2][1]["lugar"]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 2][1]["valor"]
    elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:  # Propagamos error
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
    elif (pila_aux[top_a - 2][1]["tipo"] == ['bool'] or pila_aux[top_a - 2][1]["tipo"] == ['entero']) and (pila_aux[top_a - 1][1]["tipo"] == ['bool'] or pila_aux[top_a - 1][1]["tipo"] == ['entero']):
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 2][1]["params"]
        pila_aux[top_a - 3][1]["tipo"] = ['bool']
        temp = nuevo_temporal()
        pila_aux[top_a - 3][1]["lugar"] = [temp]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 2][1]["valor"]
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Solo se admite la operacion AND entre enteros y/o booleanos')
    
def _AA_Acc0():        # _AA -> / {acc0}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def _AA_Acc1():        # _AA -> AND BB {acc1} _AA
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Mala construccion en el operador AND.')
        
    elif pila_aux[top_a - 1][1]["tipo"] == ['entero'] or pila_aux[top_a - 1][1]["tipo"] == ['bool']:
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop2_Acc()
        if pila_aux[top_a - 2][1]["tipo"] == ['entero'] or pila_aux[top_a - 2][1]["tipo"] == ['bool']:
            pila_aux[top_a - 2][1]["tipo"] = ['bool']
            lugarExp = pila_aux[top_a - 2][1]["lugar"]
            lugar_Exp = pila_aux[top_a - 1][1]["lugar"]
            temp = nuevo_temporal()
            ts_insertar_lexema(temp)
            ts_insertar_entrada(temp,'entero')
            ts_insertar_dir(temp) 
            if ts_buscar_ts(temp) == "TSL" :
                ts_incrementar_tamra(lexema_fun,1)
            gci.cuarteto = gci.CCuarteto('OPERAND',lugarExp,lugar_Exp,temp)
            gco.GenerarCO(gci.cuarteto, fd4)
            pila_aux[top_a - 2][1]["lugar"] = [temp]
            Pop1_Acc()
        else:
            nuevo_error(linea,'semantico','El primer operando de la operacion AND debe ser entero y/o booleano.')
    else:
        nuevo_error(linea,'semantico','Solo se admite la operacion AND entre enteros y/o booleanos')         
        
        
        
###**************************************
#          <>
###**************************************

def BB_Acc1():               # BB -> G {acc1} _BB {acc2}
        pila_aux[top_a - 2][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 2][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 2][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 2][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop1_Acc()
        
def BB_Acc2():                # BB -> G {acc1} _BB {acc2}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 2][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Solo se admite comparacion entre enteros')   

def _BB_Acc0():      # _BB -> / {acc0}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def _BB_Acc1():      # _BB -> > G {acc1} _BB
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Mala construccion en el operador relacional <>.')
        
    elif pila_aux[top_a - 1][1]["tipo"] == ['entero']:
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop2_Acc()
        if pila_aux[top_a - 2][1]["tipo"] == ['entero']:
            pila_aux[top_a - 2][1]["tipo"] = ['bool']
            lugarBB = pila_aux[top_a - 2][1]["lugar"]
            lugar_BB = pila_aux[top_a - 1][1]["lugar"]
            temp = nuevo_temporal()
            ts_insertar_lexema(temp)
            ts_insertar_entrada(temp,'entero')
            ts_insertar_dir(temp)
            if ts_buscar_ts(temp) == "TSL" :
                ts_incrementar_tamra(lexema_fun,1)
            gci.cuarteto = gci.CCuarteto('DISTINTO',lugarBB,lugar_BB,temp)
            gco.GenerarCO(gci.cuarteto, fd4)
            pila_aux[top_a - 2][1]["lugar"] = [temp]
            Pop1_Acc()
        else:
            nuevo_error(linea,'semantico','El primer operando de la comparacion debe ser entero.')
    else:
        nuevo_error(linea,'semantico','Solo se admiten comparaciones entre enteros.')
        
        
###**************************************
#           =
###**************************************

def CC_Acc1():               # CC -> DD {acc1} _CC {acc2}
        pila_aux[top_a - 2][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 2][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 2][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 2][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop1_Acc()
        
def CC_Acc2():                # CC -> DD {acc1} _CC {acc2}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 2][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Solo se admite comparacion entre enteros')   

def _CC_Acc0():      # _CC -> / {acc0}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def _CC_Acc1():      # _CC -> = DD {acc1} _CC
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Mala construccion en el operador relacional =.')
        
    elif pila_aux[top_a - 1][1]["tipo"] == ['entero']:
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop2_Acc()
        if pila_aux[top_a - 2][1]["tipo"] == ['entero']:
            pila_aux[top_a - 2][1]["tipo"] = ['bool']
            lugarCC = pila_aux[top_a - 2][1]["lugar"]
            lugar_CC = pila_aux[top_a - 1][1]["lugar"]
            temp = nuevo_temporal()
            ts_insertar_lexema(temp)
            ts_insertar_entrada(temp,'entero')
            ts_insertar_dir(temp)
            if ts_buscar_ts(temp) == "TSL" :
                ts_incrementar_tamra(lexema_fun,1)
            gci.cuarteto = gci.CCuarteto('IGUAL',lugarCC,lugar_CC,temp)
            gco.GenerarCO(gci.cuarteto, fd4)
            pila_aux[top_a - 2][1]["lugar"] = [temp]
            Pop1_Acc()
        else:
            nuevo_error(linea,'semantico','El primer operando de la comparacion debe ser entero.')
    else:
        nuevo_error(linea,'semantico','Solo se admiten comparaciones entre enteros.')
        
        
###**************************************
#           <
###**************************************

def DD_Acc1():               # DD -> EE {acc1} _DD {acc2}
        pila_aux[top_a - 2][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 2][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 2][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 2][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop1_Acc()
        
def DD_Acc2():                # DD -> EE {acc1} _DD {acc2}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 2][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Solo se admite comparacion entre enteros')   

def _DD_Acc0():      # _DD -> / {acc0}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def _DD_Acc1():      # _DD -> < EE {acc1} _DD
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Mala construccion en el operador relacional >.')
        
    elif pila_aux[top_a - 1][1]["tipo"] == ['entero']:
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop2_Acc()
        if pila_aux[top_a - 2][1]["tipo"] == ['entero']:
            pila_aux[top_a - 2][1]["tipo"] = ['bool']
            lugarDD = pila_aux[top_a - 2][1]["lugar"]
            lugar_DD = pila_aux[top_a - 1][1]["lugar"]
            temp = nuevo_temporal()
            ts_insertar_lexema(temp)
            ts_insertar_entrada(temp,'entero')
            ts_insertar_dir(temp)
            if ts_buscar_ts(temp) == "TSL" :
                ts_incrementar_tamra(lexema_fun,1)
            gci.cuarteto = gci.CCuarteto('MENOR',lugarDD,lugar_DD,temp)
            gco.GenerarCO(gci.cuarteto, fd4)
            pila_aux[top_a - 2][1]["lugar"] = [temp]
            Pop1_Acc()
        else:
            nuevo_error(linea,'semantico','El primer operando de la comparacion debe ser entero.')
    else:
        nuevo_error(linea,'semantico','Solo se admiten comparaciones entre enteros.')
        
        
###**************************************
#           >
###**************************************

def EE_Acc1():               # EE -> FF {acc1} _EE {acc2}
        pila_aux[top_a - 2][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 2][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 2][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 2][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop1_Acc()
        
def EE_Acc2():                # EE -> FF {acc1} _EE {acc2}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 2][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Solo se admite comparacion entre enteros')   

def _EE_Acc0():      # _EE -> / {acc0}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def _EE_Acc1():      # _EE -> > FF {acc1} _EE
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Mala construccion en el operador relacional >.')
        
    elif pila_aux[top_a - 1][1]["tipo"] == ['entero']:
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop2_Acc()
        if pila_aux[top_a - 2][1]["tipo"] == ['entero']:
            pila_aux[top_a - 2][1]["tipo"] = ['bool']
            lugarEE = pila_aux[top_a - 2][1]["lugar"]
            lugar_EE = pila_aux[top_a - 1][1]["lugar"]
            temp = nuevo_temporal()
            ts_insertar_lexema(temp)
            ts_insertar_entrada(temp,'entero')
            ts_insertar_dir(temp)
            if ts_buscar_ts(temp) == "TSL" :
                ts_incrementar_tamra(lexema_fun,1)
            gci.cuarteto = gci.CCuarteto('MAYOR',lugarEE,lugar_EE,temp)
            gco.GenerarCO(gci.cuarteto, fd4)
            pila_aux[top_a - 2][1]["lugar"] = [temp]
            Pop1_Acc()
        else:
            nuevo_error(linea,'semantico','El primer operando de la comparacion debe ser entero.')
    else:
        nuevo_error(linea,'semantico','Solo se admiten comparaciones entre enteros.')
        
###**************************************
#           -
###**************************************

def FF_Acc1():                # FF -> GG {acc1(pop)} _FF {acc2}        
        pila_aux[top_a - 2][1]["tipo"] =  pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 2][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 2][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 2][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop1_Acc()

def FF_Acc2():                # FF -> GG  {acc1(pop)} _FF {acc2}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 2][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Expresion invalida en las sumas')

def _FF_Acc0():                  # _FF -> / {acc0}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def _FF_Acc1():                  # _FF -> - GG {acc1} _FF
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Mala construccion en la resta')

    if pila_aux[top_a - 1][1]["tipo"] == ['entero']:
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop2_Acc()
        if pila_aux[top_a - 2][1]["tipo"] == ['entero']:
            lugarFF = pila_aux[top_a - 2][1]["lugar"]
            lugar_FF = pila_aux[top_a - 1][1]["lugar"]
            temp = nuevo_temporal()
            ts_insertar_lexema(temp)
            ts_insertar_entrada(temp,'entero')
            if ts_buscar_ts(temp) == "TSL" :
                ts_incrementar_tamra(lexema_fun,1)
            ts_insertar_dir(temp)
            gci.cuarteto = gci.CCuarteto('RESTA',lugarFF,lugar_FF,temp)
            gco.GenerarCO(gci.cuarteto, fd4)
            pila_aux[top_a - 2][1]["lugar"] = [temp]
            Pop1_Acc()
        else:
            nuevo_error(linea,'semantico','El primer operando de la resta debe ser entero')
    else:
        nuevo_error(linea,'semantico','Solo se admiten restas entre enteros')
        
        
###**************************************
#           +
###**************************************


def GG_Acc1():                # GG -> U {acc1(pop)} _GG {acc2}        
        pila_aux[top_a - 2][1]["tipo"] =  pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 2][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 2][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 2][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop1_Acc()

def GG_Acc2():                # GG -> U  {acc1(pop)} _GG {acc2}
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 2][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Expresion invalida en las sumas')

def _GG_Acc0():                  # _GG -> / {acc0}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def _GG_Acc1():                  # _GG -> + U {acc1} _GG
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Mala construccion en la suma')

    if pila_aux[top_a - 1][1]["tipo"] == ['entero']:
        pila_aux[top_a - 3][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
        pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 3][1]["valor"] = pila_aux[top_a - 1][1]["valor"]
        Pop2_Acc()
        if pila_aux[top_a - 2][1]["tipo"] == ['entero']:
            lugarGG = pila_aux[top_a - 2][1]["lugar"]
            lugar_GG = pila_aux[top_a - 1][1]["lugar"]
            temp = nuevo_temporal()
            ts_insertar_lexema(temp)
            ts_insertar_entrada(temp,'entero')
            if ts_buscar_ts(temp) == "TSL" :
                ts_incrementar_tamra(lexema_fun,1)
            ts_insertar_dir(temp)
            gci.cuarteto = gci.CCuarteto('SUMA',lugarGG,lugar_GG,temp)
            gco.GenerarCO(gci.cuarteto, fd4)
            pila_aux[top_a - 2][1]["lugar"] = [temp]
            Pop1_Acc()
        else:
            nuevo_error(linea,'semantico','El primer operando de la suma debe ser entero')
    else:
        nuevo_error(linea,'semantico','Solo se admiten sumas entre enteros')


        
def U_Acc1():            # U -> H {acc1}
    pila_aux[top_a - 2][1]["tipo"] = pila_aux[top_a - 1][1]["tipo"]
    pila_aux[top_a - 2][1]["params"] = pila_aux[top_a - 1][1]["params"]
    pila_aux[top_a - 2][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
    pila_aux[top_a - 2][1]["valor"] = pila_aux[top_a - 1][1]["valor"]

def U_Acc2():            # U -> - H {acc2}
    if  pila_aux[top_a - 1][1]["tipo"] == ['entero']:
        pila_aux[top_a - 3][1]["tipo"] = ['entero']
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 1][1]["params"]
        temp = nuevo_temporal()
        ts_insertar_lexema(temp)
        ts_insertar_entrada(temp,'entero')
        if ts_buscar_ts(temp) == "TSL" :
            ts_incrementar_tamra(lexema_fun,1)
        ts_insertar_dir(temp)
        pila_aux[top_a - 3][1]["lugar"] = [temp]
        gci.cuarteto = gci.CCuarteto('MENOS_UNARIO',pila_aux[top_a - 1][1]["lugar"][0],None,temp)
        gco.GenerarCO(gci.cuarteto, fd4)

    else:
        pila_aux[top_a - 3][1]["tipo"] =  ['Tipo_error']
        nuevo_error(linea,'semantico','Solo se adminten enteros unoarios')

def H_Acc0():                      # H -> ( Exp ) {acc0}
    pila_aux[top_a - 4][1]["tipo"] = pila_aux[top_a - 2][1]["tipo"]
    pila_aux[top_a - 4][1]["params"] = pila_aux[top_a - 2][1]["params"]
    pila_aux[top_a - 4][1]["lugar"] = pila_aux[top_a - 2][1]["lugar"]

def H_Acc1():                       # H -> id {acc1} I {acc2}
    global lexemas
    lexemas = lexemas + [lexema]

def H_Acc2():                       # H -> id {acc1} I {acc2}
    global lexemas
    lexe = lexemas[-1]
    lexemas = lexemas[0:-1]
    tipo_lexema_id = ts_buscar_tipo(lexe)

    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:           # Propago el error...
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','El identificador ' + str(lexe) + ' esta mal construido')
        
        
    elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_vacio']:
        pila_aux[top_a - 3][1]["params"] = [tipo_lexema_id]
        if tipo_lexema_id == 'vector':  # Tiene q ser capaz de sacar un vector como v sin v(i) 
            pila_aux[top_a - 3][1]["tipo"] = ['vector']                # Para los argumentos de una funcion: def tercervalor(v) return v(3) end def
            pila_aux[top_a - 3][1]["lugar"] = [str(lexe)]

        elif tipo_lexema_id == 'entero': 
            est = ts_getEstado()
            ts_setEstado('Global')
            tipo_lexema_id2 = ts_buscar_tipo(lexe)
            ts_etq2 = ts_buscar_lexema(lexe)
            ts_setEstado(est)
            if tipo_lexema_id2 == 'funcion':                    # Si es la llamada recursiva a una funcion sin parametros
                ts_numarg = len(ts_buscar_tipo_argc_fun(lexe))
                if ts_numarg == 0:
                    ts_etq2 = ts_etq2[2]
                    temp = nuevo_temporal()
                    ts_insertar_lexema(temp)
                    ts_insertar_entrada(temp,'entero')
                    ts_insertar_dir(temp)
                    if ts_buscar_ts(temp) == "TSL" :
                        ts_incrementar_tamra(lexema_fun,1)
                    pila_aux[top_a - 3][1]["tipo"] = ['entero']
                    pila_aux[top_a - 3][1]["lugar"] = [temp]
                    gci.cuarteto = gci.CCuarteto('LLAM_FUN',ts_etq2,[],(temp,'dir'))  # (inm, directo)
                    gco.GenerarCO(gci.cuarteto, fd4)
                else:
                    pila_aux[top_a - 3][1]["tipo"] = ['entero']            # Para que sake la variable entera que se llama igual q la funcion
                    pila_aux[top_a - 3][1]["lugar"] = [str(lexe)]
            else:
                pila_aux[top_a - 3][1]["tipo"] = ['entero']                # Las llamadas a funciones devuelven enteros, se consideran como tal.
                pila_aux[top_a - 3][1]["lugar"] = [str(lexe)]

        elif tipo_lexema_id == 'funcion':
            lista = ts_buscar_tipo_argc_fun(lexe)     # Obtener la lista de la tabla de simbolos
            lista_param = pila_aux[top_a - 1][1]["params"]
            if lista == lista_param:
                pila_aux[top_a - 3][1]["tipo"] = ['entero']      # I == Tipo_ok es: fun(a, 2+3, v(1)), entero.
                # Pasar la etiquieta
                est = ts_getEstado()
                ts_setEstado('Global')
                ts_etq = ts_buscar_lexema(lexe)
                ts_setEstado(est)
                ts_etq = ts_etq[2]
                temp = nuevo_temporal()
                ts_insertar_lexema(temp)
                ts_insertar_entrada(temp,'entero')
                ts_insertar_dir(temp)
                if ts_buscar_ts(temp) == "TSL" :
                    ts_incrementar_tamra(lexema_fun,1)
                pila_aux[top_a - 3][1]["lugar"] = [temp]
                gci.cuarteto = gci.CCuarteto('LLAM_FUN',ts_etq,[],(temp,'dir'))
                gco.GenerarCO(gci.cuarteto, fd4)
            else:
                pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
                nuevo_error(linea,'semantico','Los argumentos de la funcion ' + str(lexe)+' no son validos')
        elif tipo_lexema_id == None:
            print '**WARNING('+str(linea)+'): la variable "' + str(lexe).lower() + '" puede que no este inicializada a ningun valor.'
            pila_aux[top_a - 3][1]["tipo"] = ['entero']
            pila_aux[top_a - 3][1]["lugar"] = [str(lexe)]
            if ts_getEstado() == 'Local':
                ts_setEstado('Global')
                ts_insertar_lexema(lexe)
                ts_insertar_entrada(lexe,'entero')
                ts_insertar_dir(lexe)
                ts_setEstado('Local')
            else:
                ts_insertar_lexema(lexe)
                ts_insertar_entrada(lexe,'entero')
                ts_insertar_dir(lexe)

    elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:                 # Ha llegado todo bien por separado, termino de verificar
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 1][1]["params"]
        if tipo_lexema_id == 'entero':
            est = ts_getEstado()
            ts_setEstado('Global')
            tipo_lexema_id3 = ts_buscar_tipo(lexe)
            ts_setEstado(est)
            if tipo_lexema_id3 == 'funcion':
                tipo_lexema_id = 'funcion'

        if tipo_lexema_id == 'vector':
            pila_aux[top_a - 3][1]["tipo"] = ['entero']                 # I == Tipo_ok es: v(2+3), entero.
            temp = nuevo_temporal()
            ts_insertar_lexema(temp)
            ts_insertar_entrada(temp,'entero')
            if ts_buscar_ts(temp) == "TSL" :
                ts_incrementar_tamra(lexema_fun,1)
            ts_insertar_dir(temp)
            pila_aux[top_a - 3][1]["lugar"] = [temp]
            gci.cuarteto = gci.CCuarteto('LLAM_VECTOR',pila_aux[top_a - 1][1]["lugar"][0],lexe,temp)
            gco.GenerarCO(gci.cuarteto, fd4)
            
            if len(pila_aux[top_a - 1][1]["params"]) != 1:
                pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
                nuevo_error(linea,'semantico','Los vectores solo tienen un argumento')
                
        elif tipo_lexema_id == 'funcion':
            #Comprobar que los tipos coinciden!!!
            lista = ts_buscar_tipo_argc_fun(lexe)     # Obtener la lista de la tabla de simbolos
            lista_param = pila_aux[top_a - 1][1]["params"]
            lista_param.reverse()
            lugares = pila_aux[top_a - 1][1]["lugar"]
            if lista == lista_param:
                pila_aux[top_a - 3][1]["tipo"] = ['entero']      # I == Tipo_ok es: fun(a, 2+3, v(1)), entero.
                # Pasar la etiquieta
                est = ts_getEstado()
                ts_setEstado('Global')
                ts_etq = ts_buscar_lexema(lexe)
                ts_setEstado(est)
                ts_etq = ts_etq[2]
                temp = nuevo_temporal()
                ts_insertar_lexema(temp)
                ts_insertar_entrada(temp,'entero')
                if ts_buscar_ts(temp) == "TSL" :
                    ts_incrementar_tamra(lexema_fun,1)
                ts_insertar_dir(temp)
                pila_aux[top_a - 3][1]["lugar"] = [temp]
                gci.cuarteto = gci.CCuarteto('LLAM_FUN',ts_etq,lugares,(temp,'dir'))  # (inm, directo)
                gco.GenerarCO(gci.cuarteto, fd4)   
            else:
                pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
                nuevo_error(linea,'semantico','Los argumentos de la funcion ' + str(lexe) + ' no son validos')
        elif tipo_lexema_id == None:
            pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
            nuevo_error(linea,'semantico','Identificador ' + str(lexe) + ' no declarado')
        else:
            pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']

def H_Acc3():                      # H -> int {acc3}                -- H puede ser un entero
    pila_aux[top_a - 2][1]["tipo"] = ['entero']
    pila_aux[top_a - 2][1]["params"] = pila_aux[top_a - 2][1]["params"] + ['entero']
    pila_aux[top_a - 2][1]["valor"] = [valor]
    t = nuevo_temporal()
    ts_insertar_lexema(t)
    ts_insertar_entrada(t,'entero')
    ts_insertar_dir(t)
    if ts_buscar_ts(t) == "TSL" :
        ts_incrementar_tamra(lexema_fun,1)
    pila_aux[top_a - 2][1]["lugar"] = [t]
    gci.cuarteto = gci.CCuarteto('Asignacion',(valor,'inm'),None,(t,'dir'))  # (inm, directo)
    gco.GenerarCO(gci.cuarteto, fd4)

def H_Acc4():                      # H -> cadena {acc4}             -- o bien H puede ser cadena
    pila_aux[top_a - 2][1]["tipo"] = ['cadena']
    pila_aux[top_a - 2][1]["valor"] = [valor]
    etq = ts_generar_etiqueta("cad")
    etq = "&" + etq
    pila_aux[top_a - 2][1]["lugar"] = [etq]
    gci.cuarteto = gci.CCuarteto('GenerarCadena',valor,etq,None)
    gco.GenerarCO(gci.cuarteto, fd4)

def I_Acc1():                      # I -> ( J ) {acc1}                  # H puede ser o funcion o vector
    pila_aux[top_a - 4][1]["tipo"] = pila_aux[top_a - 2][1]["tipo"]     # I Heredara el tipo de J
    pila_aux[top_a - 4][1]["params"] = pila_aux[top_a - 2][1]["params"]     # I Heredara los parametros de J
    pila_aux[top_a - 4][1]["lugar"]  = pila_aux[top_a - 2][1]["lugar"]

def I_Acc2():                      # I -> /   Si I es lambda, entonces H es un identificador de variable entera
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["lugar"] = []

def J_Acc():                        # J -> Exp K {acc}
    global lexemas
    lexe = lexemas[-1]
    if pila_aux[top_a - 2][1]["tipo"] == ['vector']:
        if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
            pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
            nuevo_error(linea,'semantico','Alguna expresion del print no es valida')
        elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_vacio']:
            pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
            pila_aux[top_a - 3][1]["params"] = pila_aux[top_a -1][1]["params"] + pila_aux[top_a - 2][1]["tipo"]
            pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 3][1]["lugar"] + pila_aux[top_a - 2][1]["lugar"]
        elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:
            pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
            pila_aux[top_a - 3][1]["params"] = pila_aux[top_a -1][1]["params"] + pila_aux[top_a - 2][1]["tipo"]
            pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"] + pila_aux[top_a - 2][1]["lugar"]


    elif pila_aux[top_a - 2][1]["tipo"] == ['entero']:
        if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_error']:
            pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
            nuevo_error(linea,'semantico','Alguna expresion del print no es valida')
        elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_vacio']:
            pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
            pila_aux[top_a - 3][1]["params"] = pila_aux[top_a -1][1]["params"] + pila_aux[top_a - 2][1]["tipo"]
            pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 3][1]["lugar"] + pila_aux[top_a - 2][1]["lugar"]
        elif pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:
            pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
            pila_aux[top_a - 3][1]["params"] = pila_aux[top_a -1][1]["params"] + pila_aux[top_a - 2][1]["tipo"]
            pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"] + pila_aux[top_a - 2][1]["lugar"]
                # esto es para el codigo intermedio
                # print "sentencia de codigo intermedio 3"
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','La expresion en ' + str(lexe) + ' debe ser un entero o cadena') 
        
def K_Acc1():       # K -> / {acc1}
    pila_aux[top_a - 1][1]["tipo"] = ['Tipo_vacio']
    pila_aux[top_a - 1][1]["params"] = []
    pila_aux[top_a - 3][1]["lugar"] = []

def K_Acc2():       # K -> , J {acc2}       # Si K no es lambda, entonces J es una lista de expresiones
    if pila_aux[top_a - 1][1]["tipo"] == ['Tipo_ok']:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_ok']
        pila_aux[top_a - 3][1]["params"] = pila_aux[top_a - 1][1]["params"]
        pila_aux[top_a - 3][1]["lugar"] = pila_aux[top_a - 1][1]["lugar"]
    else:
        pila_aux[top_a - 3][1]["tipo"] = ['Tipo_error']
        nuevo_error(linea,'semantico','Error en los argumentos de la funcion' + str(lexema))

###**************************************
# Acciones semanticas referidas a los pops
###**************************************
def Pop1_Acc():
    global top_a
    temp=pila_aux.pop()
    top_a -= 1
def Pop2_Acc():
    global top_a
    for i in range(2):
       temp=pila_aux.pop()
       top_a -= 1
def Pop3_Acc():
    global top_a
    for i in range(3):
       temp=pila_aux.pop()
       top_a -= 1
def Pop4_Acc():
    global top_a
    for i in range(4):
       temp=pila_aux.pop()
       top_a -= 1
def Pop5_Acc():
    global top_a
    for i in range(5):
       temp=pila_aux.pop()
       top_a -= 1
def Pop6_Acc():
    global top_a
    for i in range(6):
       temp=pila_aux.pop()
       top_a -= 1
def Pop7_Acc():
    global top_a
    for i in range(7):
       temp=pila_aux.pop()
       top_a -= 1

###**************************************
### INICIO DE LAS ESTRUCTURAS DE DATOS **
###**************************************


# Lista de Terminales
Terminales = ['id', 'int', 'cadena', 'EOL', 'EOF', ';', ',', 'if', 'then', 'while', 'wend',
 'print', 'input', 'let', 'static', 'end', 'def', 'dim', '(', ')', 'or', 'and', '<>', '=', '<', '>', '-', '+']

# Lista de No Terminales
NoTerminales = ['_S', 'S', 'S1', 'S2', 'D_Dim', 'D_Def', 'Arg', 'BD', 'BodyDef', 'D_Static', 'Sent',
'Sent_If', 'Sent_While', 'Sent_IO', 'Sent_Gen', 'Sent_Print', 'Sent_Input', 'Sent_Let',
'A', 'M', 'N', 'Exp', 'AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', '_Exp', '_AA', '_BB', '_CC', '_DD', '_EE', '_FF', '_GG',
'H', 'I', 'J', 'K', 'P', 'Q', 'R', 'T', 'W', 'X', 'Y', 'Z', 'U']

#global pila_ppal
pila_ppal = []  # elemento = (simbolo,[atributos])
top_p = 0 	    # top
ntop_p = 0 	    # ntop

#global pila_aux
pila_aux = []   # elemento = (simbolo,[atributos])
top_a = 0       # top


# Inicializar las estructuras de datos
Att1 = copy.copy(Att)
Att1["tipo"] = ["Fin"]
pila_ppal.append(('$', Att1))    # El fin de cadena
Att2 = copy.copy(Att)
Att2["tipo"] = ["Axioma"]
pila_ppal.append(('_S',Att2))    # El axioma
top_p += 2
ntop_p += 2

# Creamos tabla decision
td_crearTablaDec()		

# Contador de Tablas de Simbolos locales
global num_tsl              
num_tsl = 0

# Variable condicion de parada del bucle
fin_bien = 0

###***************************************************
### INICIO DEL ALGORITMO DEL ANALIZADOR SINTACTICO **
###***************************************************

pedir_token()   	# pido el primer caracter de entrada

while numero_errores() == 0 and fin_bien == 0:

    cima = pila_ppal[-1][0] 	      # Consulto el primer elemento de la pila de trabajo
    if verbose.upper() == "DEB": print "\n\nentrada: ", token   # Modo -Verbose
    #if verbose.upper() == "DEB": print "pila_ppal"              # Modo -Verbose
    #if verbose.upper() == "DEB": printpila(pila_ppal,top_p)     # Modo -Verbose
    if verbose.upper() == "DEB": print "\npila_aux"             # Modo -Verbose
    if verbose.upper() == "DEB": printpila(pila_aux,top_a)      # Modo -Verbose

    
    #print "top_p=" + str(top_p) + "  ntop_p=" + str(ntop_p) + "  top_a=" + str(top_a)
  
    # Si la cima de la pila y el token son iguales y es $
    if (cima == '$') and (token == '$'):
       fin_bien = 1  		# La gramatica reconoce bien el lenguaje

    # Si la cima de la pila es un Terminal
    if (cima in Terminales):
        # Si la cima es igual al token de entrada y distinto de $
        if (cima == token) and (token != '$'):
            elemento = pila_ppal.pop()      # Al hacer pop hay que hacer push en la auxiliar
            pila_aux.append(elemento)       # Muevo el simbolo de la pila y sus atributos
            top_p -= 1                  # Actualizo contadores
            ntop_p -= 1
            top_a += 1
            pedir_token()
            if numero_errores() > 0:  # Si se encuentra un error lexico, detenemos el analisis
                break

        # Si la cima de la pila es un terminal, y no es igual a la cadena de entrada, error sintactico.            
        else:
            nuevo_error(linea,'sintactico','Se espera un "' + str(cima) + '"')

    # Si es un No Terminal, consultamos la tabla de decision
    if (cima in NoTerminales):
        acciones = td_consultarTablaDec(cima,token) # acciones contiene la consecuente de la produccion
        if acciones != []: 	                        # Si la lista de reglas no esta vacia, consulto las acciones
            elemento = pila_ppal.pop()		        # sacamos de la pila el elemento           
            pila_aux.append(elemento)               # al hacer pop hay que hacer push en la auxiliar
            top_p -= 1                              # Actualizo contadores
            ntop_p -= 1                             #
            top_a += 1                              #
            k = len(acciones) - 1		            # la regla correspondiente de la gramatica
            while k >= 0: 				            # Insertar en orden inverso los elementos en la pila
                if acciones[k] != '/':	            # Si es cualquier regla menos lambda
                    Att3 = copy.copy(Att)           # copia de att a att3
                    if re.search('.*_Acc.*',acciones[k]):
                        Att3 = {}
                    reg_accion = (acciones[k],Att3)
                    pila_ppal.append(reg_accion) # insertarla en la pila
                    ntop_p += 1
                    top_p += 1                      
                k -= 1
        else:
            if token != 'id':
                lexema = token
            nuevo_error(linea,'sintactico','la entrada "' + str(lexema) + '" no es valida')
            

    # Si la cima de la pila es una accion semantica, la ejecuto
    if re.search('.*_Acc.*',cima):
        cima = pila_ppal.pop()        # Saco la accion semantica
        if verbose.upper() == "DEB": print "EJECUTANDO: ", cima[0]
        exec cima[0]                  # Ejecutar Accion semantica
        cima = pila_ppal[-1][0]       # Consulto el primer elemento de la pila de trabajo
        top_p -= 1                # Resto el contador
        ntop_p -= 1

#if numero_errores() > 0:
#    nuevo_error(linea,'sintactico','La gramatica no acepta el codigo fuente')

###***********************************************
### GENERACION DE ARCHIVO DE SALIDA DE ERRORES  **
###***********************************************

# Comprueba si la compilacion termino correctamente y genera el archivo con los errores
# errores = errores_lex + errores_sint + errores_sem + errores

# ERRORES INTERNOS
# -----------------
if numero_errores_internos() != 0:
    print mostrar_errores_internos()

# ERRORES
# -----------------
if numero_errores() != 0:
    titulo_errores = '='*30+'\nLa compilacion ha finalizado con los siguientes errores\n'+'='*30+'\n'
    print titulo_errores
    print mostrar_errores()
    print '='*30
    fd1.write(titulo_errores)
    fd1.write(mostrar_errores())
    fd1.write('='*30)
else:
    titulo_errores = '='*30+'\nLa compilacion finalizo satisfactoriamente\n'+'='*30+'\n'
    print titulo_errores
    print '='*30
    fd1.write(titulo_errores)
    fd1.write('='*30)

#Cerramos los descriptores
fd.close()
fd1.close()
fd2.close()
fd3.close()
