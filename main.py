import pandas as pd
from Transform.transform import add_missing_columns, revert_geometries

edital = 11
year = 2023

df_listings = pd.read_csv('Data/Processed/merged_listings_{}_{}'.format(edital, year))
df_all_listings = pd.read_csv('Data/Ready/all_listings_updated_{}_{}'.format(edital-1, year))
df_listings.drop(columns=['Valor de Face'], inplace=True)


#.drop(columns=['Unnamed: 0', 'edital_y', 'Unnamed: 0.3', 'Unnamed: 0.1', 'Unnamed: 0.2'], inplace=True)

df_all_listings = df_all_listings.rename(columns={'edital_x': 'Edital', 'valor_caucao_x': 'Valor Caução', 'cond_pgto': 'Condição de Pagamento',
                                                  })

df_listings.rename(columns={'edital': 'Edital', 'n_imovel_no_edital': 'Nº do Imóvel no Edital', 'destinacao': 'Destinação', 'end': 'Endereço',
                            'area': 'Área', 'area_const_basica': 'Área Construção Básica', 'area_const_max': 'Área Construção Máxima', 'url': 'url_details',
                            'valor_face': 'Valor de Face', 'cond_pgto': 'Condição de Pagamento', 'valor_caucao': 'Valor Caução', 'coords': 'geometry'}, inplace=True)

temp = revert_geometries(df=df_listings)
df_listings['geometry'] = pd.Series(temp)
df_listings = add_missing_columns(df_all_listings, df_listings)

df_all_listings = pd.concat([df_listings, df_all_listings])

df_all_listings.to_csv('Data/Ready/all_listings_updated_{}_{}'.format(edital, year), index=False)
df_all_listings.to_excel('Data/Ready/all_listings_updated_{}_{}.xlsx'.format(edital, year), index=False)

















df_listings_updated = df_all_listings
df_duplicated = df_listings_updated[df_listings_updated.duplicated(subset='id_terracap')]
df_new_unique = df_listings_updated.drop_duplicates(subset='id_terracap')
df_new_unique.reset_index(inplace=True)



for i in range(len(df_duplicated)):
    cod_terracap_temp = df_duplicated['id_terracap'].iloc[i]
    data_edital_temp = df_duplicated['Edital'].iloc[i]
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


















all_listings.rename(columns={'edital': 'edital_x',
                             'n_imovel_no_edital': 'Nº do Imóvel no Edital',
                             'destinacao': 'Destinação',
                             'area': 'Área',
                             'area_const_basica': 'Área Construção Básica',
                             'area_const_max': 'Área Construção Máxima',
                             'valor_face': 'Valor de Face',
                             'valor_caucao': 'valor_caucao_x',
                             'end': 'Endereço',
                             'url': 'url_details'}, inplace=True)

merged_df = pd.merge(all_listings, df_imoveis_edital, on='url_details')

for i in range(len(merged_df)):
    try:
        merged_df['Área Construção Básica'].iloc[i] = float(merged_df['Área Construção Básica'].iloc[i].split(" ")[0])
    except:
        pass
    try:
        merged_df['Área Construção Máxima'].iloc[i] = float(merged_df['Área Construção Máxima'].iloc[i].split(" ")[0])
    except:
        pass
    try:
        merged_df['Área'].iloc[i] = float(merged_df['Área'].iloc[i].split(" ")[0])
    except:
        pass

merged_df['R$ Valor / Pot. Max'] = merged_df['Valor de Face']/merged_df['Área Construção Máxima']
merged_df['geometry'] = merged_df['coords']
merged_df['Bairro'] = merged_df['bairro']



list1 = list(merged_df.columns)
list2 = list(df.columns)
excluded_list2 = [element for element in list2 if element not in list1]

all_listings = merged_df
for unique_element in excluded_list2:
    all_listings['{}'.format(unique_element)] = '-'

list1 = list(df.columns)
list2 = list(all_listings.columns)
excluded_list2 = [element for element in list2 if element not in list1]
all_listings = all_listings.drop(columns=excluded_list2)


temp = revert_geometries(df=all_listings)
all_listings['geometry'] = pd.Series(temp)
df_new = pd.concat([all_listings, df])














df_sold_listings = pd.read_csv('Data/Raw/sold_listings_terracap_{}_{}'.format(edital, year))
























































































