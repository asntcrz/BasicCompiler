###********************************************************************
### COMPILADORES 2009-2010****IMPLEMENTACION DE LA TABLA DE SIMBOLOS **
###********************************************************************

from errores import *
import re
global palabrasreservadas 

palabrasreservadas = (
    'print',
    'input',
    'if',
    'then',
    'while',
    'wend',
    'end',
    'def',
    'static',
    'dim',
    'and',
    'or',
    'let')

global TSL
TSL = {}
despL = 0

global TSG
TSG = {}
despG = 0

global Estado
Estado = 'Global'        # No Hay local

global ancho            # ancho de un entero
ancho = 1

def ts_vector_TSG():
    return TSG.keys()

def ts_vector_TSL():
    return TSL.keys()

def ts_NElem_TSL():
    return len(TSL)

def ts_NElem_TSG():
    return len(TSG)

def ts_setEstado(est):
 global Estado
 Estado = est

def ts_getEstado():
 return Estado


# Esta funcion nos permite CREAR la tabla GLOBAL
def ts_creartablaglobal():
   global TSG
   global despG
   TSG = {}
   despG = 0
   for pr in palabrasreservadas :
		TSG[pr.upper()] = ['PR']    # No hace falta anadir nada mas a las palabras reservadas

# Esta funcion nos permite CREAR la tabla LOCAL
def ts_crearTablaLocal():
   global Estado
   global despL
   global TSL
   Estado = 'Local'
   despL = 0
   TSL = {}

# Esta funcion nos permite DESTRUIR la tabla GLOBAL
def ts_destruirTablaGlobal():
   global Estado
   global TSG
   global despG
   #print "\nTSG: ", TSG # Modo -Verbose
   Estado = ''   
   TSG = {}
   despG = 0

# Esta funcion nos permite DESTRUIR la tabla LOCAL
def ts_destruirTablaLocal():
   global Estado
   global TSL
   global despL
   #print "\nTSL: ", TSL # Modo -Verbose
   Estado = 'Global'
   despL = 0
   TSL = {}

# Printea el contenido de la TS GLOBAL y tambien lo retorna
def ts_generar_TSG():
    global despG
    txt = '='*30+'\nTABLA DE SIMBOLOS GLOBAL\n'+'='*30+'\n'
    if (ts_NElem_TSG() != 0) :
        for i in range(len(TSG)):
            txt1 = str(TSG.keys()[i])
            txt = txt + txt1
            txt = txt + str(TSG[txt1]) + "\n"
        return txt
    else:
        return txt + 'Destruida'

# Printea el contenido de la TS LOCAL y tambien lo retorna
def ts_generar_TSL():
   txt = '='*30+'\nTABLA DE SIMBOLOS LOCAL\n'+'='*30+'\n'
   if (Estado == 'Local') :
        for i in range(len(TSL)):
            txt1 = str(TSL.keys()[i])
            txt = txt + txt1
            txt = txt + str(TSL[txt1]) + "\n"
        return txt
   else:
     return (txt + 'Destruida')

# Contador para las etiquetas     
global N                 
N=0

# Genera etiquetas para las funciones     
def ts_generar_etiqueta(clave):
    global N
    N += 1
    etq = 'Etq_' + clave + '_' + str(N)
    return etq
       

###****************************************
###  CONTENIDO DE LA TABLA DE SIMBOLOS    
###****************************************
# 
# 'Elemento' - String
# Elemento - Entero 
# [Elemento] - Lista de elem
# ...
#
### Palabra reservada = ['PR']
#
### Entero = ['Tipo', Lugar, ...]
# donde Direccion = Direccion + Ancho
# y ... lo que pueda venir
#
### Vector = ['Tipo', Lugar, Tamano, ...]
# donde Tamano = Num_elems y Direccion = Direccion + Ancho * Tamano
# 
### Funcion = ['Tipo', ['Tipo_params'], 'Etiqueta', tamra]
# donde ['Tipo_param'] es pseudo argv
# etiqueta se genera con una funcion y 'Tipo_retorno' es entero
#
#*******************************************


# Nos permite insertar a la tabla correspondiente unicamente el lexema
def ts_insertar_lexema(clave):
    global Estado
    global TSG
    global TSL
    global despG
    global despL
    if Estado == 'Local' and TSL.get(clave) == None :
       TSL[clave] = ['Unknown']     # La unica informacion comun a vectores, funciones y enteros es el tipo
    elif ts_buscar_lexema(clave) == None :
       TSG[clave] = ['Unknown']
    else:
       error_emitido = 'Error interno al insertar lexema a la Tabla de Simbolos'
       nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
       print (error_emitido)

