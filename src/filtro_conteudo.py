# coding: utf-8
from settings import PALAVRAS_BLOQUEADAS, DOMINIOS_BLOQUEADOS


def pesquisaPalavra(html):
    ''' Pesquisa palavras dentro de um conteúdo html'''
    arq = ''
    try:
        arq = open(PALAVRAS_BLOQUEADAS)
        for palavra in arq:
            palavra = palavra.strip()
            if palavra and palavra in html:
                return True
        return False
    except IOError:
        return False
    finally:
        arq.close()


def verificaDominio(host):
    '''Verifica se host tem permissão'''
    arq = ''
    try:
        arq = open(DOMINIOS_BLOQUEADOS)
        for dominio in arq:
            dominio = dominio.strip()
            if dominio and dominio == host:
                return True
        return False
    except IOError:
        return False
    finally:
        arq.close()
