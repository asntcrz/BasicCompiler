def cuadrado (i)
  let cuadrado=i+i
end def

def imprime (msg, f)
  print s; msg; f : rem s es global
end def

def demo
  rem cuando no hay argumentos, no es necesario poner parentesis
  dim v(4)
  let v(4)=8
  static i
  print "Escribe tres numeros: "
  input v(1)
  input v(2)
  input v(3)
  if (v(1)>v(2)) then let v(4)=v(2)
  while i > 4
    print v(i); " al cuadrado es: "; cuadrado (v(i))
  wend
  if v(1) then print "Fin": Rem si v(1)<>-1
end def
input a
end