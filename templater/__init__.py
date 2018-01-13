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

    {{text}}

2 curly boys on each end mark a /node/ where 'text' will be evaluated in python with given context from DB

    {^IF(statement)}      {^END}

    
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
