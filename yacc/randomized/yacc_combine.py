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
    'PUNCTUATION',
    'FUNCTION',
    'COMMA'
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUAL   = r'='
t_DOLLAR  = r'\$'
#t_FUNCTION = r'C'
t_COMMA = r','

def t_RANDOM(t):
	'random'
	return t

def t_NUMBER(t):
    r'\d+\.?\d*'    
    return t

def t_FUNCTION(t):
	r'C'
	return t

def t_WORD(t):
    r"[\\a-zA-Z_]+"
    return t

def t_NEWLINE(t):
	r'\n+'
	return t

def t_BLANK(t):
    r"\s+"
    return t

def t_PUNCTUATION(t):
    r"[.?:|{};]+"
    return t

def t_error(t):
    raise TypeError("token error: Unknown text '%s'" % (t.value,))

lex.lex()

def p_segment(p):
	'''
	segment : segment element
			| element
	'''
	if len(p) == 2:
		p[0] = p[1]
	else: 
		p[0] = p[1] + p[2]

def p_element(p):
	'''
	element : random
			| PUNCTUATION
			| expression
			| WORD
			| EQUAL
			| BLANK
			| NEWLINE
	'''
	p[0] = p[1]


def p_random(p):
	'''
	random : RANDOM
	'''
	p[0] = 'random.randrange'



def p_expression(p):
	'''
	expression : expression PLUS term 
			   | expression MINUS term
			   | term 
	'''
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0] = p[1] + p[2] + p[3]


def p_term(p):
	'''
	term : term TIMES factor
		 | term DIVIDE factor
		 | term factor
		 | factor
	'''
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0] = p[1] + p[2] + p[3]
	else:
		p[0] = p[1] + '*' + p[2]


def p_factor(p):
	'''
	factor : NUMBER
		   | variable
		   | LPAREN expression RPAREN
		   | FUNCTION LPAREN expression COMMA expression RPAREN
		   | random LPAREN expression COMMA expression COMMA expression RPAREN
	'''
	if len(p) == 2:
		p[0] = p[1]
	elif len(p) == 4:
		p[0] = p[1] + p[2] + p[3]
	elif len(p) == 7:
		p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]
	else: 
		p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7] + p[8]


def p_variable(p):
	'''
	variable : DOLLAR WORD
	'''
	p[0] = p[2]
     
def p_error(p):
    raise TypeError("parse error : unknown text at %r" % (p.value,))
    
yacc.yacc()

file = open('script.txt')
data = file.read()
script = '\n<script>\n' + 'from math import factorial as f\n\n'+'import random\n\n'+'def C(n,m):\n'+'\treturn f(n)/f(m)/f(n-m)\n'
script = script + yacc.parse(data) + '\n</script>\n'

file2 = open('text.txt')
text = file2.read()

outfile = open('output.XML','w')
output = '<problem>\n' + script + text + '\n</problem>\n'
outfile.write(output)

