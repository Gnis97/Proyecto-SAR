#!/usr/bin/env python
#! -*- encoding: utf8 -*-

"""

Requesitos:

    2 argumentos: 1º indicie (2º querry)
    PREPARADO Si solo hay un argumento bucle.
    PREPARADO Operdores and or not izquierda a aderecha
    PREPARADO Salida  para 1-2 resltados fecha titulo keywords y cuerpo
    PREPARADO 3-5 fecha titular keywords y snippet(tienen que estar la querry)
    PREPARADO +5 fecha titular keywords de las 10 priemeras y un noticia por liena
    Siempre se mostrara en nombre del fichero que contiene la noticia y numero
    PREPARADO total de notiias.

"""
import re
import sys
import json
import pickle

termsnip = []
conparent = []
numparent = 0
findi = None

clean_re = re.compile('\W+')

def clean_text(text):
    return clean_re.sub(' ', text)

def load_object(file_name):
    with open (file_name, 'rb') as fh:
        obj = pickle.load(fh)
    return obj

def load_json(filename):
    with open(filename) as fh:
        obj = json.load(fh)
    return obj

def gensnippet(ar):
    listindi = [] #Lista donde se guardan los indices de los terminos de la querry
    ressnip = ""
    ar = ar.lower()
    ar = clean_text(ar)
    ar = ar.replace("\n"," ")
    ar = ar.replace("\t"," ")
    ar = ar.split()# Separamos el articulo en una lista de plabras
    for t in termsnip:# Para cada termino de la querry obtenermos su primer indice en el articulo
        listindi.append(ar.index(t))
    listindi.sort()
    for x in listindi:# Creamos el snippet obteniendo pedazos de texto de longitud 9 teniendo los terminos en el medio
        inn = max((x-4),0)# Evitamos salirnos del array
        fi = min((x+5),len(ar))# Evitamos salirnos del array
        ressnip = ressnip + " " + "..." + " ".join(ar[inn:fi]) + "..."
    return ressnip

def parsequerry(que):#Pasamos a minuscula y semaparamos la querry
    que = que.lower()
    que = que.split()
    auxque = []
    inn = -1
    cun = 0
    for e in que:
        if '"' in e:
            if inn == -1:
                inn = cun
            else:
                auxque.append(" ".join(que[inn:cun+1]))
                inn = -1
        else:
            if inn == -1:
                auxque.append(e)
        cun += 1
    que = auxque
    return que

def parentesis(quensulta):
    primer = -1
    ulti = -1
    cont = 0
    while cont < len(quensulta) and ulti == -1:
        if (quensulta[cont] == "("):
            primer = cont
        if (quensulta[cont] == ")"):
            ulti = cont
        cont += 1
    if primer == -1:
        return quensulta, 1
    nuevaq = quensulta[primer+1:ulti]
    cambio = "rexultadio" + str(len(conparent))
    conparent.append(consulta(findi, nuevaq))
    quensulta = quensulta.replace(quensulta[primer:ulti+1], cambio)
    return quensulta, 0

def posicional(ttt):
    ttt = ttt.replace('"', "")
    ttta = ttt.replace(" ", " and ")
    rrr = consulta(findi, ttta)
    k = len(rrr)
    dicDoc = findi[0]
    dicArt = findi[1]
    c = 0
    resulteido = []
    while c < k:#falta obtener los objetos
        ndoc,posdoc = dicArt[rrr[c]]
        with open(dicDoc[ndoc]) as json_file:
            ob = json.load(json_file)
        arti = ob[posdoc]
        if ttt in arti["article"]:
            resulteido.append(rrr[c])
        c += 1
    return resulteido

def procesarTermino(tt):
    if "article:" in tt:
        return tt.replace("article:",""), 2
    if "title:" in tt:
        return tt.replace("title:",""), 3
    if "summary:" in tt:
        return tt.replace("summary:",""), 4
    if "keywords:" in tt:
        return tt.replace("keywords:",""), 5
    if "date:" in tt:
        return tt.replace("date:",""), 6
    return tt, 2
