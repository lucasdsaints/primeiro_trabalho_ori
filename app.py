import sys
import nltk

# http://www.facom.ufu.br/~wendelmelo/ori201902/trab1_ori_2019-02.pdf
# chave: 3,1 2,4

def main ():
	#arquivos de entrada
	c_bases = sys.argv[1]
	c_consulta = sys.argv[2]

	#---------------------rotina para a geração de um índice invertido-----------------------------------
	arq_bases = open(c_bases, "r")
	txt_arq_bases = arq_bases.read()
	lista_bases = txt_arq_bases.split("\n")


	#preparando a base

	i = 0
	indice_invertido = {}
	for base in lista_bases:
		i = i + 1
		# print(base)
		texto = open(base, "r").read()

		vetor_palavras = limparTexto(texto)

		vetor_radicais = extrairRadicais(vetor_palavras)

		geraIndiceInvertido(indice_invertido, vetor_radicais, i)

	arq_indice = open("indice.txt", "a")

	# print(indice_invertido)
	for radical in indice_invertido:
		string = '' + radical + ': '
		for base in indice_invertido[radical]:
			string += '{base},{qtd} '.format(base=base, qtd=indice_invertido[radical][base])
		string += '\n'
		arq_indice.write(string)

	arq_indice.close()

	#---------------------------------Implementação do modelo booleano de RI-----------------------------------
	gabarito = {}
	arq_consulta = open(c_consulta, "r")
	txt_arq_consulta = arq_consulta.read()
	# print(txt_arq_consulta)
	preparaConsulta(txt_arq_consulta )


def preparaConsulta (str):
	str = str.lower()
	str = str.replace('!', 'not ')
	str = str.replace('&', 'and')
	vetor_condicoes = str.split('|')

	# limpa espacos desnecessários das strings
	# for i in range(0, len(vetor_condicoes)):
	# 	vetor_condicoes[i] = vetor_condicoes[i].strip()


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

	print(vetor_peso_consulta) # imprima isso pra ver o que aconteceu
	#	 condição 1         condição 2
	# [{casa:1, amor:1}, {casa:1, mora:0}]
	# agora com o a consulta preparada, a gnt tem que verificar para cada
	# documento da base (variavel: lista_bases), se ele atende uma das condições
	# olhando pro indice invertido (variavel: indice_invertido);
	# Se atender, já escreve no arquivo de saida e acabamos o trabalho (resposta.txt)
	# o arquivo de saida é o ultimo topico do pdf:
	# http://www.facom.ufu.br/~wendelmelo/ori201902/trab1_ori_2019-02.pdf



def geraIndiceInvertido (indice_invertido, radicais, n_base):
	for radical in radicais:
		if radical not in indice_invertido:
			indice_invertido[radical] = {n_base:1}
		else:
			if n_base in indice_invertido[radical]:
				indice_invertido[radical][n_base] = indice_invertido[radical][n_base] + 1
			else:
				indice_invertido[radical][n_base] = 1


	# print(indice_invertido)
	# print('\n')

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