
# Primeiro trabalho de Organização e Recuperação da Informação 2019-02
# Alunos: Caliton Junior e Lucas Santos
# Professor: Wendel Melo

import sys
import nltk

def main ():
	#arquivos de entrada
	c_bases = sys.argv[1]
	c_consulta = sys.argv[2]

	#---------------------rotina para a geração de um índice invertido-----------------------------------
	arq_bases = open(c_bases, "r")
	txt_arq_bases = arq_bases.read()
	lista_bases = txt_arq_bases.split("\n")


	# montando o indice invertido
	i = 0
	indice_invertido = {}
	for base in lista_bases:
		i = i + 1
		texto = open(base, "r").read()
		vetor_palavras = limparTexto(texto)
		vetor_radicais = extrairRadicais(vetor_palavras)
		geraIndiceInvertido(indice_invertido, vetor_radicais, i)

	arq_indice = open("indice.txt", "a")

	for radical in indice_invertido:
		string = '' + radical + ': '
		for base in indice_invertido[radical]:
			string += '{base},{qtd} '.format(base=base, qtd=indice_invertido[radical][base])
		string += '\n'
		arq_indice.write(string)

	arq_indice.close()

	#---------------------------------Implementação do modelo booleano de RI-----------------------------------
	arq_consulta = open(c_consulta, "r")
	txt_arq_consulta = arq_consulta.read()
	vet_consultas_and_not = getVetorConsultasAndNot(txt_arq_consulta )
	docs_resultado = set()
	for consulta in vet_consultas_and_not:
		docs_resultado.update(getDocsConsultaAndNot(consulta, indice_invertido, len(lista_bases)))

	# escreve o arquivo de saída
	arq_saida = open("resposta.txt", "a")
	arq_saida.write("{num}\n".format(num=len(docs_resultado)))
	for index in docs_resultado:
		# print(type(lista_bases))
		arq_saida.write("{arq}\n".format(arq=lista_bases[index-1]))
	arq_saida.close()

def getDocsConsultaAndNot(consulta, indice, num_docs):
	ids_docs = []
	for i in range (0,num_docs):
		ids_docs.append(i + 1)
	for radical in consulta:
		docs_indice = indice[radical].keys()
		if consulta[radical] == 1:
			ids_docs = [id for id in ids_docs if id in docs_indice]
		else:
			ids_docs = [id for id in ids_docs if id not in docs_indice]

	return ids_docs

def getVetorConsultasAndNot (str):
	str = str.lower()
	str = str.replace('!', 'not ')
	str = str.replace('&', 'and')
	vetor_condicoes = str.split('|')

	vetor_peso_consulta = []
	n_dic = 0
	for sub_str in vetor_condicoes:
		vetor_peso_consulta.append({}) # cria um novo dicionario para para cada substring/condição

		vet_sub_str = sub_str.split("and")
		for i in range(0, len(vet_sub_str)):
			if ( 'not'in vet_sub_str[i]):
				vetor_peso_consulta[n_dic][extrairRadicais(vet_sub_str[i].replace('not', '').strip())] = 0
			else:
				vetor_peso_consulta[n_dic][extrairRadicais(vet_sub_str[i].strip())] = 1
		n_dic += 1

	return vetor_peso_consulta

def geraIndiceInvertido (indice_invertido, radicais, n_base):
	for radical in radicais:
		if radical not in indice_invertido:
			indice_invertido[radical] = {n_base:1}
		else:
			if n_base in indice_invertido[radical]:
				indice_invertido[radical][n_base] = indice_invertido[radical][n_base] + 1
			else:
				indice_invertido[radical][n_base] = 1

def limparTexto (str):
	str = str.lower()
	str =  str.replace("\n", " ")
	str = str.replace(',', " ")
	str = str.replace('...', " ")
	str = str.replace('.', " ")
	str = str.replace('!', " ")
	str = str.replace('?', " ")
	vetor_palavras = ' '.join(str.split()).split(' ')
	stopwords = nltk.corpus.stopwords.words('portuguese')
	vetor_palavras_limpo = []
	for palavra in vetor_palavras:
		if palavra not in stopwords:
			vetor_palavras_limpo.append(palavra)

	return vetor_palavras_limpo

def extrairRadicais (objeto):
	stemmer = nltk.stem.RSLPStemmer()

	# se o objeto for só uma palavra
	if (type(objeto) == type('string')):
		return stemmer.stem(objeto)
	# se o objeto for um conjunto de palavras
	else:
		vetor_radicais = []
		for palavra in objeto:
			vetor_radicais.append(stemmer.stem(palavra))

	return vetor_radicais

main()