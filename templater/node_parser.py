'''
>>> text = '<h1>{{ var }}</h1>{{ var2 }}</html>'
>>> tokens = tokenise(text)
>>> p = Parser(tokens)
>>> p = Parser(tokens)
>>> node = p.parse_group()
>>> node.translate({'var': 'a', 'var2': 'b'})
'<h1>a</h1>b</html>'

>>> text = '{% if x == 1 %}Yes{%end if%}'
>>> tokens = tokenise(text)
>>> p = Parser(tokens)
>>> node = p.parse_group()
>>> node.translate({'x': 1})
'Yes'
>>> node.translate({'x': 0})
''
'''
import re

# Relative imports are hard...
try:
  import nodes
except ImportError:
  from . import nodes

def tokenise(text):
  """
  >>> tokenise('<h1>{{ person.name }} is {{ person.age }}</h1>')
  ['<h1>', '{{ person.name }}', ' is ', '{{ person.age }}', '</h1>']
  >>> tokenise("<ul id='friends-list'>")
  ["<ul id='friends-list'>"]
  >>> tokenise('{% if f.has_nickname() %} ({{ f.nickname }}) {% end if %}')
  ['', '{% if f.has_nickname() %}', ' (', '{{ f.nickname }}', ') ', '{% end if %}', '']
  """
  return re.split(r'({{.+?}}|{%.+?%}|{\$.+?\$}|{~.+?~})', text) ##

END_IF_TAG = r'^{%\s*end if\s*%}$'
END_FOR_TAG = r'^{\$\s*end for\s*\$}$'
INCLUDE_TAG = r'^{~\s*include\s+(.+?)\s*~}$'
EXPRESSION_TAG = r'^{{\s*(.+)\s*}}$'

class Parser():
  
  def __init__(self, tokens):
    self._tokens = tokens
    self._length = len(tokens)
    self._upto = 0
    
  def parse_group(self): #turns tokens into a groupnode
    group_ofNodes = []
    while not (self.end() or re.match(END_IF_TAG, self.peek()) or re.match(END_FOR_TAG, self.peek())):
      node = self.parse_expr()
      if node == None:
        node = self.parse_if()
      if node == None:
        node = self.parse_for()
      if node == None:
        node = self.parse_include()
      if node == None:
        node = self.parse_text()
      group_ofNodes.append(node)
      
    return nodes.GroupNode(group_ofNodes)


  def end(self): #returns tru if at end of string
    return self._upto == self._length

  def peek(self): #returns the current token
    return None if self.end() else self._tokens[self._upto]

  def next(self):
    if not self.end():
      self._upto += 1

  def parse_text(self):
    text = self.peek()
    self.next()
    return(nodes.TextNode(text))
  
  def parse_expr(self): #translates token into node.        node translates into html beauty
    someVariable = re.match(EXPRESSION_TAG, self.peek())
    if someVariable:
      text = someVariable.group(1)
      self.next()
      return(nodes.ExprNode(text))
    else:
      return None

  def parse_if(self): #translates token into node.        node translates into html beauty
    someVariable = re.match(r"^{%\s*if\s+(.+)%}$", self.peek())
    if someVariable: #if current val is expr node
      text = someVariable.group(1)
      
      self.next()  
      group = self.parse_group()
      if re.match(END_IF_TAG, self.peek()):
        self.next()
      else:
        raise SyntaxError("If doesn't have a corresponding end if! What's the deal man/woman?")
      return nodes.IfNode(text, group)
    else:
      return None

  def parse_for(self): #translates token into node.        node translates into html beauty
    someVariable = re.match(r"^{\$\s*for\s+(.+)\s+in\s+(.+)\$}$", self.peek())
    if someVariable: #if current val is expr node
      iterable = someVariable.group(2)
      itemName = someVariable.group(1)
      self.next()  
      group = self.parse_group()
      if re.match(END_FOR_TAG, self.peek()):
        self.next()
      else:
        raise SyntaxError("For doesn't have a corresponding end for! What's the deal man/woman?")
      return nodes.ForNode(iterable, itemName, group)
    else:
      return None

  def parse_include(self):
    someVariable = re.match(INCLUDE_TAG, self.peek())
    if someVariable:
      text = someVariable.group(1)
      self.next()
      return(nodes.IncludeNode(text))
    else:
      return None


  

def parse(text):
  tokens = tokenise(text)
  p = Parser(tokens)
  
  groupNode = p.parse_group()
  if not p.end():
    raise SyntaxError("Unexpected token: " + str(p.peek()))
  return groupNode

if __name__ == '__main__':
  import doctest
  fail_count, test_count = doctest.testmod()
  print('Passed', test_count - fail_count, 'of', test_count, 'tests.')
