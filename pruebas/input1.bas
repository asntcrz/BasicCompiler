dim v(8)
print "introduce un numero"
input a  : rem 4
print "introduce un numero menor que el anterior"
input v(2) : rem menor que a

while a > v(2)
    let a = a + (-1)
    input v(3)
    print v(3)
    print "el valor de a es :  "
    print a
wend


end