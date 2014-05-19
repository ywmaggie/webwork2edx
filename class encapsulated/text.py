import ply.lex as lex
import ply.yacc as yacc

class MyTextLexer:

    answer_blank_count = 0 # record the number of answer blanks in order to implement the answer blank in XML
    answer_count = 0
    left = 0
    right = 0
    answers = ''



    # List of token names.   
    tokens = (
                'WORD',
                'STAR',
                'ANSWER_BLANK',
                'ANSWER_BEGIN',
                'ANSWER_END',
                'MATH_LPAREN',
                'MATH_RPAREN',
                'NEWLINE',                                                                                                 
                'SPACE',
                'VARIABLE',
                'PUNCTUATION',
                'LBRACKET',
                'RBRACKET',
                'LBRACE',
                'RBRACE',
                'OPERATOR',


              )
              
    # Regular expression rules for simple tokens
    t_WORD = r'\w+'
    t_STAR = r'\*' # Star uses as a bold mark in a bold segment
    t_LBRACKET = r'\[' # left square bracket
    t_RBRACKET = r'\]' # right square bracket
    t_LBRACE = r'\{'
    t_RBRACE = r'\}'
    t_OPERATOR = r'[\+\-\/\^=]'

    #t_BLANK = r'[ \t]'
    
    #Define answer blank as [_______],where to fill in answers
    def t_ANSWER_BLANK(self,t):
        r"\[_+\]"
        return t

    #where the expected answer begins. A sample answer is {Compute("C(4($z-2),$y)C(52-4($z-2),5-$y)")}
    def t_ANSWER_BEGIN(self,t):
        r"\{Compute\(\""
        return t

    #where the expected answer ends
    def t_ANSWER_END(self,t):
        r"\"\)\}\.?"
        return t

    # The parenthesis of a math expression is like [`P(A|B) = `]. We define the left parenthesis and right parenthesis
    # and translate it into \( P(A|B) = \)
    def t_MATH_LPAREN(self,t):
        r"\[\`{1,2}"
        #global left
        self.left += 1
        #print left
        return t

    def t_MATH_RPAREN(self,t):
        r"\`{1,2}\]"
        #global right
        self.right += 1
        #print right
        return t

    # Define a rule so we can track line numbers
    def t_NEWLINE(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t

    # Define spaces and tabs
    def t_SPACE(self,t):
        r'[ \t]'
        return t

    #variables like [$x],[$y]
    def t_VARIABLE(self,t):
        r'\$[a-zA-Z_0-9]+'
        return t

    # Define all punctuations
    def t_PUNCTUATION(self,t):
        r"[().,?:|!\\\"\']"
        return t

    # Pass all comments  
    #def t_COMMENT(self,t):
    #    r"\#\s*"
    #    pass

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
        '''while True:
            tok = self.lexer.token()
            if not tok:
                break
            print tok'''
        for tok in self.lexer:
            print tok





    # Begin parser part


    # Create segment as the whole problem 
    def p_segment (self,p):
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


    # A bold segment is enbraced by *   eg.* blabla *
    def p_bold_segment (self,p):
        '''
        bold_segment : STAR text STAR
        '''   
        p[0] = '<b>'+p[2]+'</b>'

    # Text is a plain text
    def p_text(self,p):
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

    # element is the smallest unit in a problem 
    def p_element (self,p):
        '''
        element : WORD
                | SPACE
                | OPERATOR
                | PUNCTUATION
                | VARIABLE
                | LBRACKET text RBRACKET
                | MATH_LPAREN text MATH_RPAREN
                | answer
        '''
        #print p[1]
        if len(p) == 2:
            p[0] = p[1]
        elif p[1] == '[`':
            #print 'left '+str(left) + ' right ' + str(right)
            p[0] = '\(' + p[2] + '\)'

        else:
            p[0] = p[2]

    # distinctive element, the answer blank to a problem
    def p_answer_blank (self,p):
        '''
        element : ANSWER_BLANK
        '''
        self.answer_blank_count += 1
        s = '''<numericalresponse answer="$answer'''+str(self.answer_blank_count)+'''">
                    <responseparam type="tolerance" default="1%" />
                    <formulaequationinput />
                </numericalresponse>\n'''
        #print s+'*********'
        p[0] = s

    def p_newline(self,p):
        '''
        element : NEWLINE
        '''
        if self.left == self.right:
            p[0] = '</p>\n<p>'
        else:
            p[0] = '<br/>'

    #answers are added to the python script and sre not shown in the XML text
    def p_answer(self,p):
        '''
        answer : ANSWER_BEGIN text ANSWER_END
               | LBRACE text RBRACE 
        '''
        self.answer_count += 1
        self.answers += p[2]
        p[0] = ''

    def p_error(self,p):
        raise TypeError("parse error:unknown text at %r" % (p.value,))

    # Build the parser
    def build_parser(self):
        self.parser = yacc.yacc(module = self)

    #Test the parser
    def test_parser(self,data):
        result = self.parser.parse(data,lexer = self.lexer)
        return result


    def MyAnswer(self):
        return self.answers







