# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 18:47:50 2020

@author: alexa
"""
from nltk import FreqDist
import nltk
import re
from wordcloud import WordCloud
# from nltk.collocations import *
nltk.download('stopwords')
# texto.pop(0)

class Nuvens(object):
    
    def __init__(self,max_palavras=100, nome_arquivo="NuvemDePalavras", documento ='', palavras_deletar = [], cor_fundo = (47, 39, 220),cor_letra=(162, 220, 39)):
        self.max_palavras = max_palavras
        self.nome_arquivo = nome_arquivo
        self.documento = documento
        self.palavras_deletar = palavras_deletar
        self.cor_fundo =cor_fundo
        self.cor_letra = cor_letra

        self.stopwords = nltk.corpus.stopwords.words('portuguese')
        self.stopwords.extend(['hoje','exa','ex','v','falou','hoje','agora','pessoa','pessoas','obrigado','obrigada','vai','quero','queria','neste','naquele','pode','daqueles','sobre','nesta','acho','presidente','deputado','deputados','ter','ser','tão','então','dia','porque','aqui','casa'])
        self.stopwords.extend(palavras_deletar)
        
    def forma_ngrama(self):
        documento = self.documento.split()
        doc_stop = []
        for palavra in documento:
            if palavra not in self.stopwords:
                doc_stop.append(palavra)
        
        bigrama = nltk.bigrams(doc_stop)
        
        frequenciaB = FreqDist(bigrama)
        frequenciaB = dict(frequenciaB)

        dicionario = {}
        for word in frequenciaB:
            palavra = word[0]+ '_' +word[1]
            dicionario[palavra] = int(frequenciaB[word])
            
        
        
        frequencia = FreqDist(doc_stop)
        frequencia = dict(frequencia)
        d = {}

        for p in frequencia:
            d[p] = int(frequencia[p])
        
        
        for w in d:
            dicionario[w] = d[w]
        
        nuvemdepalavras = WordCloud(width=800,height=600,min_word_length=3,max_words = self.max_palavras,background_color=self.cor_fundo,color_func=lambda *args, **kwargs: self.cor_letra)
        nuvemdepalavras.fit_words(dicionario)
        nuvemdepalavras.to_file(self.nome_arquivo+"Ngrama.png")
    
    def forma_nuvens_bigrama(self):
        documento = self.documento.split()
        
        doc_stop = []
        for palavra in documento:
            if palavra not in self.stopwords:
                doc_stop.append(palavra)
                
        bigrama = nltk.bigrams(doc_stop)
        
        frequencia = FreqDist(bigrama)
        frequencia = dict(frequencia)
        dicionario = {}
        for word in frequencia:
            palavra = word[0]+ '_' +word[1]
            dicionario[palavra] = frequencia[word]
    
        nuvemdepalavras = WordCloud(width=800,height=600,min_word_length=3,max_words = self.max_palavras,background_color=(47, 39, 220),color_func=lambda *args, **kwargs: (162, 220, 39))
        nuvemdepalavras.fit_words(dicionario)
        nuvemdepalavras.to_file(self.nome_arquivo+"Bigrama.png")
    
   
    def forma_nuvens(self):
        '''
        max_palavras: inteiro com o numero maximo de palavras
        
        '''

        documento = self.documento.split()

        # texto_stop = []
        # for palavra in documento:
        #     if palavra not in stopwords:
        #         texto_stop.append(palavra)
        
        # bigrama = nltk.bigrams(texto_stop)
        
        # frequencia = FreqDist(bigrama)
        # frequencia = dict(frequencia)
        frequencia = FreqDist(documento)
        frequencia = dict(frequencia)
        for palavra in self.stopwords:
            try:
                del frequencia[palavra]
            except:
                pass
        
        
        nuvemdepalavras = WordCloud(width=800,height=600,min_word_length=3,max_words = self.max_palavras,background_color=self.cor_fundo,color_func=lambda *args, **kwargs: self.cor_letra)
        nuvemdepalavras.fit_words(frequencia)
        
        return nuvemdepalavras.to_image()
        # nuvemdepalavras.to_file(self.nome_arquivo+".png")



