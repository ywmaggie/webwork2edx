import ply.lex as lex
import ply.yacc as yacc

class MyCode:
     
    # First part : lexer
      
    # Literals are tokens that remain the same as they are 
    literals = [',','(',')','+','-','*','/','=']

    #reserverd names used in code
    reserved = {
        'C' : 'C_FUNCTION',
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
    t_SPACE   = r'[ \t]'
    t_ignore_semicolon = r';'
    t_ignore_dollar = r'\$'
    t_ignore_comment = r'\#\#.*'
    t_ignore_compute = r'compute'
    t_ignore_quotation = r'\"'

    #change 'random' in Perl to 'random.range' in Python
    def t_RANDOM(self,t):
        r'random'
        t.value = 'random.randrange'
        return t

    #change '^' to '**'
    def t_EXPONENT(self,t):
        r'\^'
        t.value = '**'
        return t

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

    # Every 
    def p_element(self,p):
        '''
        element : expression
                | '='
                | SPACE
                | NEWLINE
        '''
        p[0] = p[1]


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
    def p_factor(self,p):
        '''
        factor : NUMBER
               | ID
               | '(' expression ')'
               | C_FUNCTION '(' expression ',' expression ')'
               | RANDOM '(' expression ',' expression ',' expression ')'
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[1] + p[2] + p[3]
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

    #Test the parser
    def test_parser(self,data):
        result = self.parser.parse(data,lexer = self.lexer)
        s = '''
<problem>
    <script>
from math import factorial as f

def C(n,m):
    return f(n)/f(m)/f(n-m)
        '''
        return s+result + '</script>\n'