# Nos permite actualizar el lexema y ademas el campo tipo correspondiente al lexema.
# Inicializamos los contenidos que pueda albergar cada entrada.
def ts_insertar_entrada(clave,tipo):
    global Estado
    global TSG
    global TSL
    if Estado == 'Local' and TSL.get(clave) != None :
        temp = TSL.get(clave)           # Si esta en la tabla local
        temp[0] = tipo
        if tipo == 'entero':            # Puede ser entero
            temp.append(-1)              # Anado el campo de direccion
        elif tipo == 'vector':          # O puede ser vector
            temp.append(-1)              # Anado el campo de direccion
            temp.append(-1)              # Anado el campo de tamano
        TSL[clave] = temp
    elif ts_buscar_lexema(clave) != None:
        temp = TSG.get(clave)           # Si esta en la tabla global
        temp[0] = tipo
        if tipo == 'entero':            # Puede ser entero
            temp.append(-1)              # Anado el campo de direccion
        elif tipo == 'vector':          # Puede ser vector
            temp.append(-1)              # Anado el campo de direccion
            temp.append(-1)              # Anado el campo de tamano
        elif tipo == 'funcion':         # O puede ser funcion
            #temp.append(0)                     # argc
            temp.append([])                    # lista_tipo_arg
            etiqueta = ts_generar_etiqueta(clave) # genero_etq
            temp.append(etiqueta)              # etiqueta
            temp.append(0)                 # tamra
        TSG[clave] = temp
    else:
       error_emitido = 'Error al insertar el tipo. Variable ' + str(clave) + ' no declarada'
       nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
       print (error_emitido)

 
# Nos permite insertar el campo tipo para los vectores
def ts_insertar_tipo(clave,tipo):
    global Estado
    global TSG
    global TSL
    if Estado == 'Local' and TSL.get(clave) != None :
        temp = TSL.get(clave)           # Si esta en la tabla local
        temp[0] = tipo       
    elif ts_buscar_lexema(clave) != None:
        temp = TSG.get(clave)           # Si esta en la tabla global
        temp[0] = tipo
    else:
       error_emitido = 'Error al insertar el tipo. Variable ' + str(clave) + ' no declarada'
       nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
       print (error_emitido)

# Nos permite insertar el campo tamano para los vectores
def ts_insertar_tam(clave,tam):
    global Estado
    global TSG
    global TSL
    if Estado == 'Local' and TSL.get(clave) != None :
        temp = TSL.get(clave)
        tipo = temp[0]
        if tipo == 'vector':
            temp[2] = tam
            TSL[clave] = temp
        else:
           error_emitido = 'Tipo invalido. Solo vectores.'
           nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
           print (error_emitido)
    elif ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        tipo = temp[0]
        if tipo == 'vector':
            temp[2] = tam
            TSG[clave] = temp
        else:
           error_emitido = 'Tipo invalido. Solo vectores.'
           nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
           print (error_emitido)
    else:
        error_emitido = 'Error al insertar el tamano. Variable ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
        print (error_emitido)

# Nos permite insertar el campo direccion correspondiente al lexema
def ts_insertar_dir(clave):
    global Estado
    global TSG
    global TSL
    global despL
    global despG
    global ancho
    global valor
    if Estado == 'Local' and TSL.get(clave) != None :
        temp = TSL.get(clave)
        tipo = temp[0]
        if tipo == 'entero':
            temp[1] = despL                     # Aniado la direccion donde va a estar el entero
            despL = despL + ancho               # Actualizo el desplazamiento
        elif tipo == 'vector':
            tam = temp[2]                       # Obtengo el tamano del vector
            if tam > 0:
                temp[1] = despL                 # Aniado la direccion donde va a estar el vector
                despL = despL + ancho * tam     # Actualizo el desplazamiento
            else:
                error_emitido = 'Error interno: al insertar la direccion del identificador: ' + clave
                nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
                print (error_emitido)

        TSL[clave] = temp
    elif ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        tipo = temp[0]
        if tipo == 'entero':
            temp[1] = despG                     # Aniado la direccion donde va a estar el entero
            despG = despG + ancho               # Actualizo el desplazamiento
            TSG[clave] = temp
        elif tipo == 'vector':
            tam = temp[2]                       # Obtengo el tamano del vector
            if tam > 0:
                temp[1] = despG                 # Aniado la direccion donde va a estar el vector
                despG = despG + ancho * tam     # Actualizo el desplazamiento
                TSG[clave] = temp
        else:
            error_emitido = 'Las funciones no tienen direccion'
            nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
            print (error_emitido)
    else:
        error_emitido = 'Error al insertar la direccion. Variable ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
        print (error_emitido)

# Inserta el numero argumentos de una funcion
def ts_insertar_argc_fun(clave,argc):
    global TSG
    if ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        tipo = temp[0]
        if tipo == 'funcion':
           temp[1] = argc
           TSG[clave] = temp
        else:
           error_emitido = 'Solo las funciones tienen argumentos' 
           nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
           print (error_emitido)
    else:
        error_emitido = 'Error al modificar el numero argumentos. Variable ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
        print (error_emitido)  
  
# Inserta un la lista de tipos de argumentos a la funcion
def ts_insertar_tipo_argc_fun(clave,argv):
    global TSG
    if ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        tipo = temp[0]
        if tipo == 'funcion':
           temp[1] = argv
           TSG[clave] = temp
        else:
           error_emitido = 'Solo las funciones tienen argumentos' 
           nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
           print (error_emitido)  
    else:
        error_emitido = 'Error al modificar la lista de argumentos. Variable ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
        print (error_emitido)  

