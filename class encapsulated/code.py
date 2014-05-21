# This file contains a class definatoin for 'code' translation

import ply.lex as lex
import ply.yacc as yacc

class MyCode:
     
    # First part : lexer
      
    # Literals are tokens that remain the same as they are 
    literals = [',','(',')','+','-','*','/','=']

    #reserverd names used in code
    reserved = {
        'C' : 'C_FUNCTION',
        'ceil' : 'CEIL',
    }

    # List of token names
    tokens = [
                'RANDOM',
                'EXPONENT',
                'NUMBER',
                'ID',
                'SPACE',
                'NEWLINE',
              ] + list(reserved.values())

    # Regular expression rules for simple tokens
    t_NUMBER  = r'\d+(\.\d+)?'
    t_NEWLINE = r'\n+'
    t_SPACE   = r'[\t]'
    t_ignore_semicolon = r';'
    t_ignore_dollar = r'\$'
    t_ignore_comment = r'\#\#.*'
    t_ignore_quotation = r'\"\)'
    t_ignore_space = r'[ ]'

    # Change the name of function 'random' to a new defined function 'myrandom'
    def t_RANDOM(self,t):
        r'random'
        t.value = 'myrandom'
        return t

    #change '^' to '**'
    def t_EXPONENT(self,t):
        r'\^'
        t.value = '**'
        return t

    # Ignore the beginning part of caculating a math expression
    # like Compute("1+2+3")
    def t_compute(self,t):
        r'Compute\(\"'
        pass

    # Ignore the distinct webwork declaration
    # like Context("Numeric"); or Context()->variables->add(p => 'Real'); 
    # as the use of such declarations are already included in the translation system
    def t_context(self,t):
        r'Context.*'
        pass

    def t_ID(self,t):
        r'[a-zA-Z][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
        return t

    # Error handling rule   
    def t_error(self,t):
        print "Illegal character '%s'" % t.value[0]
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self,**kwargs)
    
    # Test the lexer
    def test(self,data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print tok


    
    # Second part : parser

    # The code itself is a segment 
    def p_segment(self,p):
        '''
        segment : segment element
                | element
        '''
        if len(p) == 2:
            p[0] = p[1]
        else: 
            p[0] = p[1] + p[2]

    # Single elements construct the the whole segment
    def p_element(self,p):
        '''
        element : expression
                | '='
                | SPACE
                | NEWLINE
        '''
        p[0] = p[1]

    # Math expression 
    def p_expression(self,p):
        '''
        expression : expression '+' term 
                   | expression '-' term
                   | term 
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[1] + p[2] + p[3]

    # Terms construct math expression
    def p_term(self,p):
        '''
        term : term '*' factor
             | term '/' factor
             | term EXPONENT factor
             | term factor
             | factor
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[1] + p[2] + p[3]
        else:
            p[0] = p[1] + '*' + p[2]

    # A factor is the basic element in a equation
    # A factor is a encapsulated element in a math expression  
    def p_factor(self,p):
        '''
        factor : NUMBER
               | ID
               | '(' expression ')'
               | C_FUNCTION '(' expression ',' expression ')'
               | RANDOM '(' expression ',' expression ',' expression ')'
               | RANDOM '(' expression ',' expression ')'
               | CEIL '(' expression ')'
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[1] + p[2] + p[3]
        elif len(p) == 5:
            p[0] = p[1] + p[2] + p[3] + p[4]
        elif len(p) == 7:
            p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]
        else: 
            p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6] + p[7] + p[8]
            



    # Error rule for syntax errors
    def p_error(self,p):
        raise TypeError("parse error : unknown text at %r %r" % (p.value,p.lineno))


    # Build the parser
    def build_parser(self):
        self.parser = yacc.yacc(module = self)

    # Test the parser and output the script
    # Add several functions useful for script interpretion
    def test_parser(self,data):
        result = self.parser.parse(data,lexer = self.lexer)
        s = '''
<problem>
    <script>
from math import factorial as f
from math import ceil
import random

def C(n,m):
    return f(n)/f(m)/f(n-m)

def myrandom(start,stop,step=1):
    return random.randint(0, int((stop - start) / step)) * step + start
'''
        return s+result + '</script>\n'



