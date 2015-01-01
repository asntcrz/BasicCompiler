import os
import re
import gci
import tablasimbolos as ts
f = open("CodigoEns.ens", "w") #, encoding="utf-8")  # mode = a
f.close()

global estadomaquina
estadomaquina = 1
global lista_cadenas
lista_cadenas = []
global lista_equs
lista_equs = []
global tam_fun
tam_fun = "ERROR"
global lista_w
lista_w = []
global lista_call
lista_call = []

def GenerarCO (cuarteto, fd):
    f = open("CodigoEns.ens", "a")
    global lista_cadenas
    global lista_equs
    global tam_fun
    op1 = gci.DarOperando1(cuarteto)
    op2 = gci.DarOperando2(cuarteto)
    res = gci.DarResultado(cuarteto)

    if gci.DarOperador(cuarteto) == 'INICIO':
        gci.EscribirCuarteto(fd,cuarteto)
        f.write("\t\tORG 0\n")
        f.write("\t\tMOVE .SP, .R9\n")
        f.write("\t\tBR /main\n")

    if gci.DarOperador(cuarteto) == 'Main':
        gci.EscribirCuarteto(fd,cuarteto)
        f.write("main: NOP\n")  
        
    if  gci.DarOperador(cuarteto) == 'DEF':
        gci.EscribirCuarteto(fd,cuarteto)
        tam_fun = op1
        tam_fun = tam_fun[0:-2]
        f.write(op1+":\n")
        f.write("\t\t NOP\n")
        
    if  gci.DarOperador(cuarteto) == 'fin':
        gci.EscribirCuarteto(fd,cuarteto)    
        f.write("\t\tHALT\n\n")
        
    if  gci.DarOperador(cuarteto) == 'EndDEF':
        gci.EscribirCuarteto(fd,cuarteto)
        f.write("\t\tRET\n\n")
        tam = ts.ts_tamano_ra("l") + estadomaquina
        lista_equs.append((tam_fun,tam))
        


    if  gci.DarOperador(cuarteto) == 'Asignacion':
        gci.EscribirCuarteto(fd,cuarteto)
        # op1 = origen
        # op2 = None si entero || dimension si vector || id si direccionamiento relativo (para let)
        # res = destino
        f.write("; Asignacion\n")
        if op1[1] == 'inm':
            if res[1] == 'dir':
                entradares = ts.ts_buscar_lexema(res[0])
                lugarres = entradares[1]
                if ts.ts_buscar_ts(res[0]) == "TSL":
                    f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
                    f.write("\t\tMOVE .A, .IY\n")
                elif ts.ts_buscar_ts(res[0]) == "TSG":         
                    f.write("\t\tMOVE .R9, .IY\n")
                f.write("\t\tMOVE " + '#' + str(op1[0]) + ", " + '#-' + str(lugarres) + "[.IY]\n")
                #f.write("\n")
            else:
                print "ERROR 1"

        elif op1[1] == 'dir':
            if res[1] == 'dir':
                entradaop1 = ts.ts_buscar_lexema(op1[0])
                lugarop1 = entradaop1[1]
                entradares = ts.ts_buscar_lexema(res[0])
                lugarres = entradares[1]
                if op2 == None:
                    i = 1
                else:
                    i = op2
                for k in range(i):
                    if ts.ts_buscar_ts(op1[0]) == "TSL":
                        f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
                        f.write("\t\tMOVE .A, .IX\n") 
                    elif ts.ts_buscar_ts(op1[0]) == "TSG":         
                        f.write("\t\tMOVE .R9, .IX\n")
                    if ts.ts_buscar_ts(res[0]) == "TSL":
                        f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
                        f.write("\t\tMOVE .A, .IY\n")
                    elif ts.ts_buscar_ts(res[0]) == "TSG":         
                        f.write("\t\tMOVE .R9, .IY\n")
                        
                    f.write("\t\tMOVE " + "#-" + str(lugarop1+k) + "[.IX], " + "#-" + str(lugarres+k) + "[.IY]\n")
                    #f.write("\n")
            elif res[1] == 'rel':
                # op1 = origen
                # op2 = acceso_vector
                # res = lugar res
                entradaop1 = ts.ts_buscar_lexema(op1[0])
                lugarop1 = entradaop1[1]
                lugarid = ts.ts_buscar_dir(op2)
                entradares = ts.ts_buscar_lexema(res[0])
                lugarres = entradares[1]

                if ts.ts_buscar_ts(op1[0]) == "TSL":
                    f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
                    f.write("\t\tMOVE .A, .IX\n") 
                elif ts.ts_buscar_ts(op1[0]) == "TSG":         
                    f.write("\t\tMOVE .R9, .IX\n")
                    
                if ts.ts_buscar_ts(op2) == "TSL":
                    f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
                    f.write("\t\tSUB .A, #"  + str(lugarid) + "\n")
                    f.write("\t\tMOVE .A, .IY\n")
                elif ts.ts_buscar_ts(op2) == "TSG":         
                    f.write("\t\tMOVE .R9, .IY\n")
                    f.write("\t\tSUB .IY, #"  + str(lugarid) + "\n")
                    f.write("\t\tMOVE .A, .IY\n")

                f.write("\t\tMOVE [.IY], .R8\n")

                if ts.ts_buscar_ts(res[0]) == "TSL":
                    f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
                    f.write("\t\tSUB .A, #"  + str(lugarres) + "\n")
                    f.write("\t\tMOVE .A, .IY\n")
                elif ts.ts_buscar_ts(res[0]) == "TSG":         
                    f.write("\t\tMOVE .R9, .IY\n")
                    f.write("\t\tSUB .IY, #"  + str(lugarres) + "\n")
                    f.write("\t\tMOVE .A, .IY\n")
                
                f.write("\t\tSUB .IY, .R8\n")
                f.write("\t\tMOVE .A, .IY\n")
                
                f.write("\t\tMOVE " + "#-" + str(lugarop1) + "[.IX],  [.IY]\n")
                #f.write("\n")
            else:
                print "ERROR 2"



    if  gci.DarOperador(cuarteto) == 'GenerarCadena':
        gci.EscribirCuarteto(fd,cuarteto)
        lista_cadenas.append((op1,op2))

    if gci.DarOperador(cuarteto) == 'Datos':
        gci.EscribirCuarteto(fd,cuarteto)
        f.write("; Imprimimos los datos y etiquetas\n")
        for i in range(len(lista_cadenas)):
            op1 = lista_cadenas[i][0]
            op2 = lista_cadenas[i][1]
            op2 = op2.strip('&')
            f.write('{0}: DATA {1}'.format(op2,op1) + '\n')
        for i in range(len(lista_equs)):
            op1 = lista_equs[i][0]
            op2 = lista_equs[i][1]
            f.write('{0}: EQU {1}'.format(op1,op2) + '\n')
        #f.write("\n")
        
    if  gci.DarOperador(cuarteto) == 'LLAM_FUN':
        gci.EscribirCuarteto(fd,cuarteto)
        contpushes = 0
        # op1 = Etq_fun1
        # op2 = parametros - lista de lugares
        # res = destino 
        f.write("; Llamada a funcion\n")
        res = res[0]
        f.write("\t\tMOVE .SP, .R4\n")      # R4 puntero a marco de pila
        f.write("\t\tPUSH #0\n")
        contpushes += 1
        op2.reverse()
        for i in op2:
            offset = ts.ts_buscar_dir(i)
            if ts.ts_buscar_tipo(i) == 'entero':
                if ts.ts_buscar_ts(i) == "TSL":
                    f.write("\t\tADD .R4, #" + str(tam_fun) + "\n")
                    f.write("\t\tMOVE .A, .IY\n")
                    f.write("\t\tPUSH " + '#-' + str(offset) + "[.IY]\n")
                    contpushes += 1
                elif ts.ts_buscar_ts(i) == "TSG":         
                    f.write("\t\tMOVE .R9, .IY\n")
                    f.write("\t\tPUSH " + '#-' + str(offset) + "[.IY]\n")
                    contpushes += 1
            elif ts.ts_buscar_tipo(i) == 'vector':
                tam = ts.ts_buscar_tam(i)
                for j in range(tam):
                    if ts.ts_buscar_ts(i) == "TSL":
                        f.write("\t\tADD .R4, #" + str(tam_fun) + "\n")
                        f.write("\t\tMOVE .A, .IY\n")
                        f.write("\t\tPUSH " + '#-' + str(offset+j) + "[.IY]\n")
                        contpushes += 1                         
                    elif ts.ts_buscar_ts(i) == "TSG":         
                        f.write("\t\tMOVE .R9, .IY\n")
                        f.write("\t\tPUSH " + '#-' + str(offset+j) + "[.IY]\n")
                        contpushes += 1

        lxlx = re.split("[_]",op1)
        lexema_fun = lxlx[1]
        for k in range(ts.ts_buscar_tamra(lexema_fun)-contpushes):
            f.write("\t\tPUSH #0\n")
        f.write("\t\tCALL /" + str(op1) + "\n")
        for k in range(ts.ts_buscar_tamra(lexema_fun)):
            f.write("\t\tPOP .R8\n")                # R8 ES PARA LOS POPS!!!!!!!!!!!!!!

        if str(op1) not in lista_call:
            lista_call.append(str(op1))

        offset = ts.ts_buscar_dir(res)
        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
            f.write("\t\tMOVE .R8, " + '#-' + str(offset) + "[.IY]\n")                       
        elif ts.ts_buscar_ts(res) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")
            f.write("\t\tMOVE .R8, " + '#-' + str(offset) + "[.IY]\n")
        #f.write("\n")
        
    if gci.DarOperador(cuarteto) == 'LLAM_VECTOR':
        gci.EscribirCuarteto(fd,cuarteto)
        # op1 = lugar_index
        # op2 = lexema_id
        # res = destino
        f.write("; Accediendo a vector\n")
        offset1 = ts.ts_buscar_dir(op1)
        offset2 = ts.ts_buscar_dir(op2)
        offset3 = ts.ts_buscar_dir(res)
        
        if ts.ts_buscar_ts(op1) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offset1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(offset1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")

        if ts.ts_buscar_ts(op2) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offset2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(op2) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")
            f.write("\t\tSUB .IY, #" + str(offset2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")

        f.write("\t\tSUB .IY, [.IX]\n")
        f.write("\t\tMOVE .A, .IX\n")
        
        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offset3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
            
        elif ts.ts_buscar_ts(res) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")       
            f.write("\t\tSUB .IY, #" + str(offset3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")       
        
        f.write("\t\tMOVE [.IX], [.IY]\n")

        
    if gci.DarOperador(cuarteto) == 'MENOS_UNARIO':
        gci.EscribirCuarteto(fd,cuarteto)
        # op1 = lugar de H
        # op2 = None
        # res = destino
        f.write("; Calculando el menos unario\n")
        offsetop1 = ts.ts_buscar_dir(op1)
        offsetres = ts.ts_buscar_dir(res)
        
        if ts.ts_buscar_ts(op1) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetop1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(offsetop1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetres) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(res) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")       
            f.write("\t\tSUB .IY, #" + str(offsetres) + "\n")
            f.write("\t\tMOVE .A, .IY\n")   
        
        f.write("\t\tSUB #0, [.IX]\n")
        f.write("\t\tMOVE .A, [.IY]\n")
        #f.write("\n")
        
    if gci.DarOperador(cuarteto) == 'Print_Ent':
        gci.EscribirCuarteto(fd,cuarteto)
        # op1 = offset de entero
        # op2 = lexema
        f.write("; Imprime entero\n")
        lugar = op1
        if ts.ts_buscar_ts(op2) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op2) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            
        f.write("\t\tWRINT #-" + str(lugar) + "[.IX] \n")
        #f.write("\n")
        
    if gci.DarOperador(cuarteto) == 'Print_Cad':
        gci.EscribirCuarteto(fd,cuarteto)
        # op1 = lugar de cadena
        f.write("; Imprime cadena\n")
        lugar = op1.strip('&')
        f.write("\t\tWRSTR /" + str(lugar) + "\n")
        #f.write("\n")
        

    if gci.DarOperador(cuarteto) == 'OPEROR':
        gci.EscribirCuarteto(fd,cuarteto)     
        # op1[0] = lugar Exp
        # op2[0] = lugar _Exp
        # res = temporal       
        f.write("; Operacion AND\n")
        offsop1 = ts.ts_buscar_dir(op1[0])
        offsop2 = ts.ts_buscar_dir(op2[0])
        offsre3 = ts.ts_buscar_dir(res)

        if ts.ts_buscar_ts(op1[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsop1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(offsop1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        if ts.ts_buscar_ts(op2[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsop2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(op2[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")
            f.write("\t\tSUB .IY, #" + str(offsop2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
            
        # Acceder al primer operando y evaluar
        f.write("\t\tMOVE [.IX], .R5\n")
        f.write("\t\tADD #1, .R5\n")
        f.write("\t\tBZ $5\n")          # Si el resultado da 0, es que era 1
        f.write("\t\tMOVE #0, .R5\n")   # Dejo un 0 como False apuntando en el registro temporal
        f.write("\t\tBR $3\n")
        f.write("\t\tMOVE #-1, .R5\n")     # Dejo un 1 como True apuntando en el registro temporal
        
        # Acceder al segundo operando y evaluar
        f.write("\t\tMOVE [.IY], .R6\n")
        f.write("\t\tADD #1, .R6\n")
        f.write("\t\tBZ $5\n")          # Si el resultado da 0, es que era 1
        f.write("\t\tMOVE #0, .R6\n")   # Dejo un 0 como False apuntando en el registro temporal
        f.write("\t\tBR $3\n")
        f.write("\t\tMOVE #-1, .R6\n")     # Dejo un 1 como True apuntando en el registro temporal       

        # Hago el OR sobre los registros
        f.write("\t\tOR .R5, .R6\n")   # Lugar de op1 AND lugar de op2
        f.write("\t\tCMP .A, #0\n")     # Comparo el .A (resultado de and) contra
        f.write("\t\tBZ $5\n")          # Si el resultado da 0, es que era 1
        f.write("\t\tMOVE #-1, .R8\n")  # Dejo un -1 como True apuntando en el registro temporal
        f.write("\t\tBR $3\n")
        f.write("\t\tMOVE #0, .R8\n")   # Dejo un 0 como False apuntando en el registro temporal

        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsre3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(res) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")       
            f.write("\t\tSUB .IY, #" + str(offsre3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")       
        f.write("\t\tMOVE .R8, [.IY]\t;\tCargo el contenido de .R8(0 si False, 1 si True) en donde apunte .IY\n")
        #f.write("\n")

        
        
    if gci.DarOperador(cuarteto) == 'OPERAND':
        gci.EscribirCuarteto(fd,cuarteto)     
        # op1[0] = lugar Exp
        # op2[0] = lugar _Exp
        # res = temporal
        f.write("; Operacion AND\n")
        offsop1 = ts.ts_buscar_dir(op1[0])
        offsop2 = ts.ts_buscar_dir(op2[0])
        offsre3 = ts.ts_buscar_dir(res)

        if ts.ts_buscar_ts(op1[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsop1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(offsop1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        if ts.ts_buscar_ts(op2[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsop2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(op2[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")
            f.write("\t\tSUB .IY, #" + str(offsop2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        
        # Acceder al primer operando y evaluar
        f.write("\t\tMOVE [.IX], .R5\n")
        f.write("\t\tADD #1, .R5\n")
        f.write("\t\tBZ $5\n")          # Si el resultado da 0, es que era 1
        f.write("\t\tMOVE #0, .R5\n")   # Dejo un 0 como False apuntando en el registro temporal
        f.write("\t\tBR $3\n")
        f.write("\t\tMOVE #-1, .R5\n")     # Dejo un 1 como True apuntando en el registro temporal
        
        # Acceder al segundo operando y evaluar
        f.write("\t\tMOVE [.IY], .R6\n")
        f.write("\t\tADD #1, .R6\n")
        f.write("\t\tBZ $5\n")          # Si el resultado da 0, es que era 1
        f.write("\t\tMOVE #0, .R6\n")   # Dejo un 0 como False apuntando en el registro temporal
        f.write("\t\tBR $3\n")
        f.write("\t\tMOVE #-1, .R6\n")     # Dejo un 1 como True apuntando en el registro temporal      

        # Hago el AND sobre los registros
        f.write("\t\tAND .R5, .R6\n")   # Lugar de op1 AND lugar de op2
        f.write("\t\tCMP .A, #0\n")     # Comparo el .A (resultado de and) contra
        f.write("\t\tBZ $5\n")          # Si el resultado da 0, es que era 1
        f.write("\t\tMOVE #-1, .R8\n")  # Dejo un -1 como True apuntando en el registro temporal
        f.write("\t\tBR $3\n")
        f.write("\t\tMOVE #0, .R8\n")   # Dejo un 0 como False apuntando en el registro temporal
        
        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsre3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(res) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")       
            f.write("\t\tSUB .IY, #" + str(offsre3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")       
        f.write("\t\tMOVE .R8, [.IY]\t;\tCargo el contenido de .R8(0 si False, 1 si True) en donde apunte .IY\n")
        #f.write("\n")

    if gci.DarOperador(cuarteto) == 'DISTINTO':
        gci.EscribirCuarteto(fd,cuarteto)     
        # op1[0] = lugar F
        # op2[0] = lugar _F
        # res = temporal
        f.write("; Operacion Distinto\n")
        offsetoper1 = ts.ts_buscar_dir(op1[0])
        offsetoper2 = ts.ts_buscar_dir(op2[0])
        offsetres3 = ts.ts_buscar_dir(res)
        
        if ts.ts_buscar_ts(op1[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetoper1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(offsetoper1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        if ts.ts_buscar_ts(op2[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetoper2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(op2[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")
            f.write("\t\tSUB .IY, #" + str(offsetoper2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        f.write("\t\tSUB [.IX], [.IY]\n")
        f.write("\t\tBZ $5\n")          # Si el resultado es cero es que son iguales, asique salto indicando q distintos = FALSE
        f.write("\t\tMOVE #-1, .R8\n")  # Dejo un -1 como True apuntando en el registro temporal
        f.write("\t\tBR $3\n")
        f.write("\t\tMOVE #0, .R8\n")   # Dejo un 0 como False apuntando en el registro temporal
        
        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetres3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(res) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")       
            f.write("\t\tSUB .IY, #" + str(offsetres3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")       
        f.write("\t\tMOVE .R8, [.IY]\t;\t Cargo el contenido de .R8(0 si False, 1 si True) en donde apunte .IY\n")
        #f.write("\n")

        
    if gci.DarOperador(cuarteto) == 'IGUAL':
        gci.EscribirCuarteto(fd,cuarteto)     
        # op1[0] = lugar F
        # op2[0] = lugar _F
        # res = temporal
        f.write("; Operacion Igual\n")
        offsetoper1 = ts.ts_buscar_dir(op1[0])
        offsetoper2 = ts.ts_buscar_dir(op2[0])
        offsetres3 = ts.ts_buscar_dir(res)
        
        if ts.ts_buscar_ts(op1[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetoper1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(offsetoper1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        if ts.ts_buscar_ts(op2[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetoper2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(op2[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")
            f.write("\t\tSUB .IY, #" + str(offsetoper2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        f.write("\t\tSUB [.IX], [.IY]\n")
        f.write("\t\tBZ $5\n")          # Si el resultado es cero es que son iguales, asique salto indicando q Iguales = TRUE
        f.write("\t\tMOVE #0, .R8\n")   # Dejo un 0 como False apuntando en el registro temporal
        f.write("\t\tBR $3\n")
        f.write("\t\tMOVE #-1, .R8\n")  # Dejo un -1 como True apuntando en el registro temporal
        
        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetres3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(res) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")       
            f.write("\t\tSUB .IY, #" + str(offsetres3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")       
        f.write("\t\tMOVE .R8, [.IY]\t;\t Cargo el contenido de .R8(0 si False, 1 si True) en donde apunte .IY\n")
        #f.write("\n")

        
    if gci.DarOperador(cuarteto) == 'MAYOR':
        gci.EscribirCuarteto(fd,cuarteto)     
        # op1[0] = lugar F
        # op2[0] = lugar _F
        # res = temporal
        f.write("; Operacion Mayor\n")
        offsetoper1 = ts.ts_buscar_dir(op1[0])
        offsetoper2 = ts.ts_buscar_dir(op2[0])
        offsetres3 = ts.ts_buscar_dir(res)
        
        if ts.ts_buscar_ts(op1[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetoper1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(offsetoper1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        if ts.ts_buscar_ts(op2[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetoper2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(op2[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")
            f.write("\t\tSUB .IY, #" + str(offsetoper2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")

        f.write("\t\tSUB [.IX], [.IY]\n")
        f.write("\t\tBZ $2\n")          # Si el resultado es cero, no es mayor, salto indicando mayor = FALSE
        f.write("\t\tBP $5\n")          # Si el resultado es positivo(S=0) es que a mayor b = TRUE
        f.write("\t\tMOVE #0, .R8\n")   # Dejo un 0 como False apuntando en el registro temporal
        f.write("\t\tBR $3\n")
        f.write("\t\tMOVE #-1, .R8\n")  # Dejo un -1 como True apuntando en el registro temporal
        
        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetres3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(res) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")       
            f.write("\t\tSUB .IY, #" + str(offsetres3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")       
        f.write("\t\tMOVE .R8, [.IY]\t;\t Cargo el contenido de .R8(0 si False, 1 si True) en donde apunte .IY\n")
        #f.write("\n")
        
    if gci.DarOperador(cuarteto) == 'MENOR':
        gci.EscribirCuarteto(fd,cuarteto)     
        # op1[0] = lugar F
        # op2[0] = lugar _F
        # res = temporal
        f.write("; Operacion Menor\n")
        offsetoper1 = ts.ts_buscar_dir(op1[0])
        offsetoper2 = ts.ts_buscar_dir(op2[0])
        offsetres3 = ts.ts_buscar_dir(res)
        if ts.ts_buscar_ts(op1[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetoper1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(offsetoper1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        if ts.ts_buscar_ts(op2[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetoper2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(op2[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")
            f.write("\t\tSUB .IY, #" + str(offsetoper2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        f.write("\t\tSUB [.IX], [.IY]\n")
        f.write("\t\tBZ $2\n")          # Si el resultado es cero, no es menor, salto indicando menor = FALSE
        f.write("\t\tBN $5\n")          # Si el resultado es negativo(S=1) es que a menor b = TRUE
        f.write("\t\tMOVE #0, .R8\n")   # Dejo un 0 como False apuntando en el registro temporal
        f.write("\t\tBR $3\n")
        f.write("\t\tMOVE #-1, .R8\n")  # Dejo un -1 como True apuntando en el registro temporal
        
        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetres3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(res) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")       
            f.write("\t\tSUB .IY, #" + str(offsetres3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")       
        f.write("\t\tMOVE .R8, [.IY]\t;\t Cargo el contenido de .R8(0 si False, 1 si True) en donde apunte .IY\n")
        #f.write("\n")    
        

    if gci.DarOperador(cuarteto) == 'SUMA':
        gci.EscribirCuarteto(fd,cuarteto)     
        # op1[0] = lugar G
        # op2[0] = lugar _G
        # res = temporal
        f.write("; Operacion Suma\n")
        offseto1 = ts.ts_buscar_dir(op1[0])
        offseto2 = ts.ts_buscar_dir(op2[0])
        offsetr3 = ts.ts_buscar_dir(res)
        
        if ts.ts_buscar_ts(op1[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offseto1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(offseto1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        if ts.ts_buscar_ts(op2[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offseto2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(op2[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")
            f.write("\t\tSUB .IY, #" + str(offseto2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        f.write("\t\tADD [.IX], [.IY]\t;\t Lugar de op1 + lugar de op2\n")
        f.write("\t\tMOVE .A, .R8\n")
        
        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetr3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(res) == "TSG":
            f.write("\t\tMOVE .R9, .IY\n")       
            f.write("\t\tSUB .IY, #" + str(offsetr3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
            
        f.write("\t\tMOVE .R8, [.IY]\t;\t Cargo el acumulador a+b en donde apunte .IY\n")
        #f.write("\n")

    if gci.DarOperador(cuarteto) == 'RESTA':
        gci.EscribirCuarteto(fd,cuarteto)     
        # op1[0] = lugar G
        # op2[0] = lugar _G
        # res = temporal
        f.write("; Operacion Resta\n")
        offseto1 = ts.ts_buscar_dir(op1[0])
        offseto2 = ts.ts_buscar_dir(op2[0])
        offsetr3 = ts.ts_buscar_dir(res)
        
        if ts.ts_buscar_ts(op1[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offseto1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(offseto1) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        if ts.ts_buscar_ts(op2[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offseto2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(op2[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")
            f.write("\t\tSUB .IY, #" + str(offseto2) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
            
        f.write("\t\tSUB [.IX], [.IY]\t;\t Lugar de op1 - lugar de op2\n")
        f.write("\t\tMOVE .A, .R8\n")

        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(offsetr3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(res) == "TSG":
            f.write("\t\tMOVE .R9, .IY\n")       
            f.write("\t\tSUB .IY, #" + str(offsetr3) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
            
        f.write("\t\tMOVE .R8, [.IY]\t;\t Cargo el acumulador a+b en donde apunte .IY\n")
        #f.write("\n")


        
    if gci.DarOperador(cuarteto) == 'IniWhile':
        global lista_w
        gci.EscribirCuarteto(fd,cuarteto)
        et_while = ts.ts_generar_etiqueta("while")
        lista_w.append(et_while)
        f.write(et_while+":\n")
        f.write("\t\t NOP\n")

        
    if gci.DarOperador(cuarteto) == 'EVALEXPw':
        gci.EscribirCuarteto(fd,cuarteto)
        # op1 = lugar exp
        ofsetExp = ts.ts_buscar_dir(op1[0])
        final = lista_w[-1]+"_fin"
        
        if ts.ts_buscar_ts(op1[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(ofsetExp) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(ofsetExp) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
            
        f.write("\t\tMOVE [.IX], .R5\n")
        f.write("\t\tADD #1, .R5\n")
        #f.write("\t\tMOVE .A, .R5\n")
        f.write("\t\tBNZ /" + str(final) + "\n")


    if gci.DarOperador(cuarteto) == 'FinWhile':
        gci.EscribirCuarteto(fd,cuarteto)
        ini = lista_w[-1]
        f.write("\t\tBR /" + str(ini) + "\n")
        et_while = lista_w.pop()
        f.write(et_while+"_fin:\n")
        f.write("\t\t NOP\n")

        
    if gci.DarOperador(cuarteto) == 'EVALEXPif':
        gci.EscribirCuarteto(fd,cuarteto)
        # op1 = lugar exp
        ofsetExp = ts.ts_buscar_dir(op1[0])
        
        et_while = ts.ts_generar_etiqueta("fin_if")
        lista_w.append(et_while)
        final = lista_w[-1]
        
        if ts.ts_buscar_ts(op1[0]) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #" + str(ofsetExp) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
        elif ts.ts_buscar_ts(op1[0]) == "TSG":         
            f.write("\t\tMOVE .R9, .IX\n")
            f.write("\t\tSUB .IX, #" + str(ofsetExp) + "\n")
            f.write("\t\tMOVE .A, .IX\n")
            
        f.write("\t\tMOVE [.IX], .R5\n")
        f.write("\t\tADD #1, .R5\n")
        #f.write("\t\tMOVE .A, .R5\n")
        f.write("\t\tBNZ /" + str(final) + "\n")        
  
    if gci.DarOperador(cuarteto) == 'Fin_if':
        gci.EscribirCuarteto(fd,cuarteto)
        et_if = lista_w.pop()
        f.write(et_if+":\n") 
        f.write("\t\t NOP\n")


    if gci.DarOperador(cuarteto) == 'INPUT':
        gci.EscribirCuarteto(fd,cuarteto)
        # op1 = lugar de Z
        # op2 = None
        # res = lugar de id
        f.write("; Input\n")
        ofsetres = ts.ts_buscar_dir(res)
        
        if ts.ts_buscar_ts(res) == "TSL":
            f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
            f.write("\t\tSUB .A, #"  + str(ofsetres) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        elif ts.ts_buscar_ts(res) == "TSG":         
            f.write("\t\tMOVE .R9, .IY\n")
            f.write("\t\tSUB .IY, #"  + str(ofsetres) + "\n")
            f.write("\t\tMOVE .A, .IY\n")
        
        if op1 != None:
            ofsetop1 = ts.ts_buscar_dir(op1[0])
            if ts.ts_buscar_ts(op1[0]) == "TSL":
                f.write("\t\tADD .SP, #" + str(tam_fun) + "\n")
                f.write("\t\tSUB .A, #" + str(ofsetop1) + "\n")
                f.write("\t\tMOVE .A, .IX\n")
            elif ts.ts_buscar_ts(op1[0]) == "TSG":         
                f.write("\t\tMOVE .R9, .IX\n")
                f.write("\t\tSUB .IX, #" + str(ofsetop1) + "\n")
                f.write("\t\tMOVE .A, .IX\n")
                
            f.write("\t\tSUB .IY, [.IX]\n")
            f.write("\t\tMOVE .A, .IY\n")
            f.write("\t\tININT [.IY]\n")    
        else:
            f.write("\t\tININT [.IY]\n")


    f.close()
            