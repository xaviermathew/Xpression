class OP(object):
    def __init__(self, s, rhs=None, operator=None):
        self.s = s
        self.rhs = rhs
        self.operator = operator

    def __repr__(self):
        if self.rhs is None:
            return '(%s)' % self.s
        else:
            return '(%s) %s (%s)' % (self.s, self.operator, self.rhs)

    __str__ = __repr__

    __unicode__ = __repr__

    def copy(self):
        return OP(s=self)

    def from_children(self, rhs, operator):
        if rhs is None:
            raise ValueError('rhs cant be none')
        if operator is None:
            raise ValueError('operator cant be none')
        new_op = self.copy()
        new_op.rhs = rhs
        new_op.operator = operator
        return new_op

    @staticmethod
    def from_pair(x, y, operator):
        if not isinstance(x, OP):
            x = OP(x)
        if not isinstance(y, OP):
            y = OP(y)
        return x.from_children(y, operator)

    @staticmethod
    def eval_node_from_str(s):
        raise NotImplementedError

    @staticmethod
    def eval_binary_expression(lhs, operator=None, rhs=None):
        raise NotImplementedError

    @classmethod
    def eval_node(cls, s):
        if isinstance(s, basestring):
            return '(%s)' % cls.eval_node_from_str(s)
        else:
            return '(%s)' % cls.eval(s)

    @classmethod
    def eval(cls, op):
        results = [cls.eval_node(op.s)]
        if op.rhs:
            results.append(op.operator)
            results.append(cls.eval_node(op.rhs))
        return cls.eval_binary_expression(*results)
