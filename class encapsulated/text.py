import ply.lex as lex
import ply.yacc as yacc

class MyText:

    answer_blank_count = 0 # record the number of answer blanks in order to implement the answer blank in XML
    answer_count = 0 # count the number, to give the answers different IDs
    left = 0
    right = 0
    answers = ''

    # First Part: lexer

    states = (
              ('answer','exclusive'),
            )

    # Asterisk serves as a bold mark in a bold segment
    literals = ['*','[',']','{','}']


    # List of token names.   
    tokens = (
                'WORD',
                'ANSWER_BLANK',
                'MATH_LPAREN',
                'MATH_RPAREN',
                'NEWLINE',                                                                                                 
                'SPACE',
                'VARIABLE',
                'PUNCTUATION',
                'OPERATOR',
                'LT',
            )
              
    # Regular expression rules for simple tokens
    t_WORD = r'\w+'
    t_OPERATOR = r'[\+\-\/\^=]'
    t_SPACE = r'[ \t]'
    t_ignore_comment = r'\#\#.*'
    
    #Define answer blank as [_______],where to fill in answers
    def t_ANSWER_BLANK(self,t):
        r"\[_+\]"
        return t

    # where the expected answer begins. A sample answer is {Compute("C(4($z-2),$y)C(52-4($z-2),5-$y)")}
    # the lexer enters a specail mode 'answer' to fetch to entire answer 
    def t_answer(self,t):
        r"(\{Compute\(\")"
        t.lexer.code_start = t.lexer.lexpos
        t.lexer.begin('answer')
        self.answer_count += 1

    #where the expected answer ends
    def t_answer_end(self,t):
        r"\"\)\}\.?"
        t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos-len(t.value)]
        t.type = "ANSWER"
        #t.lexer.lineno += t.value.count('\n')
        self.answers = self.answers + 'answer' + str(self.answer_count) + ' = 1.0*' + t.value + '\n'
        t.lexer.begin('INITIAL')

    def t_answer_element(self,t):
        r'[^\"\}]+'

    def t_answer_error(self,t):
        print 'lexer error at %r %r' % (t.value,t.lineno)
        t.lexer.skip(1)
        

    # The parenthesis of a math expression is like [`P(A|B) = `]. We define the left parenthesis and right parenthesis
    # and translate it into \( P(A|B) = \)
    def t_MATH_LPAREN(self,t):
        r"\[\`{1,2}"
        #global left
        self.left += 1
        #print left
        t.value = '\('
        return t

    def t_MATH_RPAREN(self,t):
        r"\`{1,2}\]"
        #global right
        self.right += 1
        #print right
        t.value = '\)'
        return t

    # Define a rule so we can track line numbers
    def t_NEWLINE(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return t

    #variables like [$x],[$y]
    def t_VARIABLE(self,t):
        r'\$[a-zA-Z_0-9]+'
        return t

    # Define all punctuations
    def t_PUNCTUATION(self,t):
        r"[().,?:|!\\\"\']"
        return t

    def t_LT(self,t):
        r'\<'
        t.value = '&lt;'
        return t

    # Error handling rule
    def t_error(self,t):
        print "Illegal character %r %r" % (t.value[0],t.lineno)
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





    # Second part : parser


    # The text itself is a segment
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


    # A bold segment is text enbraced by *   eg.* blabla *
    def p_bold_segment (self,p):
        '''
        bold_segment : '*' text '*'
        '''   
        p[0] = '<b>'+p[2]+'</b>'

    # Text is pure text, not bold text
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
                | LT
                | VARIABLE
                | '[' text ']' 
                | MATH_LPAREN text MATH_RPAREN
                | '{'
                | '}'
        '''
        #print p[1]
        if len(p) == 2:
            p[0] = p[1]
        elif p[1] == '\(':
            #print 'left '+str(left) + ' right ' + str(right)
            p[0] = p[1] + p[2] + p[3]
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
    '''
    def p_answer(self,p):
        
        answer : ANSWER_BEGIN text ANSWER_END
               | '{' text '}'
        
        self.answer_count += 1
        self.answers = self.answers + 'answer' + str(self.answer_count) + ' = 1.0*' + p[2] + '\n'
        p[0] = ''
    '''

    def p_error(self,p):
        raise TypeError("parse error:unknown text at %r %r" % (p.value,p.lineno))

    # Build the parser
    def build_parser(self):
        self.parser = yacc.yacc(module = self)

    #Test the parser
    def test_parser(self,data):
        result = self.parser.parse(data,lexer = self.lexer)
        return '<p>'+result + '</p>\n</problem>'


    def MyAnswer(self):
        return self.answers







