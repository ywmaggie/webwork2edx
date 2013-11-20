from ply import *
from math import factorial as f
        
def C(n,m):
	return f(n)*1.0/f(m)/f(n-m)

tokens = (
    "BEGIN",
    "END",
    "ANSWER",
    "ANSWER_BLANK",
    "MATH_EXPRESSION",
    "BOLD_MARK",
    "WORDS",
    "NEWLINE",
    "BLANK"
)
#ignore the start part, which we don't need in XML files
def t_BEGIN(t):
    r"[\s\S]*BEGIN_PGML"
    pass

#ignore the ending part
def t_END(t):
    r"END_PGML[\s\S]*"
    pass

#to get the true answer out if the format of "Compute"
def t_ANSWER(t):
    r"\{Compute\(\".+\"\)\}"
    split_1 = t.value
    split_2 = split_1.split('{Compute(\"')[1]
    split_3 = split_2.split('\")}')[0]	
    t.value = eval(split_3)
    return t

#find the place to fill in answers
def t_ANSWER_BLANK(t):
    r"\[_+\]"
    return t

#find the math expression different from words that need to be carefully dealt with
def t_MATH_EXPRESSION(t):
    r"\[\`\\\w+\`\]"
    return t

#find the mark of bold content
def t_BOLD_MARK(t):
    r"\*"
    return t

#the normal words,with punctuation
def t_WORDS(t):
    r"[\w\'\",\.\?-]+[ \t]*"
    return t

#a new line
def t_NEWLINE(t):
    r"\n+"
    return t

#the other blanks we want to ignore
def t_BLANK(t):
    r"\s+"
    pass

#error handling
def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

#build the lexer
lex.lex()