"""
Se recorrera la querry detectando los operadores booleanos y realizando las
operaciones interseccion, union y diferencia requeridas.
1 = and, 2 = or, 3 = not, 10 = and not, 20 = or not
"""
def consulta(ind, q):
    aux = None
    flag = 0
    while flag == 0:
        q,flag = parentesis(q)
    operador = -1
    res = []
    inda = ind[1]
    q = parsequerry(q)
    for t in q:# Recorrremos la querry
        print("TERMINO: ", t)
        t,lugbus = procesarTermino(t) # te devuelve el termino limpio y el diccionario en el que tienes que bucar
        if len(res) == 0 and not t == "not" and not t == "and" and not t == "or" and operador == -1:
            print("PRIMER TERMINO")
            if "rexultadio" in t:
                aux = conparent[int(t.replace("rexultadio",""))]
            elif '"' in t:
                aux = posicional(t)
            else:
                aux = ind[lugbus].get(t,[]) #************************************************
            if aux is not []:
                res += aux
                if "rexultadio" not in t:
                    termsnip.append(t)
        else:
            if(t == "and" or t == "or" or t == "not"):
                if t == "and": #es una and
                    print("HE ENCONTRADO UN AND")
                    operador = 1
                if t == "or":
                    print("HE ENCONTRADO UN OR")
                    operador = 2
                if t == "not":
                    print("HE ENCONTRADO UN NOT")
                    if operador > 0:
                        print("NOT DOBLE")
                        operador = operador*10
                    else:
                        print("NOT SIMPLE")
                        operador = 3
            else:
                if operador == 1:
                    print("HE APLICADO UN AND")
                    if "rexultadio" in t:
                        aux = conparent[int(t.replace("rexultadio",""))]
                    elif '"' in t:
                        aux = posicional(t)
                    else:
                        aux = ind[lugbus].get(t,[]) #*******************************************************************
                    if aux is not []:
                        termsnip.append(t)
                    res = intersection(res, aux)
                if operador == 2:
                    print("HE APLICADO UN OR")
                    if "rexultadio" in t:
                        aux = conparent[int(t.replace("rexultadio",""))]
                    elif '"' in t:
                        aux = posicional(t)
                    else:
                        aux = ind[lugbus].get(t,[]) #********************************************************************
                    if aux is not []:
                        termsnip.append(t)
                    res = union(res, aux)
                if operador == 3:
                    print("HE APLICADO UN NOT")
                    if "rexultadio" in t:
                        aux = conparent[int(t.replace("rexultadio",""))]
                    elif '"' in t:
                        aux = posicional(t)
                    else:
                        aux = ind[lugbus].get(t,[]) #*********************************************************************
                    res = diferencia(inda, aux)
                if operador == 10:
                    print("HE APLICADO UN AND NOT")
                    if "rexultadio" in t:
                        aux = conparent[int(t.replace("rexultadio",""))]
                    elif '"' in t:
                        aux = posicional(t)
                    else:
                        aux = ind[lugbus].get(t,[]) #*********************************************************************
                    aux = diferencia(inda, aux)
                    res = intersection(res, aux)
                if operador == 20:
                    print("HE APLICADO UN OR NOT")
                    if "rexultadio" in t:
                        aux = conparent[int(t.replace("rexultadio",""))]
                    elif '"' in t:
                        aux = posicional(t)
                    else:
                        aux = ind[lugbus].get(t,[]) #**********************************************************************
                    aux = diferencia(inda, aux)
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
        i+=1
    while j < len(p2):
        ep2 = p2[j]
        res.append(ep2)
        j+=1
    return  res

def diferencia(dic,p2):
    res = []
    for k,_ in dic.items():
        if k not in p2:
                res.append(k)
    return res

def mostrar(r, ind):
    dicDoc = ind[0]
    dicArt = ind[1]
    m = (0,0,0,0,0) #{fecha, titulo ,keywords, cuerpo, snippet}
    k = len(r)
    if(k == 0):
        print("No se han encontrado resultados\n")
    if(k == 1 or k == 2):
        m = (1,1,1,1,0)
    if(3 <= k and k <= 5):
        m = (1,1,1,0,1)
    if(5 < k):
        k = min(len(r), 10)
        m = (1,1,1,0,0)
    c = 0
    print("Numero de resultados: ", len(r))
    while c < k:#falta obtener los objetos
        ndoc,posdoc = dicArt[r[c]]
        with open(dicDoc[ndoc]) as json_file:
            ob = json.load(json_file)
        arti = ob[posdoc]
        p = ""
        if m[0]:
            p = p + arti["date"] + " "
        if m[1]:
            p = p + arti["title"] + " "
        if m[2]:
            p = p + arti["keywords"] + " "
        if m[3]:
            p = p + arti["article"] + " "
        if m[4]:
            p = p
            #p = p + gensnippet(arti["article"]) + " "
        print(p)
        c = c+1
    print("Numero de resultados: ", len(r))

if __name__ == "__main__":
    querry = None
    resultado = None
    if len(sys.argv) >= 2:
        findi = sys.argv[1] #indice
        findi = load_object(findi)#(diccionario de documentos, diccionario de articulos, diccionario de terminos)
        if len(sys.argv) >= 3:
            querry = sys.argv[2] #querry
        if querry != None:
            if '"' in querry:
                print("yes")
            resultado = consulta(findi, querry)
            mostrar(resultado, findi)
        else:
            while True:
                termsnip = []
                conparent = []
                numparent = 0
                text = input("Dime:")
                if len(text) == 0:
                    break
                querry = text
                print(querry)
                resultado = consulta(findi, querry)
                mostrar(resultado, findi)