# Inserta el tipo de retorno de la funcion
def ts_insertar_tipo_ret_fun(clave):
    global TSG
    if ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        tipo = temp[0]
        if tipo == 'funcion':
            argv = temp[1]
            if len(argv) == 1:
                temp[3] = argv[0]
            elif len(argv) > 1:
                for i in range(len(argv) - 1):
                    temp[3] = temp[3] + argv[i] + ' x '
                temp[3] = temp[3] + argv[len(argv) - 1]
            else:
                temp[3] = 'entero'
            TSG[clave] = temp
        else:
            error_emitido = 'Solo las funciones tienen tipo de retorno' 
            nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
            print (error_emitido)  
    else:
        error_emitido = 'Error al modificar la lista de argumentos. Variable ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
        print (error_emitido)  


def ts_insertar_tamra(clave,n):   
    global TSG
    if ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        tipo = temp[0]
        if tipo == 'funcion':
           temp[3] = n
           TSG[clave] = temp
        else:
           error_emitido = 'Solo las funciones tienen tamano de registro de activacion' 
           nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
           print (error_emitido)
    else:
        error_emitido = 'Error al modificar el tamano de registro de activacion. Variable ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
        print (error_emitido)     
        
        
def ts_incrementar_tamra(clave,n):
    global TSG
    if ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        tipo = temp[0]
        if tipo == 'funcion':
           temp[3] = temp[3] + n
           TSG[clave] = temp
        else:
           error_emitido = 'Solo las funciones tienen tamano de registro de activacion' 
           nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
           print (error_emitido)
    else:
        error_emitido = 'Error al modificar el tamano de registro de activacion. Variable ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
        print (error_emitido)     
        
        

# Busca el lexema en alguna de las dos tablas y devuelve su contenido
def ts_buscar_lexema(clave):
    global Estado
    global TSG
    global TSL
    if Estado == 'Local' :
        if TSL.get(clave) == None :
           return TSG.get(clave)
        else:
           return TSL.get(clave)
    else:
        return TSG.get(clave)

# Busca el tipo de una clave
def ts_buscar_tipo(clave):
    global Estado
    global TSG
    global TSL
    if Estado == 'Local' and TSL.get(clave) != None :
       temp = TSL.get(clave)
       return temp[0] 
    elif ts_buscar_lexema(clave) != None :
       temp = TSG.get(clave)
       return temp[0]

def ts_buscar_dir(clave):
    global Estado
    global TSG
    global TSL
    if Estado == 'Local' and TSL.get(clave) != None :
        temp = TSL.get(clave)
        tipo = temp[0]
        if tipo == 'entero' or tipo == 'vector':
            return temp[1]
        elif tipo == 'funcion':
            return temp[2]    
    elif ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        tipo = temp[0]
        if tipo == 'entero' or tipo == 'vector':
            return temp[1]
        elif tipo == 'funcion':
            return temp[2]
    else:
        error_emitido = 'Error al buscar la direccion. Variable ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)


# Busca el tipo de una clave
def ts_buscar_tam(clave):
    global Estado
    global TSG
    global TSL
    if Estado == 'Local' and TSL.get(clave) != None :
        temp = TSL.get(clave)
        tipo = temp[0]
        if tipo == 'vector':
            return temp[2]
        else:
            error_emitido = 'Solo los vectores tienen tamano'
            nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
            print (error_emitido)  
    elif ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        tipo = temp[0]
        if tipo == 'vector':
            return temp[2]
        else:
            error_emitido = 'Solo los vectores tienen tamano'
            nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
            print (error_emitido)
    else:
        error_emitido = 'Error al buscar el tamano. Variable ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
        print (error_emitido)

# Busca la lista de tipos de argumentos a la funcion
def ts_buscar_tipo_argc_fun(clave):
    global TSG
    if ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        return temp[1]
    else:
        error_emitido = 'Error al buscar la lista de argumentos. Funcion ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
        print (error_emitido)  


# Busca el lexema en la tabla local y devuelve su contenido
def ts_buscar_lexema_TSL(clave):
    global TSL
    return TSL.get(clave)
    
def ts_buscar_ts(clave):
    global Estado
    global TSG
    global TSL
    if TSL.get(clave) != None:
        return "TSL"
    elif TSG.get(clave) != None:
        return "TSG"
    else:
        return None

# Busca el campo etiquetea de una funcion
def ts_buscar_etq(clave):
    global TSG
    if ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        return temp[2]
    else:
        error_emitido = 'Error al buscar la etiqueta. Funcion ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
        print (error_emitido)  
        
        
# Busca el tamano del registro de activacion segun una variable
def ts_buscar_tamra(clave):
    global TSG
    if ts_buscar_lexema(clave) != None :
        temp = TSG.get(clave)
        return temp[3]
    else:
        error_emitido = 'Error al buscar el tamano de RA. Funcion ' + str(clave) + ' no declarada'
        nuevo_error_interno('-','Tabla_Simbolos',error_emitido)
        print (error_emitido)  


def ts_tamano_ra(tabla):
    global despG
    global despL
    if tabla == "l":
        return despL
    elif tabla == "g":
        return despG
 
    