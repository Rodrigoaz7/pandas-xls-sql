import pandas as pd
from decimal import Decimal
import math

"""
	INSERT INTO public.ingrediente_ingredientelivre
	(nome, composicao_quimica_centesimal_id)
	VALUES('', 0);
	INSERT INTO public.ingrediente_composicaoquimicacentesimal
	(carboidrato, proteina, gordura_total, gordura_saturada, gordura_trans, fibra, sodio, calcio, cinzas, cobre, 
	colesterol, ferro, fosforo, magnesio, manganes, niacina, piridoxina, potassio, riboflavina, tiamina, umidade, vitamina_c, zinco)
	VALUES(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);
"""

def is_number(s):
	if isinstance(s, float) or isinstance(s, int):
		return not math.isnan(float(s))
	return False

def gerarCampo(s, obrigatorio, converterMgParaG):
	if is_number(s):
		return s if not converterMgParaG else s/1000.0
	else:
		return 0 if obrigatorio else "null"

# linha 3 no código é a linha 5 no xls.
df = pd.read_excel('Taco_4a_edicao_2011.xls')
posicaoTabelas = [[5,35], [39,70], [76,105], [109,140], [144,175], [179,183], [186,210], [214,245], [249,280], [284,290], [293,306], 
	[310,315], [319,350], [354,365], [368,385], [389,420], [424,455], [459,490], [494,502], [505,524], [528, 531], [534,547], 
	[550,556], [558,559], [563,580], [583,591], [594,594], [598,601], [605,629], [633,639], [642, 662], [666, 674], [677,687]]
sql = ""

for table in posicaoTabelas:
	for row in range(table[0]-2, table[1]-1):
		# dados obrigatórios para cada ingrediente
		nome = df.iloc[row,1]
		energia = gerarCampo(df.iloc[row,3], True, False)
		proteina = gerarCampo(df.iloc[row,5], True, False)
		gordura_total = gerarCampo(df.iloc[row,6], True, False)
		carboidrato = gerarCampo(df.iloc[row,8], True, False)
		fibra = gerarCampo(df.iloc[row,9], True, False)
		sodio = gerarCampo(df.iloc[row,17], True, True)

		#dados optativos
		umidade = gerarCampo(df.iloc[row,2], False, False)
		colesterol = gerarCampo(df.iloc[row,7], False, True)
		cinzas = gerarCampo(df.iloc[row,10], False, False)
		calcio = gerarCampo(df.iloc[row,11], False, True)
		magnesio = gerarCampo(df.iloc[row,12], False, True)
		manganes = gerarCampo(df.iloc[row,14], False, True)
		fosforo = gerarCampo(df.iloc[row,15], False, True)
		ferro = gerarCampo(df.iloc[row,16], False, True)
		potassio = gerarCampo(df.iloc[row,18], False, True)
		cobre = gerarCampo(df.iloc[row,19], False, True)
		zinco = gerarCampo(df.iloc[row,20], False, True)
		tiamina = gerarCampo(df.iloc[row,24], False, True)
		riboflavina = gerarCampo(df.iloc[row,25], False, True)
		piridoxina = gerarCampo(df.iloc[row,26], False, True)
		niacina = gerarCampo(df.iloc[row,27], False, True)
		vitaminaC = gerarCampo(df.iloc[row,28], False, True)

		sql += (
				"INSERT INTO public.ingrediente_composicaoquimicacentesimal " +
				"(carboidrato, proteina, gordura_total, gordura_saturada, gordura_trans, fibra, sodio, calcio, cinzas, cobre,  " +
				"colesterol, ferro, fosforo, magnesio, manganes, niacina, piridoxina, potassio, riboflavina, tiamina, umidade,  " +
				"vitamina_c, zinco)  " +
				"VALUES({}, {}, {}, 0, 0, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});\n "
		).format(carboidrato, proteina, gordura_total, fibra, sodio, calcio, cinzas, 
			cobre, colesterol, ferro, fosforo, magnesio, manganes, niacina, piridoxina, potassio, riboflavina, tiamina, 
			umidade, vitaminaC, zinco)

		selectComposicaoQuimicaCentesimal = "(SELECT currval('ingrediente_composicaoquimicacentesimal_id_seq'))";

		sql += (
			"INSERT INTO public.ingrediente_ingredientelivre(nome, composicao_quimica_centesimal_id) " +
			"VALUES({}, {});\n "
		).format("'"+nome+"'", selectComposicaoQuimicaCentesimal)

	sql += "\n\n"

#	print(str(nome) + " " + str(energia) +  " " + str(proteina) + " " + str(gordura_total) + " " + str(carboidrato) + " " + str(fibra))

text_file = open("ingredientes.sql", "w")
text_file.write(sql)
text_file.close()


