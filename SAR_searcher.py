#!/usr/bin/env python
#! -*- encoding: utf8 -*-

import sys
import json

def load_json(filename):
    with open(filename) as fh:
        obj = json.load(fh)
    return obj
    
def intersection(p1,p2):
	res = []
	i = 0
	j = 0
	while i < len(p1) and  j < len(p2):
		ep1 = p1[i]
		ep2 = p2[j]
		if ep1 == ep2:
			res.append(ep1)
			i+=1
			j+=1
		else:
			if ep1 < ep2:
				i+=1
			else:
				j+=1
	return res

def union(p1,p2):
	res = []
	i = 0
	j = 0
	while i < len(p1) and  j < len(p2):
		ep1 = p1[i]
		ep2 = p2[j]
		if ep1 == ep2:
			res.append(ep1)
			i+=1
			j+=1
		else: 
			if ep1 < ep2:
				res.append(ep1)
				i+=1
			else:
				res.append(ep2)
				j+=1
	while i < len(p1):
		ep1 = p1[i]
		res.append(ep1)
	while j < len(ep2):
		ep2 = p2[j]
		res.append(ep2)
	return  res
	
def diferencia(p1,p2): "(p1 not p2)"
	i = 0
	j = 0
	if len(p1) > len(p2):
		res = p1
	else:
		res = p2
	while i < len(p1) and  j < len(p2):
		ep1 = p1[i]
		ep2 = p2[j]
		if ep1 == ep2:
			res.remove(ep1)
			j+=1
		else:
			if ep1 < ep2:
				i+=1
			else:
				j+=1
	return res
	
q = False
e = False

if __name__ == "__main__":
if len(sys.argv) >= 555

