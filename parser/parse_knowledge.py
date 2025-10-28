import sympy as sp
import networkx as nx
import re
import json
import os

def parse_npl_(string:str):
    pattern = r'\$\$(.*?)\$\$'
    pattern_not_display = r'\$(.*?)\$'

    expressions = re.findall(pattern, string, re.DOTALL)


    for expr in expressions:
        l_side = string.find('$$' + expr + '$$')
        r_side = string.find('$$' + expr + '$$')
        if l_side != -1 and r_side != -1:
            string = string[:l_side] + string[r_side:]
    
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


if __name__ == '__main__':
    exprs = parse_npl_("$$2x+1=3$$" + " $A + B = C$ " + "$$2x+35=10$$")
    print(exprs)
