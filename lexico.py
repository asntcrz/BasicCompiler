###******************************************************************
### COMPILADORES 2009-2010****IMPLEMENTACION DEL ANALIZADOR LEXICO **
###******************************************************************
###  En principio terminado a falta de modificaciones posteriores
###******************************************************************

from tablasimbolos import *
from errores import *
import re

global listatokens
listatokens = []

tokens = palabrasreservadas + (
	'ID',
	'NUMBER',
	'MAS',
	'MENOS',
	'IGUAL', 
	'APARENT',
	'CPARENT',
	'COMA',
    'PYC',
	'MAYOR',
    'MENOR',
    'DISTINTO',
	'STRING',
	'COMMENT',
	'CR',
	'PR',
	'IDFAKE')

# Tokens
t_MAS = r'\+'
t_MENOS = r'-'
t_IGUAL = r'='
t_COMA = r','
t_PYC = r';'
t_MAYOR = r'>'
t_MENOR = r'<'
t_DISTINTO = r'<>'
t_APARENT = r'\('
t_CPARENT = r'\)'
t_CR = r'(\\n|\:)'
t_STRING = r'\"([^\\\n\"]|(\\.))*_?\"'


def t_IDFAKE(t):
    r'[0-9]+[a-zA-Z][a-zA-Z0-9]*'
    nuevo_error(t.lineno,'lexico','Identificador ' + str(t.value) + ' mal construido')
    t.lexer.lineno += t.value.count("\n")
    pass

def t_COMMENT(t):
    r'([Rr][Ee][Mm])[ \t](.)*\n?'
    t.lexer.lineno += t.value.count("\n")
    pass

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    try:
        t.value = t.value.lower()
        palabrasreservadas.index(t.value)
        t.type = 'PR'
    except:
        t.value = t.value.lower()
        t.type = 'ID'
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    if t.value > 32767:
       pass
       #print "Esto no es un numero '%s'" % t.value
       nuevo_error(t.lineno,'semantico','Numero ' + str(t.value) + ' incorrecto (Valor maximo 32767)')
    else:
       return t 
 
# Ignored characters
t_ignore  = ' \t'

def t_newline(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")
	t.type = 'CR'
	return t

def t_error(t):
    print "t.value = ", t
    nuevo_error(t.lineno,'lexico',"Caracter -->" + str(t.value[0]) + "<-- ilegal")
    t.lexer.skip(1)

def lexico(data):
    # Build the lexer 
    import ply.lex as lex
    lex.lex()
    debug=0

    # Give the lexer some input
    lex.input(data)

    # Tokenize
    while True:
        tok = lex.token()
        if not tok: break      # No more input
        listatokens.append([tok.type,tok.value,tok.lineno])
        #listatokens.append(str(tok))
    token_eof = ['EOF','$',0]
    listatokens.append(token_eof)
