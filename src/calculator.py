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
    r'-?\d+' 
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

# Giving higher precedence to MULTIPLY and DIVIDE.
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

# Defining productions for the parsing step.
def p_calc(p):
    '''
    calc : expression
         | var_assign
         | empty
    '''
    value = run(p[1])
    if value != None:
        print(value)

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    '''
    p[0] = (p[2], p[1], p[3])

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

def p_expression_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    print("Syntax error found!")

parser = yacc.yacc()
env = {}

# Execute the calculator actions.
def run(p):
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '=':
            env[p[1]] = run(p[2])
        elif p[0] == 'var':
            if p[1] not in env:
                print(f"Undeclared variable '{p[1]}'")
            else:
                return env[p[1]]
    else:
        return p

print("Welcome to the PLY calculator!")

while True:
    try:
        s = input(">> ")
    except EOFError:
        break
    parser.parse(s)