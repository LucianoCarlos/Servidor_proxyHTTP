# coding: utf-8

import socket
from settings import *
from filtro_conteudo import *
from controle_cache import *
from thread import start_new_thread, exit
import argparse

_TIMEOUT = 2
__DESCRICAO__ = ''' Simples servidor proxy para conexões http'''


def help():
    ''' Trata argumentos inseridos pelo usuário, exibe texto de ajuda '''
    # Descrição do programa.
    parser = argparse.ArgumentParser(description=__DESCRICAO__)

    # Adicinando argumento.
    parser.add_argument('--port', '-p', action='store', dest='port', default=PORTA,
                        required=False, help='Porta de escuta do servidor proxy.')

    return parser.parse_args()


class ClienteHTTP:
    ''' Esta classe define uma conexão http com um host. '''

    def __init__(self, host='', port=80):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.sock.connect((host, port))

    def defineTimeout(self, segundos):
        self.sock.settimeout(segundos)

    def is_html(self):
        return True if 'text/html' in self.dado else False

    def recebe_dados(self, buffer_size):
        self.dado = ''
        try:
            self.dado = self.sock.recv(buffer_size)
        except socket.timeout:
            return ''
        except socket.error:
            return ''
        return self.dado

    def enviaDados(self, dados):
        self.sock.send(dados)

    def terminaConexao(self):
        self.sock.close()


def iniciaServidor(arguments):
    ''' Inicia soquete TCP para conexões com cliente.'''
    try:
        # Extraindo porta dos argumentos.
        port = int(arguments.port)

        # Iniciando servidor proxy.
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, port))
        servidor.listen(100)
    except ValueError:
        print 'Porta invalida...'
    except socket.error as e:
        print 'Porta com privilegios insuficiente de acesso'
    else:
        print '\nserver up {0} port {1}'.format(HOST, port), '....\n'
        escutaConexao(servidor)
        servidor.close()


def escutaConexao(servidor):
    ''' Escuta porta e responde requisições dos clientes.
    '''
    global is_bloqueado
    is_bloqueado = False

    while True:
        con, infoCliente = servidor.accept()
        header = con.recv(BUFFER_SIZE)
        # Verifica conexão https. Caso seja, rejeita.
        if verificaHttps(header) or not header:
            continue
        print[infoCliente[0]], '--', header.split('\r\n')[0], '\n'
        if is_bloqueado == False:
            start_new_thread(respondeCliente, tuple([header,  con]))


def cria_new_header(req, headers, submit, cache):
    ''' Cria novo cabeçalho, adicionando campos Get condicional '''

    # Remove pedido de compactaçao
    try:
        headers.pop('Accept-Encoding')
    except:
        pass

    # Acrescenta campo get condicional.
    if cache:
        headers['If-Modified-Since'] = obterData(cache[:2048])

    # Novo cabeçalho.
    new_header = ' '.join(req)

    for x in headers:
        new_header = new_header + '\r\n' + x + ': ' + headers[x]

    # Adicionando dados POST
    return new_header + submit


def respondeCliente(header, con):
    # Extraindo requisição do cabeçalho.
    req, headers, submit = extraiCabecalho(header)

    # Verifica permissao do dominio.
    if verificaDominio(headers['Host']):
        print 'Host bloqueado', headers['Host']
        con.send(abre_arquivo(PAGINA_BLOQUEIO))
        con.close()
        exit()

    # Ler arquivo presente em cache.
    cache = ler_cache(req[1])

    try:
        cliente = ClienteHTTP(headers['Host'], 80)
    except socket.gaierror:
        exit()
    except socket.error:
        exit()

    # Define timeout e envia cabeçalho para servidor web.
    cliente.defineTimeout(_TIMEOUT)

    # Envia dados para o servidor web.
    cliente.enviaDados(cria_new_header(req, headers, submit, cache))

    # Recebe dados
    dado, dados = cliente.recebe_dados(BUFFER_SIZE), ''

    if statusResposta(dado) == 304 and cache:
        # print '**********arquivo em cache************'
        con.send(cache)
    else:

        if cliente.is_html():
            while True:
                if not dado:
                    break
                dados = dados + dado
                dado = cliente.recebe_dados(BUFFER_SIZE)

            if pesquisaPalavra(dados):
                is_bloqueado = True
                dados = abre_arquivo(PAGINA_BLOQUEIO)
            con.send(dados)
            con.close()

        else:
            while True:
                if not dado:
                    break
                try:
                    con.send(dado)
                except socket.error:
                    con.close()
                    exit()
                dados = dados + dado
                dado = cliente.recebe_dados(BUFFER_SIZE)

        # Gravando cache.
        tam_arq = len(dados)
        if tam_arq <= TAMANHO_MAX_CACHE and tam_arq > TAMANHO_MIN_CACHE:
            grava_arquivo_cache(req[1], dados)
    con.close()
    cliente.terminaConexao()
    exit()


def abre_arquivo(nome_arq):
    ''' abre arquivo e le seu conteúdo. '''
    dados = ''
    try:
        dados = open(nome_arq).read()
    except IOError:
        pass
    return dados


def statusResposta(dados):
    ''' Retonar o status da resposta '''
    return 1 if not dados else int(dados.split()[1])


def verificaHttps(request):
    ''' Verifica se é uma requisição https(port 443) '''
    return True if ':443' in request else False


def extraiCabecalho(header):
    ''' Extrai dados do cabeçalho. Retorna uma tuple os dados extraidos.
        Uma tuple contendo dados de requisição, dicionario contendo campos,
        e os dados caso seja uma requisição POST. 
    '''
    header_dict = {}
    header = header.split('\r\n')

    # Remove campo GET ou POST.
    request = header.pop(0).split()

    submit = '\r\n\r\n'
    if not header[-2]:
        header.pop(-2)
        submit = submit + header.pop(-1)

    # Armazena os itens do cabeçalho em um dicionario.
    for tag in header:
        tag = tag.split(': ')
        header_dict[tag[0]] = tag[1]

    return (request, header_dict, submit)


def obterData(dados):
    ''' Obtem a data de um cabeçalho.
        Retorna data caso exista e False caso contrário.
    '''
    try:
        return dados.split('Date: ')[1].split('\r\n')[0]
    except IndexError as e:
        return ''


if __name__ == '__main__':
    ''' Função principal '''
    arguments = help()
    try:
        # proxy.setup_http_proxy('10.0.0.254', 8080)
        iniciaServidor(arguments)
    except KeyboardInterrupt:
        print '\n\nEncerrando servidor...\n\n'
