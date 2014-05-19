import ply.lex as lex
import ply.yacc as yacc

class MyCodeLexer:
    # List of token names.   This is always required
    tokens = (
              'NUMBER',
              'COMMA',
              'C_FUNCTION',
              'LPAREN',
              'RPAREN',
              'EXPONENT',
              'DOLLAR',
              'WORD',
              'EQUAL',
              'SEMICOLON',
              'PLUS',
              'MINUS',
              'TIMES',
              'DIVIDE',
              'SPACE',
              'NEWLINE',
              'RANDOM',
              )

    # Regular expression rules for simple tokens
    t_EXPONENT= r'\^'
    t_COMMA   = r'\,'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    #t_C_FUNCTION = r'C'
    t_NUMBER  = r'\d+(\.\d+)?'
    t_WORD    = r'[a-zA-Z][a-zA-Z_0-9]*'
    t_NEWLINE = r'\n+'
    t_SPACE   = r'[ \t]'
    #t_RANDOM  = r'random'
    #t_OPERATOIN = r'[\+\-\*\/]'
    t_EQUAL   = r'\='
    t_SEMICOLON = r';'
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIVIDE  = r'/'
    t_DOLLAR  = r'\$'

    # Error handling rule

    def t_RANDOM(self,t):
        r'random'
        return t

    def t_C_FUNCTION(self,t):
        r'C'
        return t

        
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


    
    def p_segment(self,p):
        '''
        segment : segment element
                | element
        '''
        if len(p) == 2:
            p[0] = p[1]
        else: 
            p[0] = p[1] + p[2]

    def p_element(self,p):
        '''
        element : SEMICOLON
                | expression
                | EQUAL
                | SPACE
                | NEWLINE
                | random
        '''
        if p[1] == ';':
            p[0] = ''
        else:
            p[0] = p[1]


    def p_random(self,p):
        '''
        random : RANDOM
        '''
        p[0] = 'random.randrange'


    def p_expression(self,p):
        '''
        expression : expression PLUS term 
                   | expression MINUS term
                   | term 
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            p[0] = p[1] + p[2] + p[3]


    def p_term(self,p):
        '''
        term : term TIMES factor
             | term DIVIDE factor
             | term EXPONENT factor
             | term factor
             | factor
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            if p[2] == '^':
                p[0] = p[1] + '**' + p[3]
            else:
                p[0] = p[1] + p[2] + p[3]
        else:
            p[0] = p[1] + '*' + p[2]


    def p_factor(self,p):
        '''
        factor : NUMBER
               | variable
               | LPAREN expression RPAREN
               | C_FUNCTION LPAREN expression COMMA expression RPAREN
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
            

    def p_variable(self,p):
        '''
        variable : DOLLAR WORD
                 | WORD
        '''
        if len(p) == 2:
            p[0] = p[1]
        else: 
            p[0] = p[2]



    # Error rule for syntax errors
    def p_error(self,p):
        raise TypeError("parse error : unknown text at %r" % (p.value,))


    # Build the parser
    def build_parser(self):
        self.parser = yacc.yacc(module = self)

    #Test the parser
    def test_parser(self,data):
        result = self.parser.parse(data,lexer = self.lexer)
        print result