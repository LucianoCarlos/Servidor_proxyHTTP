# coding: utf-8

import socket

from setting import *

import thread

_TIMEOUT = 2

''' Referência
 http://www.caucho.com/resin-4.0/admin/http-proxy-cache.xtp
'''


class ClienteHTTP:
    def __init__(self, host='', port=80):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.connect((self.host, self.port))

    def defineTimeout(self, segundos):
        self.sock.settimeout(segundos)

    def enviaDados(self, dados):
        self.sock.send(dados)

    def recebeDados(self, buffer):
        dados = ''
        while True:
            # Captura exceção do timeout.
            try:
                dado = self.sock.recv(buffer)
                if not dado:
                    break
                dados = dados + dado
            except socket.timeout:
                break
        return dados

    def terminaConexao(self):
        self.sock.close()


def iniciaServidor():
    ''' Inicia soquete TCP para conexões com cliente.'''
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORTA))
    servidor.listen(1)
    print '\nserver up port ', PORTA, '....'
    escutaConexao(servidor)


# usar depois
def terminaServidor(servidor):
    ''' Termina soquete TCP. '''
    servidor.close()


def escutaConexao(servidor):
    ''' Escuta porta e responde requisições dos clientes.
    '''
    while True:
        con, infoCliente = servidor.accept()
        header = con.recv(BUFFER_SIZE)
        # Verifica conexão https. Caso seja, rejeita.
        if verificaHttps(header) != -1 or not header:
            continue
        print [infoCliente[0]], header.split('\n')[0], '\n'
        thread.start_new_thread(respondeCliente, tuple([header,  con]))


def respondeCliente(header, con):
    host = header.split('\r\n')[1].split()[1]
    cliente = ClienteHTTP(host, 80)
    cliente.defineTimeout(_TIMEOUT)
    cliente.enviaDados(header)
    dado = ''
    while True:
        dado = cliente.recebeDados(1024)
        if not dado:
            break
        con.send(dado)


def statusResposta(dados):
    if not dados:
        return 1
    return int(dados.split()[1])


def extraiCabecalho(cabecalho):
    ''' Extrai e armazena todo o cabeçalho em um dicionário para
        facilitar a manipulação. Retorna o cabeçalho criado.
    '''
    cabecalhoDicionario = {}
    # Elimina '\r' da string.
    cabecalho = cabecalho.replace('\r', '')
    # Elimina campo da requisição.
    cabecalho = cabecalho.split('\n')[1:]
    # Armazena os itens do cabeçalho em um dicionario.
    for tag in cabecalho:
        # Verifica fim do cabeçalho.
        if not tag:
            break
        tag = tag.split(': ')
        cabecalhoDicionario[tag[0]] = tag[1]
    return cabecalhoDicionario


def obterData(dados):
    ''' Obtem a data de um cabeçalho.
        Retorna data caso exista e False caso contrário.
    '''
    header = extraiCabecalho(dados)
    try:
        return header['Date']
    except KeyError:
        return '\n'


def extraiNomeArquivo(request_browser):
    ''' Extrai nome do arquivo em uma requisicao. '''
    request_browser = request_browser.replace('HTTP/1.1', '')
    request_browser = request_browser.split('?')[0]
    return request_browser[request_browser.rfind('/') + 1:]


def verificaHttps(request):
    ''' Verifica se é uma requisição https(port 443) '''
    return request.split('\n')[0].find('443')


def extraiRequisicao(dados):
    ''' Extrai e retorna a requisição do cabeçalho.
        primeira linha do cabeçalho http.
    '''
    return dados.split('\r\n')[0] if dados else False


if __name__ == '__main__':
    ''' Função principal '''
    try:
        # proxy.setup_http_proxy('10.0.0.254', 8080)
        iniciaServidor()
    except KeyboardInterrupt:
        print '\n\nEncerrando servidor...\n\n'
