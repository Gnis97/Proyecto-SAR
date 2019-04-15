#!/usr/bin/env python
#! -*- encoding: utf8 -*-

import json
import pickle
import re
import sys
import os

# cada doc: {'article': ' ','url' 'date' 'keywords' 'id': '', 'summary': '', 'title':''}, {'article'...
#guardar un objecte(índex) en un fitxer
def save_object(object, file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)
        
clean_re = re.compile('\W+')

def clean_text(text):
    return clean_re.sub(' ', text)
    
    

def indexer(folder,fitxerGuardat):

    dDocs = {}
    dArticles = {}
    postingListTerms = {} #cada termino: lista de id de las noticias en que aparece
    for dirname, subdirs, files in os.walk(folder): #"paseja" per la carpeta
        for filename in files: #agafa els fitxers
            wholeName = os.path.join(dirname,filename)
            with open(wholeName) as json_file:
                ob = json.load(json_file)#carrega el fitxer
            dDocs[len(dDocs)] = wholeName #afig el fitxer al diccionari de fitxers
            pos = 0
            for noti in ob:
                tupla = [len(dDocs),pos]
                pos +=1
                
                dArticles[len(dArticles)] = tupla
                text = noti["article"]
                text = text.lower()
                text = clean_text(text)
                text = text.replace("\n"," ")
                text = text.replace("\t"," ")
                text = text.split()
            
                for simb in text:
                    #if simb in lletres or simb in nums:
                    postingListTerms[simb] = postingListTerms.get(simb,[])
                    if postingListTerms[simb] == [] :
                        postingListTerms[simb] = [len(dArticles)]
                    else :
                        var = len(postingListTerms[simb])
                        lista = postingListTerms[simb]
                        if len(dArticles) > lista[var-1]: #si el article que estem procesant es major que el ultim inserit vol dir que no esta
                            postingListTerms[simb] = postingListTerms.get(simb) + [len(dArticles)]
    objecte = [dDocs, dArticles, postingListTerms]
    save_object(objecte, fitxerGuardat)
    
    
    
'''El fichero invertido puede ser una tabla hash implementada como un diccionario de
    python, indexado por término y que haga referencia a una lista con los newid
    asociados a ese término.'''

'''La mejor forma de guardar los datos de los índices en disco es utilizar la librería pickle
    que permite guardar un objeto python en disco. Si quieres guardar más de un objeto,
    puedes hacer una tupla con ellos, (obj1, obj2, …, objn), y guardar la tupla. Consulta la
    práctica del mono infinito.'''
    #Toda la información necesaria para el recuperador de noticias se guardará en un único
    #fichero en disco.


'''Aceptará dos argumentos de entrada: el primero el directorio donde está la colección
de noticias y el segundo el nombre del fichero donde se guardará el índice.'''
if __name__ == "__main__":
    if len(sys.argv) == 3:
        colNot = ""
        colNot += sys.argv[1]
        savIndx = sys.argv[2]
        indexer(colNot, savIndx)
    else:
        syntax()
        