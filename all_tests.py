#!/usr/bin/env python3

ALL_MODULES = [
  'backend_objects',
  'db',
  'templater',
  'templater.nodes',
  'templater.node_parser',
]

import importlib
import doctest

for name in ALL_MODULES:
  mod = importlib.import_module(name)
  failure_count, test_count = doctest.testmod(mod)
  print(name, ': passed', test_count - failure_count, 'of', test_count, 'tests.')
