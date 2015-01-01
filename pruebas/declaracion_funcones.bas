def fun0
    print "funcion 0"
    let fun0 = 99
end def

def fun1 (a)
    print "1 argumento"
    print "introduce un numero"
    input fun1
end def

def fun2(d,f)
    print "2 argumentos"
    let fun2 = d + f
end def

dim v(10)

print "    llamada a fun0    "
let a = fun0
print fun0

print "    llamada a fun2    "
print fun2(4,5)

print "   llamada a fun1    "
let  b = fun1(v(9))


end