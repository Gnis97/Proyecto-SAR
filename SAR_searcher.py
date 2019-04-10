#!/usr/bin/env python
#! -*- encoding: utf8 -*-

"""

Requesitos:

    2 argumentos: 1º indicie (2º querry)
    Si solo hay un argumento bucle.
    Salida  para 1-2 resltados fecha titulo keywords y cuerpo
    Operdores and or not izquierda a aderecha
    3-5 fecha titular keywords y snippet(tienen que estar la querry)
    +5 fecha titular keywords de las 10 priemeras y un noticia por liena
    Siempre se mostrara en nombre del fichero que contiene la noticia y numero
    total de notiias.

"""

import sys
import json
import pickle

def load_object(file_name):
    with open (file_name, 'rb') as fh:
        obj = pickle.load(fh)
    return obj

def load_json(filename):
    with open(filename) as fh:
        obj = json.load(fh)
    return obj

def parsequerry(que):
    que.lower()
    que = que.split()
    return que

def consulta(in, q):
    operador = -1
    res = None
    in = load_object(in)
    q = parsequerry(q)
    for t in q:
        if res == None:
            res = in[t]
        else:
            if t == "AND":
                operador = 1
                break
            if t == "OR":
                operador = 2
                break
            if t == "NOT":
                if operador > 0:
                    operador = operador*10
                else:
                    operador = 3
                break

            if operador == 1:
                aux = in[t]
                res = intersection(res, aux)
            if operador == 2:
                aux = in[t]
                res = union(res, aux)
            if operador == 3:
                aux = in[t]
                res = diferencia(in, in[t])
            if operador == 10:
                aux = diferencia(in, in[t])
                res = intersection(res, aux)
            if operador == 20:
                aux = diferencia(in, in[t])
                res = union(res, aux)
            operador = -1
    return res

def intersection(p1,p2):
	res = []
	i = 0
	j = 0
	p1.sort()
	p2.sort()
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
	p1.sort()
	p2.sort()
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

def diferencia(dic,p2):
	res = []
	for k,v in dic:
		for e in v:
			if e not in p2:
				res.append(e)
	return res


if __name__ == "__main__":
    querry = None
    resultado = None
    if len(sys.argv) >= 2:
        findi = sys.argv[1]
        if len(sys.argv) >= 3:
            querry = sys.argv[2]
        if querry != None:
            resultado = consulta(findi, querry)
            mostrar(resultado)
        else:
            while True:
                text = input("Dime:")
                if len(text) == 0:
                    break
                querry = text
                resultado = consulta(findi, querry)
                mostrar(resultado)
