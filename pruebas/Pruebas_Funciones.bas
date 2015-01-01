def fun0
    static v0
    print "0"
end def

def fun1(pf1)
    static v1
    print "1"
end def

def fun2(pf1,pf2)
    static v2, v3
    print "2"
end def

dim vec(15)
dim vec0(20)

rem LLAMADAS A FUNCION CON CERO ARGUMENTOS***************************
rem CORRECTAS------------------
let a0 = fun0
let b0 = fun0 + 1
let c0 = fun0 + vec(1)
let d0 = 13 + fun0
let e0 = vec(fun0)
let f0 = vec(fun0 + 2)
let g0 = fun0 + a
let h0 = (fun0 + b + a)

rem INCORRECTAS----------------
rem let z0 = fun0(1)
rem let y0 = fun0(a)
rem let x0 = fun0(vec(1))
rem let w0 = fun0(vec(a))
rem let v0 = a + fun0(a)
rem let u0 = fun0(a+1,b+3)

rem LLAMADAS A FUNCION CON UN ARGUMENTO *****************************
rem CORRECTAS------------------
let a1 = fun1(0)
let a1 = fun1(a)
let b1 = fun1(a + 1)
let c1 = fun1(2 + vec(1))
let d1 = fun1(a + vec(1))
let e1 = vec(fun1(vec(1)))
let f1 = vec(fun1(vec(fun1(a))) + 2)
let g1 = fun1((vec(2)) + a)
let h1 = fun1(fun1(a + b))

rem INCORRECTAS----------------
rem let z1 = fun1
rem let y1 = fun1(1,2)
rem let y1 = fun1(a,b)
rem let y1 = fun1(1,c)
rem let x1 = fun1(vec(1),vec(2))
rem let w1 = fun1(vec(a),vec(2))
rem let v1 = fun1(a + fun1(a),fun1(a))
rem let u1 = fun1(a+1,b+3)

rem LLAMADAS A FUNCION CON DOS ARGUMENTOS****************************
rem CORRECTAS------------------
let a2 = fun2(1,2) + fun2(a,1) + fun2(1,b) + fun2(a,b)
let b2 = fun2(fun2(fun1(a),fun0),fun2(fun2(fun0,fun0),fun1(fun0)))
let c2 = fun2(a + vec(1), vec(8))
let d2 = 13 + fun2(vec(8),fun1(fun2(fun1(vec(8)),fun0)))
let e2 = fun1(vec(fun2(fun0,fun2(a,fun1(vec(8))))))
let f2 = vec(fun2(a + 2,v))
let g2 = fun2(fun2(vec(1) + a, fun0), fun1(fun2(fun0,fun2(fun0,fun0))))
let h2 = vec(fun2(fun1(fun0 + fun2(fun0,fun1(vec(8)))),a + b) + a15)

rem INCORRECTAS----------------
rem let z2 = fun2(1)
rem let y2 = fun2(a)
rem let x2 = fun2(vec(1))
rem let w2 = fun2(vec(a))
rem let v2 = a + fun2(a)
rem let u2 = fun2(a+1,b+2,c+3)

end