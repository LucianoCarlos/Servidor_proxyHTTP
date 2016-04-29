# coding: utf-8

# Endereço do servidor.
HOST = '127.0.0.1'

# Porta usada para conexão com cliente.
PORTA = 8088

# Buffer de envio e recebimento de dados.
BUFFER_SIZE = 4096

# Pasta usada para armazenar cache.
DIR_CACHE = '../cache/'

# Página html de informação de bloqueio
PAGINA_BLOQUEIO = '../html/bloqueio.html'

# Tamanho mínimo em bytes de arquivos que podem ser armazenado em cache.
TAMANHO_MIN_CACHE = 100

# Tamanho máximos em bytes do arquivos que podem ser armazenado em cache.
TAMANHO_MAX_CACHE = 1000

# Arquivo de palavras bloqueadas.
PALAVRAS_BLOQUEADAS = '../config/palavras.conf'

# Arquivo de dominios bloqueados.
DOMINIOS_BLOQUEADOS = '../config/dominios.conf'
