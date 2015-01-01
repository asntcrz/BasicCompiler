dim U(8)

def fun0
    static v0
    print "0"
end def

def fun1(pf1)
    static v1
    print "1"
end def

input f
input U(7)
input U(fun0+fun1(f+5))
input U(U(U(U(U(fun1(1)+1)))))
end