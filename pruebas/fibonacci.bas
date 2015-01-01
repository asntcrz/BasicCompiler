def fibonacci (n)

let a = -1

if n > 1 then let a = 0
if n >1 then let fibonacci = fibonacci(n+(-1)) + fibonacci(n+(-2))
print fibonacci
while a
 let fibonacci = 1
    let a = 0
wend

end def


input x

print fibonacci(x)

end