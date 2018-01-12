"""
>>> node_1 = TextNode("TEST 1 ")
>>> context = {"variable":"TEST 2"}
>>> node_2 = ExprNode("variable")
>>> node_3 = GroupNode([node_1,node_2])
>>> node_3.translate(context)
'TEST 1 TEST 2'
"""


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
        return eval(self._string,context) #MAY NEED CHANGE BASED ON SYNTAX


if __name__ == '__main__':
    import doctest
    doctest.testmod()
