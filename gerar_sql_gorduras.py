import pandas as pd
from decimal import Decimal
import math

"""
	update ingrediente_composicaoquimicacentesimal set gordura_saturada = x, gordura_trans = y 
	where id = (
		select composicao_quimica_centesimal_id from ingrediente_ingredientelivre where nome = 'dadas'
	)
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
xls = pd.ExcelFile('Taco_4a_edicao_2011.xls')
df = pd.read_excel(xls, 'AGtaco3')
posicaoTabelas = [[5,35], [39,64], [66,70], [74,105], [109,112], [115,139], [145,157], [160,175], [179,210], [214,215], [218,245], 
	[249,280], [284,315], [319,347], [353,373], [376,381], [387,396], [399,401], [404,408], [411,417], [421,445], [448,452], 
	[456,479], [482,487], [491,494]]
sql = ""

for table in posicaoTabelas:
	for row in range(table[0]-2, table[1]-1):
		nome = df.iloc[row,1]
		gorduraSaturada = gerarCampo(df.iloc[row,2], True, False)
		gorduraTrans = gerarCampo(df.iloc[row,23], True, False) + gerarCampo(df.iloc[row,24], True, False)
		
		sql += (
			"UPDATE ingrediente_composicaoquimicacentesimal SET gordura_saturada = {}, gordura_trans = {} " + 
			"WHERE id = ( " +
			"	select composicao_quimica_centesimal_id from ingrediente_ingredientelivre where nome = '{}' " +
			");\n"
		).format(gorduraSaturada, gorduraTrans, nome)

	sql += "\n\n"


text_file = open("atualizarGorduras.sql", "w")
text_file.write(sql)
text_file.close()


