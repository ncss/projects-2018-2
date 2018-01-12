#look for all tags (end and star ones) 
#text, python expr
import re
import node

def tokenise(text):
  """
  >>> tokenise('<h1>{{ person.name }} is {{ person.age }}</h1>')
  ['<h1>', '{{ person.name }}', ' is ', '{{ person.age }}', '</h1>']
  >>> tokenise("<ul id='friends-list'>")
  ["<ul id='friends-list'>"]
  >>> tokenise('{% if f.has_nickname() %} ({{ f.nickname }}) {% end if %}')
  ['', '{% if f.has_nickname() %}', ' (', '{{ f.nickname }}', ') ', '{% end if %}', '']
  """
  return re.split(r'({{.+?}}|{%.+?%})', text)

def parse(text):
  tokens = tokenise(text)
  parsed = []
  for token in tokens:
    if token[:2] == "{{" and token[-2:] == "}}":
      token = token[2:-2].strip()
      parsed.append(node.ExprNode(token))
    else:
      parsed.append(node.TextNode(token))
  groupNode = node.GroupNode(parsed)
  return groupNode

if __name__ == '__main__':
  import doctest
  doctest.testmod()
