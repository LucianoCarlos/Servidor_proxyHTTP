# coding: utf-8
from settings import PALAVRAS_BLOQUEADAS, DOMINIOS_BLOQUEADOS


def pesquisaPalavra(html):
    ''' Pesquisa palavras dentro de um conteúdo html '''
    arquivo = html.upper()
    try:
        with open(PALAVRAS_BLOQUEADAS) as arq:
            for palavra in arq:
                palavra = palavra.strip()
                if palavra and palavra.upper() in arquivo:
                    print 'Palavra bloqueada = ', palavra
                    return True

    except IOError:
        pass
    return False


def verificaDominio(host):
    '''Verifica se host tem permissão'''
    host = host.upper()
    try:
        with open(DOMINIOS_BLOQUEADOS) as arq:
            for dominio in arq:
                dominio = dominio.strip().upper()
                if dominio and dominio == host:
                    return True

    except IOError:
        pass
    return False
