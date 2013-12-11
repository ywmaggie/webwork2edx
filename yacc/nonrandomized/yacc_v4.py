from ply import *
from math import factorial as f
        
def C(n,m):
    return f(n)*1.0/f(m)/f(n-m)

answer_blank_count = 0
answer_count = 0
all_answer = []
left = 0
right = 0

tokens = (
    "BEGIN",
    "END",
    "ANSWER_BLANK",
    "ANSWER_BEGIN",
    "ANSWER_END",
    "MATH_LPAREN",
    "MATH_RPAREN",
    "LBRACE",
    "RBRACE",
    "NUMBER",
    "PARAMETER",
    "PUNCTUATION",
    "PLUS",
    "MINUS",
    "DIVIDE",
    "LPAREN",
    "RPAREN",
    "EQUAL",
    "WORD",
    "NEWLINE",
    "BLANK",
    "COMMENT",
    "STAR",
    "VARIABLE",
    "EXPONENT",
    "LBOLD",
    "RBOLD"
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_EQUAL = r'='
t_LBRACE = r'{'
t_RBRACE = r'}'

def t_LBOLD(t):
    r'\s\*'
    return t

def t_RBOLD(t):
    r'\*\s'
    return t

def t_VARIABLE(t):
    r'\$[a-zA-Z_0-9]+'
    return t

def t_EXPONENT(t):
    r'\^'
    return t

def t_BEGIN(t):
    r"[\s\S]*\$showPartialCorrectAnswers\ =\ 1\;\n*"
    pass

def t_BEGIN_PG(t):
    r"\n*BEGIN_PGML"
    pass
    
def t_COMMENT(t):
    r"\#\s*"
    pass

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
    r"\"\)\}\.?"
    return t

#the typical parentheses for a math expression
def t_MATH_LPAREN(t):
    r"\[\`{1,2}"
    global left
    left += 1
    #print left
    return t

def t_MATH_RPAREN(t):
    r"\`{1,2}\]"
    global right
    right += 1
    #print right
    return t

#find the mark of bold content
def t_STAR(t):
    r"\*"
    return t

def t_NUMBER(t):
    r'\d+'
    #t.value = int(t.value)    
    return t

#the normal words,without punctuation
def t_WORD(t):
    r"[\\a-zA-Z_]+"
    return t

def t_PUNCTUATION(t):
    r"[,.?:|!\'\"]+"
    return t

#a new line
def t_NEWLINE(t):
    r"\n"
    return t

#the other blanks we want to ignore
def t_BLANK(t):
    r"\s"
    return t

#error handling
def t_error(t):
    raise TypeError("token error:Unknown text '%s'" % (t.value,))

#build the lexer
lex.lex()

def p_segment (p):
    '''
    segment : segment bold_segment
            | segment text
            | bold_segment
            | text 
    '''
    if len(p) == 2:
        p[0] = p[1]
    else :
        p[0] = p[1] + p[2]


def p_bold_segment (p):
    '''
    bold_segment : LBOLD text RBOLD
    '''   
    p[0] = '<b>'+p[2]+'</b>'


def p_expect_answer(p):
    '''
    text : ANSWER_BLANK answer
    '''
    global answer_blank_count
    answer_blank_count += 1
    s = '''<numericalresponse answer="$answer'''+str(answer_blank_count)+'''">
                <responseparam type="tolerance" default="1%" />
                <formulaequationinput />
            </numericalresponse>\n'''

    global answer_count
    answer_count += 1
    ss = p[2].split('{')[1]
    answer = ss.split('}')[0]
    ans = 'answer' + str(answer_count) + ' = 1.0*' + answer
    all_answer.append(ans)
    p[0] = s


def p_answer(p):
    '''
    answer : ANSWER_BEGIN text ANSWER_END 
    '''
    p[0] = '{'+p[2]+'}'

def p_answer_2(p):
    '''
    answer : LBRACE segment RBRACE
    '''
    p[0] = p[1] + p[2] + p[3]


def p_text(p):
    '''
    text : text element
         | element         
    '''
    #print 'text:',
    if len(p) == 2:
        #print p[1]
        p[0] = p[1]
    else:
        #print p[1],p[2]
        p[0] = p[1]+p[2]


def p_exponent(p):
    '''
    exponent : EXPONENT
    '''
    p[0] = '**'

def p_element (p):
    '''
    element : WORD
            | BLANK
            | PUNCTUATION
            | MINUS
            | DIVIDE
            | LPAREN
            | RPAREN
            | EQUAL
            | MATH_LPAREN text MATH_RPAREN
            | PLUS
            | answer
            | NUMBER
            | STAR
            | exponent
    '''
    #print p[1]
    if len(p) == 2:
        p[0] = p[1]
    else:
        #print 'left '+str(left) + ' right ' + str(right)
        p[0] = '\(' + p[2] + '\)'


def p_newline(p):
    '''
    element : NEWLINE
    '''
    if left == right:
        p[0] = '</p>\n<p>'
    else:
        p[0] = '<br/>'



def p_error(p):
    raise TypeError("parse error:unknown text at %r" % (p.value,))
    #print 'error'

yacc.yacc()


file = open('poker_cond5_2.pg')
data = file.read()

lex.input(data)
for tok in iter(lex.token, None):
    print str(repr(tok.type))+str(repr(tok.value))


outfile = open('output.XML','w')

text =  '</script>\n\n<text>\n<p>\n' + yacc.parse(data) + '\n</p>\n</text>\n</problem>'

script = '<problem>\n<script>\n' + 'from math import factorial as f\n\n'+'def C(n,m):\n'+'\treturn f(n)/f(m)/f(n-m)\n'

for ans in all_answer:
    script = script + ans + '\n'

output = script + text

outfile.write(output)

