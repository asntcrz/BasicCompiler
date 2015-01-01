
def FactorialDo (n)
  static factorial
  let factorial = 1
  while n > 1: rem hasta que n sea menor que uno
    let factorial = factorial + n
    let n = n + 1
  wend
  let FactorialDo = factorial
end def


let a = FactorialDo (2)
end