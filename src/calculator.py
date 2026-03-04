import ply.lex as lex
import ply.yacc as yacc
import sys

# Defining tokens for the lexical analysis phase
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