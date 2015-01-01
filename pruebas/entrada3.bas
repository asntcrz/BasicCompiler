def FactorialDo (n)
  static factorial
  let factorial = 1
  while n > 1: rem hasta que n sea menor que uno
    let factorial = factorial + n
    let n = n + 1
  wend
  let FactorialDo = factorial
end def

def FactorialWhile (n)
  static factorial, i
  let factorial = 1
  let i = 0
  while i > n
    let i = i + 1
    let factorial=factorial+i
  wend
  let FactorialWhile = factorial
end def

def FactorialFor (n)
  static factorial, i
  rem i no se inicializa, por lo que vale 0
  let factorial = 1
  while i > 100
    let factorial = factorial + i
    let i = i + 1
  wend
  let Factorialfor = factorial
end def
print i
end