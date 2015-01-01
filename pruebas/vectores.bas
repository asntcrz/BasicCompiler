def funvect(t(4))
  dim a(4)
    print t(1)
    print t(2)
    let a = t
    let t(1) = t(3)
    print t(1)
    print t(2)
end def

def funvect2(t(4),x(4))
    dim a(4)
    let a = t
    print x(1)
    let t(1) = t(3)
    print t(1)
    print t(2)
    let x(3) = t (4)
    print x(3)
end def

dim v(4)
dim g(4)
rem let n = 9
rem let g(4) = n

let n = 0
let g(n) = 9
rem while 5 > n
   rem  let g(n) = 9
    let n = n + 1
rem wend

print "introduce un 1, un 2, un 3 y un 4 por favor"
input v(1)
print v(1)
input v(2)
print v(2)
input v(3)
print v(3)
input v(4)
print v(4)

while 5 > n
   let g(n) = 9
   print n
    print g(n)
    let n = n + 1
wend

let v(1) = v(2) + v(3)
rem  let v(1) = 5
rem print "ahora v(1) vale:"
print v(1)

print funvect2(v,g)
print funvect(v)
end