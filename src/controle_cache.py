# coding: utf-8

from os import path, makedirs
from urlparse import urlparse, urljoin
from settings import DIR_CACHE
from shutil import rmtree
from server_proxyHTTP import verifica_html


def separa_url(url):
    ''' Pesquisa dentro da url a requisição. Separa da requisição
        a árvore de diretórios e o nome do arquivo.
    '''
    url = ''.join(urlparse(url)[1:3])
    return path.split(url)


def ler_cache(requisicao):
    ''' Pesquisa um arquivo em disco. Se existir retorna seu conteúdo.
        Caso contrario retorna False.
    '''
    nome_dir, nome_arq = separa_url(requisicao)

    if not nome_arq:
        nome_arq = 'index.html'

    nome_dir = DIR_CACHE + nome_dir

    try:
        return open(nome_dir + '/' + nome_arq).read()
    except IOError:
        return ''


def grava_arquivo_cache(url, dados):
    ''' Grava um arquivo em disco. Cria uma pasta, caso não exista,
        com nome do host.
    '''
    nome_dir, nome_arq = separa_url(url)

    if not nome_arq:
        nome_arq = 'index.html'

    nome_dir = DIR_CACHE + nome_dir

    # Criando arvores de diretório.
    try:
        makedirs(nome_dir)
    except OSError:
        pass
    else:
        try:
            open(nome_dir + '/' + nome_arq, 'w').write(dados)
        except IOError:
            pass


def apaga_conteudo_cache(nome_pasta):
    try:
        rmtree(DIR_CACHE + nome_pasta)
    except OSError:
        pass
