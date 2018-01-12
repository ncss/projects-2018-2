

class Node:
    """Basic Node Structure"""
    def __init__(self,string):
        self._string = string

class GroupNode(Node):
    """A GroupNode contains more Nodes"""
    def __init__(self,nodeList):
        self._nL = nodeList
    def translate(self):
        final = ''
        for node in self._nL:
            final += node.translate()
        return final

class TextNode(Node):
    """Creates a TextNode which contains nothing to edit"""
    def translate(self):
        return self._string

class ExprNode(Node):
    """Creates an Expression Node which contains python code to evaluate"""
    def translate(self):
        return eval(self._string[2:-2]) #MAY NEED CHANGE BASED ON SYNTAX

