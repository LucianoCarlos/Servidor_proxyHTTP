# coding: utf-8
from settings import PALAVRAS_BLOQUEADAS, DOMINIOS_BLOQUEADOS

def pesquisaPalavra(html):
	''' Pesquisa palavras dentro de um conteúdo html'''
	
	try:
		arq = open(PALAVRAS_BLOQUEADAS)
		for palavra in arq:
			palavra = palavra.replace('\n', '')
			if palavra in html:
				print palavra
				return True
		return False
	except IOError:
		return False
	
	
def verificaDominio(host):
	'''Verifica se host tem permissão'''
	
	try:
		arq = open(DOMINIOS_BLOQUEADOS)
		for dominio in arq:
			dominio = dominio.replace('\n', '')
			print dominio
			if dominio == host:
				return True
		return False
	except IOError:
		return False
	
