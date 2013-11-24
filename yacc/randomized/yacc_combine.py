#from yacc_v2 import *
from ply import *

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUAL',
    'LPAREN',
    'RPAREN',
    'RANDOM',
    'WORD',
    'DOLLAR',
    'NEWLINE',
    'BLANK',
    'PUNCTUATION'
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUAL   = r'='
t_DOLLAR  = r'\$'

def t_RANDOM(t):
	'random'
	return t

def t_NUMBER(t):
    r'\d+\.?\d*'    
    return t

def t_WORD(t):
    r"[\\a-zA-Z_-]+"
    return t

def t_NEWLINE(t):
	r'\n+'
	return t

def t_BLANK(t):
    r"\s+"
    return t

def t_PUNCTUATION(t):
    r"[,.?:|{};]+"
    return t

def t_error(t):
    raise TypeError("token error: Unknown text '%s'" % (t.value,))

lex.lex()

def p_term(p):
	'''
	term : term factor
	     | factor
	'''
	if len(p) == 2:
		p[0] = p[1]
	else:
		p[0] = p[1] + p[2]

def p_random(p):
	'''
	factor : RANDOM
	'''
	p[0] = 'random.randrange'

def p_factor(p):
	'''
	factor : NUMBER
		   | PLUS
		   | MINUS
		   | TIMES
		   | DIVIDE
		   | LPAREN
		   | RPAREN
		   | WORD
		   | EQUAL
		   | BLANK
		   | PUNCTUATION
	'''
	p[0] = p[1]

def p_newline(p):
	'''
	factor : NEWLINE
	'''
	p[0] = p[1]

def p_variable(p):
	'''
	factor : DOLLAR WORD
	'''
	p[0] = p[2]
     
def p_error(p):
    raise TypeError("parse error : unknown text at %r" % (p.value,))
    
yacc.yacc()

file = open('script.txt')
data = file.read()
print yacc.parse(data)
lex.input(data)
for tok in iter(lex.token, None):
    print str(repr(tok.type))+str(repr(tok.value))