import pandas as pd

terrenos_edital = pd.read_csv('df_terracap_df_1.csv')
#terrenos_edital = pd.read_csv('datasets/terracap_vendidos_entre_2019_2021_abr.csv')
terrenos_vendidos = pd.read_csv('datasets/terrenos_vendidos_terracap.csv')

terrenos_edital['end_comp'] = terrenos_edital['end'].str.replace(" ", "")
terrenos_vendidos['endereco_comp'] = terrenos_vendidos['endereco'].str.replace(" ", "")


lista_def = terrenos_edital.drop_duplicates(subset=['id_terracap'])


lista_def = lista_def.rename(columns={'id_terracap': 'ID TERRACAP', 'classficacao': 'Classificação', 'relevo': 'Relevo',
                                      'situacao': 'Situação', 'tipo_de_solo': 'Tipo de Solo', 'forma': 'Forma',
                                      'posicao': 'Posição', 'frente': 'Frente', 'fundo': 'Fundo',
                                      'lado_esquerdo': 'Lado Esquerdo', 'bairro': 'Bairro', 'lado_direito': 'Lado Direito',
                                      'edital_x': 'Edital da Venda', 'valor_caucao_x': 'Valor Caução',
                                      'url_details': 'Link Terracap', 'n_imoveis': 'N. de Imóveis', 'area_y': 'Área',
                                      'coord_name': 'ID das Coordenadas', 'coords': 'Coordenadas'
                                      })

lista_def.to_csv('def_terracap_ongoing.csv')

lista_def['Área de Construção Básica'] = None
lista_def['Área de Construção Máxima'] = None
lista_def['Área do Terreno'] = None
lista_def['Participação em Outros Editais'] = None

for i in range(len(lista_def)):
    try:
        lista_def['Área de Construção Básica'].iloc[i] = int(lista_def['area_const_basica'].iloc[i].replace(" m²", ""))
    except:
        pass
    try:
        lista_def['Área de Construção Máxima'].iloc[i] = int(lista_def['area_const_max'].iloc[i].replace(" m²", ""))
    except:
        pass
    try:
        lista_def['Área do Terreno'].iloc[i] = int(lista_def['area_x'].iloc[i].replace(" m²", ""))
    except:
        pass
    part_outros_editais_string = str(lista_def['outros_editais_1'].iloc[i]) + ' ' + str(lista_def['outros_editais_2'].iloc[i]) + \
                                 ' ' + str(lista_def['outros_editais_3'].iloc[i]) + ' ' + str(lista_def['outros_editais_4'].iloc[i]) + \
                                 ' ' + str(lista_def['outros_editais_5'].iloc[i]) + ' ' + str(lista_def['outros_editais_6'].iloc[i]) + \
                                 ' ' + str(lista_def['outros_editais_7'].iloc[i]) + ' ' + str(lista_def['outros_editais_8'].iloc[i]) + \
                                 ' ' + str(lista_def['outros_editais_9'].iloc[i])
    lista_def['Participação em Outros Editais'].iloc[i] = part_outros_editais_string.replace('nan', '')

lista_def.to_csv('def_terracap_ongoing_2.csv')


lista_def = lista_def.rename(columns={'valor_face': 'Valor de Face', 'edital': 'Edital',
                                      'n_imovel_no_edital': 'Nº do Imóvel no Edital',
                                      'area_const_max': 'Area Construção Máxima',
                                      'valor_caucao': 'Valor Caução', 'end': 'Endereço'
                                      }, inplace=False)

lista_def = lista_def.drop(columns=['edital_y', 'endereco', 'index', 'valor_caucao_y', 'area_const_basica',  'Area Construção Máxima'])


lista_def['Número Lances'] = None
lista_def['Valor Lance Vencedor'] = None
lista_def['Valor Lance Segundo Colocado'] = None
lista_def['Valor Lance Terceiro Colocado'] = None
lista_def['R$ Valor / Pot. Max'] = None
lista_def['Entrada'] = None
lista_def['Número Meses'] = None

lista_def = lista_def[lista_def['Área de Construção Máxima'] >= 10]
lista_def['R$ Valor / Pot. Max'] = None
lista_def = lista_def.reset_index()
temp = []

lista_def.to_csv('def_terracap_ongoing_3.csv')


for i in lista_def['end_comp']:
    for j in terrenos_vendidos['endereco_comp']:
        if i == j:
            temp.append(j)
        else:
            pass


for i in range(len(lista_def)):
    end = lista_def['end_comp'][i]
    terrenos_selecionados = terrenos_vendidos[terrenos_vendidos['endereco_comp'].str.contains(end)]
    try:
        lista_def['Número Lances'][i] = len(terrenos_selecionados)
    except:
        lista_def['Número Lances'][i] = 0

    terrenos_selecionados = terrenos_selecionados.reset_index()
    if len(terrenos_selecionados) >= 1:
        if terrenos_selecionados['colocacao'][0] == 'Desclassificado':
            lista_def['Valor Lance Vencedor'][i] = '-'
        else:
            lista_def['Valor Lance Vencedor'][i] = terrenos_selecionados['valor'][0]
    else:
        lista_def['Valor Lance Vencedor'][i] = '-'

    if len(terrenos_selecionados) >= 2:
        if terrenos_selecionados['colocacao'][1] == 'Desclassificado':
            lista_def['Valor Lance Segundo Colocado'][i] = '-'
        else:
            lista_def['Valor Lance Segundo Colocado'][i] = terrenos_selecionados['valor'][1]
    else:
        lista_def['Valor Lance Segundo Colocado'][i] = '-'

    if len(terrenos_selecionados) >= 3:
        if terrenos_selecionados['colocacao'][2] == 'Desclassificado':
            lista_def['Valor Lance Terceiro Colocado'][i] = '-'
        else:
            lista_def['Valor Lance Terceiro Colocado'][i] = terrenos_selecionados['valor'][2]
    else:
        lista_def['Valor Lance Terceiro Colocado'][i] = '-'

    try:
        lista_def['R$ Valor / Pot. Max'][i] = float(lista_def['Valor Lance Vencedor'][i])/float(lista_def['Área de Construção Máxima'][i])
    except:
        lista_def['R$ Valor / Pot. Max'][i] = float(lista_def['Valor de Face'][i]) / float(lista_def['Área de Construção Máxima'][i])
    try:
        lista_def['Número Meses'][i] = int(terrenos_selecionados['meses'][0])
    except:
        lista_def['Número Meses'][i] = '-'
    try:
        lista_def['Entrada'][i] = '{}%'.format(int(terrenos_selecionados['entrada'][0] * 100))
    except:
        lista_def['Entrada'][i] = '-'



lista_def.to_csv('imoveis_cleaned_new.csv')

lista_def.to_excel('imoveis_cleaned.xlsx')

imoveis = pd.read_csv('df_terracap_df_1.csv')
lista_def = imoveis.drop_duplicates(subset=['endereco'])


import pandas as pd
pd.read_csv("pd.read_csv('terracap_estoque_brasilia.csv')")



