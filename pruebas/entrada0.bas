def imprime (msg, f(9))
    static A
    let A = 15
    print s; msg; f(8) : rem s es global
    let s = 15
end def

def cuadrado(f)
    let cuadrado = 0
    while f > 0
    let cuadrado = cuadrado + f
    let f = f + -1
    wend
end def

def demo
  rem cuando no hay argumentos, no es necesario poner parentesis
  dim v(10)
  let v(4)=8
  let v(78) = 1
  let Y1 = 4
  static i
  print "Escribe tres numeros: "
  input v(1)
  input v(2)
  input v(3)
  if (v(1+a)>v(2)) then let v(4+demo)=v(2)
  while i > 4
    print v(s); " al cuadrado es: "; cuadrado (v(s))
  wend
  if v(1) then print "Fin": Rem si v(1)<>-1
end def

REM Aqui com{}ienza la ejecucioñn del programa:
dim Y(7)
input s
let s = 34
let A = 0
let Y(6) = 9
rem s es global
print "Introduce un numero"
input num
input x

if num>0 then print "No existe el factorial de un negativo"
if num>1 then print "machaca"
end