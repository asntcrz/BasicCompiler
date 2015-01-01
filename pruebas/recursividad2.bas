def multiplicacionR(n,m,k)
    if n = 0 then let multiplicacionR = 0
    if n = 1 then let multiplicacionR = m
    if n>1 then let multiplicacionR = multiplicacionR(n-1,m+k,k)
    let a = 5
    let b = 9
end def

def suma(n,m)
    if n = 1 then let suma = m
    if n> 1 then let suma =4
end def

print "introduce op1"
input a
print "introduce op2"
input c

print "el resultado de la operacion recurisva es"
print multiplicacionR(a,c,c)

end