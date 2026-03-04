import ply.lex as lex
import ply.yacc as yacc
import sys

# Defining tokens for the lexical analysis phase.
tokens = [
    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS'
]

# Regular expressions for our tokens. Order matters here.
t_PLUS = r'\+'
t_MINUS = r'\-'
t_DIVIDE = r'\/'
t_MULTIPLY = r'\*'
t_EQUALS = r'\='

t_ignore = r' '

# Functions for more complicated tokens. Order matters here too.
def t_FLOAT(t):
    r'\d\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'\d+' 
    t.value = int(t.value)
    return t

def t_NAME(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    t.type = 'NAME'
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'. Skipping!")
    t.lexer.skip(1)

lexer = lex.lex()

# Defining productions for the parsing step.
def p_calc(p):
    '''
    calc : expression
         | empty
    '''
    print(p[1])

def p_expression(p):
    '''
    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = p[1]

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

parser = yacc.yacc()

print("Welcome to the PLY calculator!")
while True:
    try:
        s = input("Enter a valid expression:\n")
    except EOFError:
        break
    parser.parse(s)