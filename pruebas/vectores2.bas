def asignacion(vec(4))
    print "Introduce numeros para rellenar vector 1"
    REM input vec5 : REM funciona mal
  rem  let n = 0
    while n < 4
       rem   input vec(n)
     print vec(n)
    rem     let n = n +1
    wend
end def
rem 
rem def copiaElem(v1(4),v2(4))
rem    print "copia un vector a otro elemento a elemento"
 rem   let b = 0
rem    while b < 4
   rem     let v1(b) = v2(b)
      rem  print v2(b)
    rem    let b = b +1
  rem  wend
rem end def

rem def copiavec(v1(4),v2(4))
rem     print "copia un vector a otro directamente"
rem     let v1 = v2
rem end def

def imprimevec(v(4))
    let i = 0
    while i < 4
        print v(i)
        let i = i +1
    wend
end def

dim vec41(4)
dim vec5(5)
dim vec42(4)
dim vec43(4)
rem  dim vec42(4) : rem funciona mal

rem let a = asignacion(vec41)
rem let a = imprimevec(vec41)
rem let a = copiaElem(vec41,vec42)
rem let a = imprimevec(vec42)
rem let a = copiavec(vec43,vec42)
rem let a = imprimevec(vec43)

rem let a = copiavec(vec5,vec4) : REM funciona mal
rem let vec4 = 4 : rem funciona mal

let a = b
end

