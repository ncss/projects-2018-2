"""
___Thomas_The_Template_Engine___

      __        __________
     /  \         ========   _____________
      ||          =      =  /           ]
  ___==============      = /            ]
  \_[            ========= [            ]
    [=====================^==============
___//_(_)_(_)_(_)___\__/_____(_)_(_)_(_)
========================================

Syntax:

STATEMENT:
    {{text}}
    
    'text' will be evaluated in python with given context from DB
IF STATEMENT:
    {% if condition %}
    STUFF
    {%end if%}

    STUFF will be run if 'conditon'is true
FOR LOOP
    {$For item in list$}
    STUFF
    {$end for$}

    STUFF will run for each 'item' in 'list'.


Template Team:

Shovel "Constantine" Quazi
Ollie "Starfyre"
Ethan "Aquaman"
Jackson "Superman" 

    
"""

# Relative imports are hard...
try:
    from node_parser import *
except ImportError:
    from templater.node_parser import *

def render(file,context):
    '''Renders given html file'''
    with open(file) as f:
        return parse(f.read()).translate(context)
