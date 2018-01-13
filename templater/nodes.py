"""
>>> node_1 = TextNode("TEST 1 ")
>>> context = {"variable":"TEST 2"}
>>> node_2 = ExprNode("variable")
>>> node_3 = GroupNode([node_1,node_2])
>>> node_3.translate(context)
'TEST 1 TEST 2'
>>> forList = '[1,2,3,4,5,6,7,8,9]'
>>> del context["variable"]
>>> node_4 = ForNode(forList, "variable", node_3)
>>> node_4.translate(context)
'TEST 1 1TEST 1 2TEST 1 3TEST 1 4TEST 1 5TEST 1 6TEST 1 7TEST 1 8TEST 1 9'
>>> if_node = IfNode("x == 3", node_3)
>>> if_node.translate({'x': 3, 'variable': 'TEST 2'})
'TEST 1 TEST 2'
>>> if_node.translate({'x': 2, 'variable': 'TEST 2'})
''
>>> with open('eg1.html', 'w') as f: print('<html><head>{{ var }}</head>', file=f, end='')
>>> IncludeNode('eg1.html').translate({'var': 123})
'<html><head>123</head>'
"""

# Relative imports are hard...
try:
  import node_parser
except ImportError:
  from . import node_parser


class Node:
    """Basic Node Structure"""
    def __init__(self,string):
        self._string = string

class GroupNode(Node):
    """A GroupNode contains more Nodes"""
    def __init__(self,nodeList):
        self._nL = nodeList
    def translate(self,context):
        final = ''
        for node in self._nL:
            final += node.translate(context)
        return final

class TextNode(Node):
    """Creates a TextNode which contains nothing to edit"""
    def translate(self,context):
        return self._string

class ExprNode(Node):
    """Creates an Expression Node which contains python code to evaluate"""
    def translate(self,context):
        return str(eval(self._string,context))
class IfNode(Node):
    """An IfNode contains a statement and the required node"""
    def __init__(self,condition,statement):
        self._cond = condition
        self._stat = statement
    def translate(self,context):
        if eval(self._cond,context):
            return self._stat.translate(context)
        else:
            return ''
class ForNode(Node):
    """A For Node that contains a statement and the required node"""

    def __init__(self,iterable,item_name,statement):
        self._iter = iterable
        self._stat = statement
        self._name = item_name

    def translate(self,context):
        return_string = ''
        for item in eval(self._iter,context):
            context[self._name] = item
            return_string += self._stat.translate(context)
              
        del context[self._name]
        return return_string

class IncludeNode(Node):
    def translate(self,context):
        with open(self._string) as f:
            return node_parser.parse(f.read()).translate(context)

if __name__ == '__main__':
    import doctest
    fail_count, test_count = doctest.testmod()
    print('Passed', test_count - fail_count, 'of', test_count, 'tests.')
