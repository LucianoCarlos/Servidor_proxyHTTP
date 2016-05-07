#Servidor proxy HTTP
Trabalho desenvolvido no Curso Tecnologias em Sistemas para Internet para disciplina de Redes de Computadores.

## Descrição
Aplicativo é um simples servidor proxy http. Ele age como intermediário nas requisições http, realizadas pelos clientes (navegadores web), solicitando recursos de outros servidores. 

## Características
- Intermedia as requisições HTTP realizadas pelos clientes (navegadores web);
- Realiza o cache dos arquivos requisitados aos servidores web;
- Utiliza o GET Condicional para verificar se as cópias em cache não expiraram;
- Arquivo de configuração definindo o tamanho mínimo e máximo dos arquivos que poderão ficar em cache;
- Atua como filtro de conteúdo, impedindo o acesso a sites (domínio e IP) que estejam definidos como impróprios (em um arquivo de configuração) e também a páginas que possuam palavras proibidas (também definidas em um arquivo de configuração).

## Como funciona?
Quando o cliente faz uma requisição, o servidor verifica se o acesso ao host(domínio ou ip) é permitido. Caso não seja bloqueado, faz uma verificação local na pasta definida para cache de arquivos. Se o arquivo estiver em cache, é adicionado no cabeçalho da requisição http o campo GET Condicional. Caso o arquivo não tenha sido modificado desde o último acesso, o cache é enviado para o cliente, caso contrário é enviado o conteúdo recebido do servidor requisitado e é salvo uma copia em cache. 

Em todo arquivo do tipo html e feito um parser em busca de palavras bloqueadas, definidas no arquivo de configuração. Caso o host (domínio ou ip) ou conteúdo html contenha conteúdo proibido, é enviado ao cliente uma página de informação de bloqueio e se esse conteúdo estiver em cache é excluído do disco a pasta referente a este host.

## Como usar?
 1. - Configure o arquivo settings.py com as informações corretas.
 2. - Execute o arquivo server_proxyHttp.py.

Estes arquivos estão localizados na pasta src.

## Desenvolvedores
+ [Luciano Carlos](https://github.com/LucianoCarlos)
+ [Gabriel Barros](https://github.com/GabrielBPereira)


  
