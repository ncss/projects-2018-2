#look for all tags (end and star ones) 
#text, python expr
import re
text = """
{% include header.html %}
<section id='profile'>
<h1>{{ person.name }}</h1>
<ul id='friends-list'>
{% for f in person.friends %}
<li class='friend'>
{{ f.name.title() }} {{ f.age }} {% if f.has_nickname() %} ({{ f.nickname }}) {% end if %}
</li>
{% end for %}
</ul>
</section>
{% include footer.html %}
"""

##tokens = []
##for i in text.split():
##  i = re.split(r'({{.+?}})', text)
##  if i[:2] == "{{":
##    tokens.append(i)  	

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




if __name__ == '__main__':
  import doctest
  doctest.testmod()
