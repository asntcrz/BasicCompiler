def fun1 (d)
    let fun1 = d + 2
    let a = fun1(3)
    static b
end def

def fun2 (a,b)
    let x = fun1(a)
    let fun2 = x + fun1(2)
    dim v(4)
end def

def fun0
    print "hi"
end def

def fun3(a,b)
 dim e(10)
 let a = fun1(1)
    let x = b + fun2(2,e(e(9)))
end def

let r = fun2(1,2)
print r
print fun0
let a = fun3(r,fun1(f))
end