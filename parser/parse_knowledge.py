from enum import Enum
from dataclasses import dataclass
from collections import defaultdict
import sympy as sp
import networkx as nx
import re
import json
import os


class symbols(Enum):
    x = sp.Symbol('x')
    h = sp.Symbol('h')

@dataclass
class equations:
    values:list
    const_nums:float

def check_if_diff(f, symbols):
    a = 0

    left =  sp.limit((f.subs(symbols.x.value, a + symbols.h.value) - f.subs(symbols.x.value, a)) / symbols.h.value, symbols.h.value, 0, dir='-')
    right = sp.limit((f.subs(symbols.x.value, a + symbols.h.value) - f.subs(symbols.x.value, a)) / symbols.h.value, symbols.h.value, 0, dir='+')

    return left == right

def find_and_remove(string, sub):
    l_side = string.find(sub)
    r_side = string.find(sub)
    if l_side != -1 and r_side != -1:
        string = string[:l_side] + string[r_side:]

    return string

def parse_npl_(string:str):
    pattern = r'\$\$(.*?)\$\$'
    pattern_not_display = r'\$(.*?)\$'

    expressions = re.findall(pattern, string, re.DOTALL)


    for expr in expressions:
        string = find_and_remove(string, '$$'+expr+'$$')
    
    expressions_not_display = re.findall(pattern_not_display, string, re.DOTALL)
    expressions.extend(expressions_not_display)

    while '' in expressions:
        expressions.remove('')

    return expressions

class GraphGenerator:
    def __init__(self, max_n_nodes, n_connections_min):
        self.max_n_nodes = max_n_nodes
        self.n_connections_min = n_connections_min
        self.start = True
        self.graph = nx.DiGraph()

    @staticmethod
    def solve_problem_with_steps(problem:str):
        exprs = parse_npl_(problem)
        coefs = defaultdict(list)
        eqs = equations([], 0)

        for expr in exprs:
            expr = expr.replace(' ', '')
            for char in expr:
                if char.isalpha() and char != '':
                    pattern = r'([+-]?)(\d*\.\d+)' + re.escape(char)
                    strings = re.findall(pattern, expr, re.DOTALL)

                    for s in strings:
                        eqs.values.append(float((s[0]+s[1]).strip().replace(' ', ''))*sp.Symbol(char))



        print(eqs)
                    
        


if __name__ == '__main__':
    GraphGenerator.solve_problem_with_steps("""
    Given two equations $2.0x + 3.0y + 1.0 = 10$ and $3.0y - 1.0 = 2.0x$    
    Solve the problem.
""")
