# code adapted from  https://gist.github.com/nava45/6333409#file-infix-expression-evaluation

import logging
import re

from xpression.tree import OP
from xpression.utils import Stack

_LOG = logging.getLogger(__name__)


class InvalidExpression(Exception):
    pass


class Parser(object):
    def __init__(self, op_set, eval_node_from_str, eval_binary_expression):
        self.op_set = op_set
        self.stack = Stack()

        class ParserOP(OP):
            @staticmethod
            def eval_node_from_str(s):
                return eval_node_from_str(s)

            @staticmethod
            def eval_binary_expression(lhs, operator=None, rhs=None):
                return eval_binary_expression(lhs, operator, rhs)

        self.op_class = ParserOP

    @staticmethod
    def maybe_wrap_in_brackets(expression):
        prev_test = expression
        while True:
            test = re.sub(r'\([^\(\)]+\)', '', prev_test)
            _LOG.debug('prev_test:%s test:%s', prev_test, test)
            if test == prev_test:
                break
            else:
                prev_test = test
        if test.strip():
            expression = '(' + expression + ')'
        return expression

    @staticmethod
    def split_brackets(token):
        word_buffer = []
        for c in token:
            if c == '(':
                yield c
            elif c == ')':
                if word_buffer:
                    yield ''.join(word_buffer)
                    word_buffer = []
                yield c
            else:
                word_buffer.append(c)
        if word_buffer:
            yield ''.join(word_buffer)

    @classmethod
    def tokenize(cls, expression):
        tokens = []
        for t in expression.split():
            for t1 in cls.split_brackets(t):
                tokens.append(t1)
        return tokens

    def eval_sub_expression(self, items):
        _LOG.debug('Evaluating the preceding items:%s', items)
        firstitem = items.pop()
        prevresult = firstitem
        while firstitem:
            try:
                if hasattr(firstitem, '__call__'):
                    prevresult = firstitem(prevresult, items.pop())
                firstitem = items.pop()
            except IndexError:
                return prevresult
        _LOG.debug('Evaluated Result is : %s', prevresult)
        return prevresult

    def pop_until_open_bracket(self):
        tlist = []
        item = self.stack.pop()
        eres = 0
        while not item == '(':
            if item:
                tlist.append(item)
                item = self.stack.pop()
            else:
                _LOG.warning('Insufficient items in stack')
                return
        return self.eval_sub_expression(tlist) if tlist else eres

    def get_op(self, operator):
        def operand_wrapper(lhs, rhs):
            return self.op_class.from_pair(lhs, rhs, operator)
        return operand_wrapper

    def get_parse_tree(self, expression):
        expression = self.maybe_wrap_in_brackets(expression)
        for token in self.tokenize(expression):
            if token == ')':
                self.stack.push(self.pop_until_open_bracket())
            elif token in self.op_set:
                self.stack.push(self.get_op(token))
            else:
                self.stack.push(token)
        if len(self.stack.data) != 1:
            raise InvalidExpression('unbalanced brackets')
        return self.stack.data[0]

    def parse(self, expression):
        tree = self.get_parse_tree(expression)
        return self.op_class.eval(tree)
