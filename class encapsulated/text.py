# This file contains a class definatoin for 'text' translation

import ply.lex as lex
import ply.yacc as yacc

class MyText:

    answer_blank_count = 0 # Record the number of answer blanks in order to implement the answer blank in XML
    answer_count = 0 # Count the number, to give the answers different IDs
    left = 0         # Record the number that the left math parenthesis has appeared
    right = 0        # Record the number that the right math parenthesis has appeared
    answers = ''     # The answers need to be passed to 'code' part to translate in a different way 
                     # Here we just copy it in a string

    # First Part: lexer

    # The state control is to deal with differnt types of answers given
    states = (
              ('answer','exclusive'),
            )

    # Asterisk serves as a bold mark in a bold segment
    literals = ['*','{','}','[',']']


    # List of token names.   
    tokens = (
                'WORD',
                'ANSWER',
                'MATH_LPAREN',
                'MATH_RPAREN',
                'NEWLINE',                                                                                                 
                'SPACE',
                'VARIABLE',
                'PUNCTUATION',
                'OPERATOR',
                'LT',
                'GT',
            )
              
    # Regular expression rules for simple tokens
    t_WORD = r'\w+'
    t_OPERATOR = r'[\+\-\/\^=]'
    t_SPACE = r'[ \t]'
    t_ignore_comment = r'\#.*'

    # functions defined as t_answer_xxx are all for state 'answer'

    # Where the expected answer begins. A sample answer is {Compute("C(4($z-2),$y)C(52-4($z-2),5-$y)")}
    # The lexer enters a specail state 'answer' to fetch to entire answer 
    def t_answer(self,t):
        r"\[_+\]\{(Compute\(\")?"
        t.lexer.code_start = t.lexer.lexpos
        t.lexer.begin('answer')
        self.answer_count += 1

    # Where the expected answer ends
    def t_answer_end(self,t):
        r"\}\.?"
        value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos-len(t.value)]
        t.type = "ANSWER"
        #t.lexer.lineno += t.value.count('\n')
        self.answers = self.answers + 'answer' + str(self.answer_count) + ' = 1.0*' + value + '\n'
        t.lexer.begin('INITIAL')
        return t
    
    # Words, numbers ans all sorts of things in an answer
    def t_answer_element(self,t):
        r'[^\"\}]+'

    # Some answer are defined as {1+2+3}
    # While some are like {Compute("1+2+3")} 
    # So we need to ignore the extra words and punctuations except the real answer
    def t_answer_quotation_mark(self,t):
        r'\"\)([^\}])*\}'
        value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos-len(t.value)]
        t.type = "ANSWER"
        #t.lexer.lineno += t.value.count('\n')
        self.answers = self.answers + 'answer' + str(self.answer_count) + ' = 1.0*' + value + '\n'
        t.lexer.begin('INITIAL')
        return t

    # Deal with errors in the answer state
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

    # Variables like [$x],[$y]
    def t_VARIABLE(self,t):
        r'\$[a-zA-Z_0-9]+'
        return t

    # Define all punctuations
    def t_PUNCTUATION(self,t):
        r"[().,?:|!\\\"\']"
        return t

    # Special characters in XML that cannot behave themselves
    # eg. < is &lt; in XML, > is &gt;
    def t_LT(self,t):
        r'\<'
        t.value = '&lt;'
        return t

    def t_GT(self,t):
        r'\>'
        t.value = '&gt;'
        return t

    # Error handling rule
    def t_error(self,t):
        print "Illegal character %r %r" % (t.value[0],t.lineno)
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self,**kwargs)

    # Test the lexer
    # Print out all tokens
    def test(self,data):
        self.lexer.input(data)
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


    # A bold segment is text enbraced by '*'   eg.* This is a bold sentence. *
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
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1]+p[2]

    # element is the smallest unit in a problem 
    def p_element (self,p):
        '''
        element : WORD
                | SPACE
                | OPERATOR
                | PUNCTUATION
                | LT
                | GT
                | VARIABLE
                | '[' text ']'
                | MATH_LPAREN segment MATH_RPAREN
                | '{'
                | '}'
        '''
        if len(p) == 2:
            p[0] = p[1]
        elif p[1] == '\(':
            p[0] = p[1] + p[2] + p[3]
        else:
            p[0] = p[2]
        
    # A newline is simply '\n' in PGML
    # Here we translate it into <br/>
    def p_newline(self,p):
        '''
        element : NEWLINE
        '''
        if self.left == self.right: # When the numbers of appeared left math parenthesis and right math parenthesis are the same
                                    # means we are not in the middle of a math expression
                                    # Thus we are in between paragraphs
                                    # We give the last part a end mark </p> and the next part a start mark <p>
            p[0] = '</p>\n<p>'
        else:
            p[0] = '<br/>'          # When we are in the middle of a math expression, using <p></p> will destroy the form 
                                    # but a <br/> will do good

    # Distinctive element, the answer to a problem
    # Change an answer blank from [____] in PGML to the following in XML
    def p_answer (self,p):
        '''
        element : ANSWER
        '''
        self.answer_blank_count += 1 # To record the number of answer blanks and give each answer blank a distint ID
                                     # in order to match the answer ID which will appear in the code part before the text part  
        s = '''<numericalresponse answer="$answer'''+str(self.answer_blank_count)+'''">
                    <responseparam type="tolerance" default="1%" />
                    <formulaequationinput />
                </numericalresponse>\n'''
        p[0] = s

    # Error handling
    def p_error(self,p):
        raise TypeError("parse error:unknown text at %r %r" % (p.value,p.lineno))

    # Build the parser
    def build_parser(self):
        self.parser = yacc.yacc(module = self)

    #Test the parser
    def test_parser(self,data):
        result = self.parser.parse(data,lexer = self.lexer)
        return '<p>'+result + '</p>\n</problem>'

    # Return all answers to pass them to 'code' part
    def MyAnswer(self):
        return self.answers







