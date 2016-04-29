# coding: utf-8
from settings import PALAVRAS_BLOQUEADAS, DOMINIOS_BLOQUEADOS


def pesquisaPalavra(html):
    ''' Pesquisa palavras dentro de um conteúdo html'''
    achou = False
    try:
        arq = open(PALAVRAS_BLOQUEADAS)
        for palavra in arq:
            palavra = palavra.strip()
            if palavra and palavra in html:
                achou = True
                break
        arq.close()
        return achou
    except IOError:
        return False


def verificaDominio(host):
    '''Verifica se host tem permissão'''
    achou = False
    try:
        arq = open(DOMINIOS_BLOQUEADOS)
        for dominio in arq:
            dominio = dominio.strip()
            if dominio and dominio == host:
                achou = True
                break

        arq.close()
        return achou
    except IOError:
        return False
