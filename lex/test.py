from lexer import *

file = open('poker_problem_2.pg')
data = file.read()

lex.input(data)

output = open('output.txt','w')

for tok in iter(lex.token, None):
    output.write(str(repr(tok.type))+str(repr(tok.value))+'\n')