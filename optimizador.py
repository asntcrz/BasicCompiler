from os import rename, remove
from sys import *
from gco import *
from tablasimbolos import *

def crea_linea(n,k):
    aux = ""
    for i in range(n):
        if k == "push":
            aux = aux + "\t\tPUSH #0\n"
        elif k == "pop":
            aux = aux + "\t\tPOP .R8\n" 
    return aux

def optimizador_codigo():
    global lista_call                       # tiene la lista de las funciones llamadas
    aux = []
    m = 0
    fd_in = open ("CodigoEns.ens","r") 
    fd_out = open ("faux","w") 
    n = ts_tamano_ra("g")                   # devuelve el numero de push que hay que meter
    reemplazo = "main: NOP\n" + crea_linea(n+1,"push")
    for line in fd_in.readlines():
        if line[0:4] == "Etq_" and "while" not in line and "if" not in line and "equ" not in line and "EQU" not in line and "DATA" not in line:     # Si empieza por etiqueta Etq_ casi siempre sera funcion
            lex = re.split("[_]",line[0:-2])
            lexema_fun = lex[1]
            if line[0:-2] in lista_call:    # Si miramos los caracteres Etq_FUN_1 y ha sido llamada por alguien
                aux = aux + [line[0:-2]]    # Apilo la funcion, ahora comprobare los calls que recibo con la cima de la pila
                m = ts_buscar_tamra(lexema_fun) # Y obtengo el numero de pushes y pops que deberia de haber
        if "PUSH" in line:
            m -= 1                              # Siempre que encuentre push resto uno al contador
        if "RET" in line:
            if aux != []:
                aux.pop()                        # si hay un retorno, desapilo la funcion
        if "CALL /" in line:                    # Si recibo una llamada 
            if aux != []:                       # y estoy dentro de una funcion
                if line[8:-1] == aux[-1]:       # Compruebo si la llamada es recursiva, preguntando si algun call tiene la etiqueta
                    aver = crea_linea(m,"push") + line + crea_linea(m,"pop")
                    escribe = line.replace(line,aver)
                    fd_out.write(escribe)
                    line = fd_in.read()
                else:                               # Si no era mi funcion reinicio el contador
                    m = ts_buscar_tamra(lexema_fun)
        newline = line.replace("main: NOP",reemplazo)   # Arreglamos el main
        fd_out.write(newline)
    fd_out.close()
    fd_in.close()
    remove("CodigoEns.ens")
    rename("faux", "CodigoEns.ens")