def fun(n,v(8))
    print v(n)
    let v(n) = n + 1
    print v(n)
  rem   while 5 > n
    if 5 > n then let fun = fun(n+1,v)
     print n
     let n = n +1
   rem wend

end def

dim v (8)

let v(1) = 1
print v(1)
let n = 2
let v(n) = 9
print v(n)
print fun(0,v)
end