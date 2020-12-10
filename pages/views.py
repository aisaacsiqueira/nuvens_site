from django.shortcuts import render, redirect
from pages.info import partidos, deputados
from pages.coleta import Coleta
from pages.discursos import pre_processa
from pages.nuvens import Nuvens
from django.http import HttpResponse, FileResponse
import requests
import json
import base64, urllib
from io import BytesIO
from pages.mle import cria_modelo
# Create your views here.
def index(request):


    # p = {'dataInicio':'2019-01-01'}
    # r = requests.get('https://dadosabertos.camara.leg.br/api/v2/deputados', params=p)
    # texto = r.text

    # dicionario = json.loads(texto)
    # dados = dicionario['dados']
    # nomes = {}
    # partidos = []
    # for dado in dados:
    #     nomes[dado['id']] = dado['nome'] + ', '+ dado['siglaPartido']
    #     partidos.append(dado['siglaPartido'])
    # partidos = list(set(partidos))
    # partidos.sort()
    nomes = deputados
    context = {
        'nomes':nomes,
        'partidos':partidos,
    }

    return render(request,'pages/index.html',context)

def nuvem(request):
    # partido = request.GET.get('partido')
    partido = "Partidos"
    deputado = request.GET.get('deputado')
    inicio = request.GET.get('inicio')
    fim = request.GET.get('fim')
    cor_fundo = request.GET.get('cor_f')
    cor_letra = request.GET.get('cor_l')
    deletar = request.GET.get('palavras_deletar')
    deletar = deletar.lower().split()
    print(deletar)
    print(partido,deputado,inicio,fim)
    if deputado == 'Deputados' and partido == 'Partidos':
        return redirect('index')
    if deputado != 'Deputados':
        c = Coleta(deputado=deputado[:deputado.find(',')],data_fim=fim,data_inicio=inicio)
    if partido != 'Partidos':
        c = Coleta(partido=partido,data_fim=fim,data_inicio=inicio)


    discursos = c.coleta_discursos()
    if type(discursos) == str:
        # não há discursos para esse deputado
        print(discursos)
    else:
        discursos_processados = pre_processa(discursos)
        img_nuvens = {}
        palavras_deletar = ['fez','tudo','falar','ainda','disse','dar','lá','dizer','disso','assim','bem','boa','precisamos','portanto','brasil','têm','todo','fazer','brasileiro','brasileira','todos','vamos','sim','não','psl','pt','psol','país','lado','quer','brasileiro','partido','srs','sras','paulo','ganime','benedita','hatten']
        palavras_deletar.extend(deletar)
        for deputado in discursos_processados.keys():
            palavras_deletar.extend(deputado[0].lower().split())
            palavras_deletar.extend(deputado[1].lower().split())
            nuvem=Nuvens(cor_fundo = cor_fundo,cor_letra = cor_letra,max_palavras=100, nome_arquivo=str(deputado), documento =discursos_processados[deputado],palavras_deletar=palavras_deletar)
            r = nuvem.forma_nuvens()
            # response = HttpResponse(content_type="image/png")
            # r.save(response, "PNG")
            # return response


            buffered = BytesIO()
            r.save(buffered, format="png")
            img_str = base64.b64encode(buffered.getvalue())
            image_64 = 'data:image/png;base64,' + urllib.parse.quote(img_str)
            img_nuvens[deputado[0]] = image_64
        context = {
            'nomes':deputados,
            'partidos':partidos,
            'wordcloud':img_nuvens,

        }
        return render(request,'pages/index.html',context)

    return HttpResponse(r)

def modelo(request):
    deputado = request.GET.get('deputado')
    