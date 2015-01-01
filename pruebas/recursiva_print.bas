def fun(a,b,c)
print c
print b
print a
print fun(c,b,a)
end def

def fun2(a,b)
rem print a
rem print b
print fun(a,b,a+b)

end def

print fun2(2,3)

end