from ply import *
from math import factorial as f
import sys
        
def C(n,m):
	return f(n)*1.0/f(m)/f(n-m)

tokens = (
    "BEGIN",
    "END",
    "ANSWER_BLANK",
    "ANSWER_BEGIN",
    "ANSWER_END",
    "MATH_LPAREN",
    "MATH_RPAREN",
    "BOLD_MARK",
    "NUMBER",
    "PARAMETER",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    "EQUAL",
    "DOUBLE_QUOTATION_MARK",
    "SINGLE_QUOTATION_MARK",
    "WORD",
    "NEWLINE",
    "BLANK",
    "COMMENT",
    "PUNCTUATION"
    
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUAL = r'='
t_DOUBLE_QUOTATION_MARK = r'\"'
t_SINGLE_QUOTATION_MARK = r'\''

def t_BEGIN(t):
    r"[\s\S]*\$showPartialCorrectAnswers\ =\ 1\;"
    pass

def t_BEGIN_PG(t):
    r"BEGIN_PGML"
    pass
    
def t_COMMENT(t):
    r"\#\s*"
    pass

#ignore the start part, which we don't need in XML files


#ignore the ending part
def t_END(t):
    r"END_PGML[\s\S]*"
    pass

#find the place to fill in answers
def t_ANSWER_BLANK(t):
    r"\[_+\]"
    return t

#where the expected answer begins
def t_ANSWER_BEGIN(t):
    r"\{Compute\(\""
    return t

#where the expected answer ends
def t_ANSWER_END(t):
    r"\"\)\}"
    return t

#the typical parentheses for a math expression
def t_MATH_LPAREN(t):
    r"\[\`"
    return t

def t_MATH_RPAREN(t):
    r"\`\]"
    return t

#find the mark of bold content
def t_BOLD_MARK(t):
    r"\*"
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_PARAMETER(t):
    r'$\w'
    return t

#the normal words,without punctuation
def t_WORD(t):
    r"[\\a-zA-Z_-]+"
    return t

def t_PUNCTUATION(t):
    r"[,.?]+"
    return t

#a new line
def t_NEWLINE(t):
    r"\n+"
    return t

#the other blanks we want to ignore
def t_BLANK(t):
    r"\s+"

#error handling
def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

#build the lexer
lex.lex()

def p_newline(p):
        """
        newline : NEWLINE
        """
        print 'newline=',p[1]
        p[0]=p[1]

def p_bold_mark(p):
        """
        bold_mark : BOLD_MARK
        """
        print 'bold_mark=',p[1]
        p[0]=p[1]

def p_word(p):
        """
        word : WORD
        """
        print 'word=',p[1]
        p[0]=p[1]

def p_error(p):
        print "error"
        return "error"

#build the parser
yacc.yacc()
