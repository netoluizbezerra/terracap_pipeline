from functions import get_edital, get_basic_info_monthly_edict_terracap, get_details_terracap, check_df_edital, \
    sold_properties
import pandas as pd

year = 2023
edital = get_edital()

if edital == None:
    edital = int(input('Edital não encontrado. Digite o edital: '))
else:
    edital = edital.split("/")[0]

imoveis_edital = get_basic_info_monthly_edict_terracap(edital=edital, year=2023)
df_imoveis_edital = pd.DataFrame(imoveis_edital)

list_urls = df_imoveis_edital['url_details'].tolist()
check_df_edital(edital, year)

all_listings = pd.read_csv('Data/Raw/listings_terracap_{}_{}'.format(edital, year))
all_listings = all_listings.drop_duplicates(subset='url')
mask = df_imoveis_edital[~df_imoveis_edital["url_details"].isin(all_listings["url"])]
list_urls = mask['url_details'].tolist()

while len(list_urls) > 0:
    for link in list_urls:
        imovel = get_details_terracap(url=link)
        imovel = pd.DataFrame(imovel)
        all_listings = pd.read_csv('Data/Raw/listings_terracap_{}_{}'.format(edital, year))
        all_listings = pd.concat([all_listings, imovel])
        all_listings.to_csv('Data/Raw/listings_terracap_{}_{}'.format(edital, year), index=False)
        list_urls.remove(link)
        print(len(list_urls))


# Tem q fazer um merge com o df_imoveis_edital
df_2 = df_imoveis_edital[['url_details', 'coord_name', 'coords']]
df_2.rename(columns={'url_details': 'url'}, inplace=True)

merged_df = pd.merge(all_listings, df_2, on='url')
merged_df.to_csv('Data/Raw/merged_listings_terracap_{}_{}'.format(edital, year), index=False)
merged_df.to_excel('temp_11_2023.xlsx')

df_sold_properties = sold_properties(bidding=10, year=2023)
df_sold_properties.to_csv('Data/Raw/sold_listings_terracap_{}_{}'.format(edital, year), index=False)


# Merging all dataframes
lista_def = merged_df
df_vendidos = df_sold_properties

df_vendidos['endereco_comp'] = df_vendidos['endereco'].str.replace(" ", "")
lista_def['end_comp'] = lista_def['end'].str.replace(" ", "")

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
                          'area': 'Área'}, inplace=True)

for i in range(len(lista_def)):
    try:
        lista_def['Área Construção Básica'].iloc[i] = float(lista_def['Área Construção Básica'].iloc[i].split(" ")[0])
    except:
        pass
    try:
        lista_def['Área Construção Máxima'].iloc[i] = float(lista_def['Área Construção Máxima'].iloc[i].split(" ")[0])
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
        lista_def['R$ Valor / Pot. Max'][i] = float(lista_def['Valor Lance Vencedor'][i])/float(lista_def['Área Construção Máxima'][i])
    except:
        lista_def['R$ Valor / Pot. Max'][i] = float(lista_def['Valor de Face'][i]) / float(lista_def['Área Construção Máxima'][i])
    try:
        lista_def['Número Meses'][i] = int(terrenos_selecionados['meses'][0])
    except:
        lista_def['Número Meses'][i] = '-'
    try:
        lista_def['Entrada'][i] = '{}%'.format(int(terrenos_selecionados['entrada'][0] * 100))

    except:
        lista_def['Entrada'][i] = '-'


lista_def['R$ Valor Face / Pot. Max'] = lista_def['valor_face']/lista_def['Área Construção Máxima']
lista_def.to_csv('Data/Processed/merged_listings_{}_{}'.format(edital, year), index=False)


























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

import ast
def revert_geometries(df):
    temp =[]
    for i in range(len(df)):
        coord = ast.literal_eval(df.geometry.iloc[i])
        new_temp = []
        for item in coord:
            item.reverse()
            new_temp.append(item)
        temp.append(new_temp)
    return temp

temp = revert_geometries(df=all_listings)
all_listings['geometry'] = pd.Series(temp)
df_new = pd.concat([all_listings, df])

# Atualizar o edital atual
listings = df_new.copy()









for i in range(len(listings)):
     if listings['edital_x'].iloc[i] == '6/2023':
          listings['edital_x'].iloc[i] = listings['edital_x'].iloc[i] + '- (Atual)'
     else:
         pass

for i in range(len(listings)):
     if listings['edital_x'].iloc[i] == '5/2023- (Atual)':
          listings['edital_x'].iloc[i] = '5/2023'
     else:
         pass




df_new.to_csv('terracap_atualizado_{}.csv'.format(edital))


