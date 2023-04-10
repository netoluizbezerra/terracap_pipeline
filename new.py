import pandas as pd
import ast

df_all = pd.read_csv('df_terracap_df_2023.csv')
df_info_basica = pd.read_csv('info_basica_terracap_2023')
df_all_01 = pd.read_csv('listings_terracap_2023')
df_vendidos = pd.read_csv('terrenos_vendidos_terracap_2023_new.csv')

# KEpp goin with DF all e DF Vendidos
lista_def = df_all
df_vendidos['endereco_comp'] = df_vendidos['endereco'].str.replace(" ", "")
lista_def['end_comp'] = lista_def['endereco'].str.replace(" ", "")

lista_def['Número Lances'] = 0
lista_def['Valor Lance Vencedor'] = 0
lista_def['Valor Lance Segundo Colocado'] = 0
lista_def['Valor Lance Terceiro Colocado'] = 0
lista_def['R$ Valor / Pot. Max'] = 0
lista_def['Número Meses'] = 0
lista_def['Entrada'] = 0
lista_def['Valor de Face'] = 0
lista_def['Valor de Face'] = 0

# Ajustes na nomenclatura de lista DEF
lista_def.rename(columns={'area_const_max': 'Área Construção Máxima',
                          'area_const_basica': 'Área Construção Básica',
                          'area_x': 'Área'}, inplace=True)

for i in range(len(lista_def)):
    try:
        lista_def['Área Construção Básica'].iloc[i] = float(lista_def['Área Construção Básica'].iloc[i].split(" ")[0])
    except:
        pass
    try:
        lista_def['Area Construção Máxima'].iloc[i] = float(lista_def['Area Construção Máxima'].iloc[i].split(" ")[0])
    except:
        pass
    try:
        lista_def['Área'].iloc[i] = float(lista_def['Área'].iloc[i].split(" ")[0])
    except:
        pass



for i in range(len(lista_def)):
    end = lista_def['end_comp'][i]
    terrenos_selecionados = df_vendidos[df_vendidos['endereco_comp'].str.contains(end)]
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
        lista_def['R$ Valor / Pot. Max'][i] = float(lista_def['Valor Lance Vencedor'][i])/float(lista_def['Area Construção Máxima'][i])
    except:
        lista_def['R$ Valor / Pot. Max'][i] = float(lista_def['Valor de Face'][i]) / float(lista_def['Area Construção Máxima'][i])
    try:
        lista_def['Número Meses'][i] = int(terrenos_selecionados['meses'][0])
    except:
        lista_def['Número Meses'][i] = '-'
    try:
        lista_def['Entrada'][i] = '{}%'.format(int(terrenos_selecionados['entrada'][0] * 100))

    except:
        lista_def['Entrada'][i] = '-'


listings = pd.read_csv('imoveis_cleaned_def_2')
listings.columns
lista_def.columns

listings.drop(columns=['Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0', 'level_0', 'index'],
              inplace=True)


lista_def.drop(columns=['titulo'], inplace=True)

listings.rename(columns={'Area do Terreno': 'Área',
                          'dest_new': 'Destinação Resumida'}, inplace=True)

lista_def.rename(columns={'coords': 'geometry',
                          'valor_face': 'Valor de Face'}, inplace=True)


list1 = list(listings.columns)
list2 = list(lista_def.columns)

unique_list1 = []
unique_list2 = []

for element in list1:
    if element not in list2:
        unique_list1.append(element)

for element in list2:
    if element not in list1:
        unique_list2.append(element)

print("Unique elements in list 1:", unique_list1)
print("Unique elements in list 2:", unique_list2)


lista_def = lista_def.reset_index(drop=True)
listings = listings.reset_index(drop=True)

df_listings_updated = pd.concat([a, listings])
df_listings_updated.to_csv('terracap_atualizado.csv', index=False)

df_duplicated = df_listings_updated[df_listings_updated.duplicated(subset='id_terracap')]
df_new_unique = df_listings_updated.drop_duplicates(subset='id_terracap')
df_new_unique.reset_index(inplace=True)



for i in range(len(df_duplicated)):
    cod_terracap_temp = df_duplicated['id_terracap'].iloc[i]
    data_edital_temp = df_duplicated['edital_x'].iloc[i]
    index_temp = df_new_unique[df_new_unique['id_terracap'] == cod_terracap_temp].index
    if df_new_unique['outros_editais_1'].iloc[index_temp[0]] == None:
        df_new_unique['outros_editais_1'].iloc[index_temp[0]] = data_edital_temp
    elif df_new_unique['outros_editais_2'].iloc[index_temp[0]] == None:
        df_new_unique['outros_editais_2'].iloc[index_temp[0]] = data_edital_temp
    elif df_new_unique['outros_editais_3'].iloc[index_temp[0]] == None:
        df_new_unique['outros_editais_3'].iloc[index_temp[0]] = data_edital_temp
    elif df_new_unique['outros_editais_4'].iloc[index_temp[0]] == None:
        df_new_unique['outros_editais_4'].iloc[index_temp[0]] = data_edital_temp
    elif df_new_unique['outros_editais_5'].iloc[index_temp[0]] == None:
        df_new_unique['outros_editais_5'].iloc[index_temp[0]] = data_edital_temp
    elif df_new_unique['outros_editais_6'].iloc[index_temp[0]] == None:
        df_new_unique['outros_editais_6'].iloc[index_temp[0]] = data_edital_temp
    elif df_new_unique['outros_editais_7'].iloc[index_temp[0]] == None:
        df_new_unique['outros_editais_7'].iloc[index_temp[0]] = data_edital_temp
    elif df_new_unique['outros_editais_8'].iloc[index_temp[0]] == None:
        df_new_unique['outros_editais_8'].iloc[index_temp[0]] = data_edital_temp
    elif df_new_unique['outros_editais_9'].iloc[index_temp[0]] == None:
        df_new_unique['outros_editais_9'].iloc[index_temp[0]] = data_edital_temp
    else:
        print('abrir novo campo para {}'.format(cod_terracap_temp))



df_new['id_terracap'].value_counts()[0:20]

df = pd.read_csv('terracap_atualizado.csv')
temp =[]

new_df = df.iloc[0:290]
old_df = df.iloc[290:]


for i in range(len(new_df)):
    coord = ast.literal_eval(new_df['geometry'].iloc[i])
    new_temp = []
    for item in coord:
        item.reverse()
        new_temp.append(item)
    temp.append(new_temp)


new_df['geometry'] = pd.Series(temp)

df_final = pd.concat([new_df, old_df])
df_final.to_csv('terracap_atualizado_2.csv', index=False)



df.drop(columns=['titulo', 'Unnamed: 0.1', 'Unnamed: 0'], inplace=True)

