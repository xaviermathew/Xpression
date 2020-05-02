import operator as builtin_operator

from xpression.parser import Parser

op_map = {
    '+': builtin_operator.add,
    '-': builtin_operator.sub,
    '*': builtin_operator.mul,
    '/': builtin_operator.div,

}


def eval_node_from_str(s):
    return int(s)


def eval_binary_expression(lhs, operator, rhs):
    if operator and rhs:
        return op_map[operator](lhs, rhs)
    else:
        return lhs


def parse(expression):
    parser = Parser(op_set=op_map.keys(),
                    eval_node_from_str=eval_node_from_str,
                    eval_binary_expression=eval_binary_expression)
    return parser.parse(expression)


q = '((1 + 1) * (2 + 2)) / ((5 + 2) + 1)'
print parse(q)
