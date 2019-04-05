#!/usr/bin/env python
#! -*- encoding: utf8 -*-

"""
PAMG
"""

import sys
import json

def load_json(filename):
    with open(filename) as fh:
        obj = json.load(fh)
    return obj

q = False
e = False

if __name__ == "__main__":
    if len(sys.argv) >= 
