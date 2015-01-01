dim v(2)
let a = 5
let b = 3
if -1 then print "BIEN"
if 0 then print "MAL"
if a>b then let v(0)=-1
if v(0) then let v(1) = 4
print v(1)

if a>b then let v(0)=1
if v(0) then let v(1) = 5
print v(1)

rem let b=fun(1,2): rem MAL!
rem if fun(1,2,3) then print "hola"
let a = 0
if a then print "hola"
let a = -1
if a then print "adios"
end