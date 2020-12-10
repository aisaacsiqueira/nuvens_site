# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 22:51:37 2020

@author: alexa
"""

import nltk
from nltk.lm import MLE, Laplace
from nltk.lm.preprocessing import padded_everygram_pipeline
from nltk import word_tokenize, sent_tokenize
import pandas as pd
from pages.discursos import pre_processa_modelo
from pages.coleta import Coleta


def remove_palavras(palavras,texto):
    for palavra in palavras:
        texto = texto.replace(palavra,' ')
    return texto

def imprime_frase(treinado):
    texto = ''
    for palavra in treinado:
        if (str(palavra) != '<UNK>' or str(palavra) != "</s>" or str(palavra) != '<s>'):
            texto += str(palavra) + ' '
    return texto

def cria_modelo(deputado,max_palavras):
    c = Coleta(deputado=deputado[:deputado.find(',')],data_inicio='2019-01-01')
    discursos = c.coleta_discursos()
    agr = pre_processa_modelo(discursos)
    # texto = agr.loc[('Talíria Petrone','PSOL')]
    # texto = remove_palavras(['talíria','petrone'],texto)

    # texto = agr.loc[('Marcelo Freixo','PSOL')]
    texto = agr[(d[:d.find(',')],d[d.find(',')+2:])]
    texto = remove_palavras(deputado.split().lower(),texto)

    tk =  [list(map(str.lower, word_tokenize(sent))) for sent in sent_tokenize(texto)]


    train_data, padded_sents = padded_everygram_pipeline(3, tk)
    lm = MLE(3)
    lm.fit(train_data, padded_sents)

    # print(lm.generate(30, random_seed=10))


    random_s = 2
    import random

    texto_aleatorio = []

    while(len(texto_aleatorio) < max_palavras):
        
        treinado = lm.generate(100, random_seed= random.randint(0,100))
        random_s += 3
        for palavra in treinado:
            if(palavra != "</s>" and palavra != "<s>"):
                texto_aleatorio.append(palavra)
                print(palavra, end=' ')

    return imprime_frase(treinado)
