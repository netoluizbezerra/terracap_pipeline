from functions import get_edital, get_basic_info_monthly_edict_terracap, get_details_terracap, check_df_edital, \
    get_unique_elements
import pandas as pd

edital = get_edital()
edital = edital.replace("/", "_")
imoveis_edital = get_basic_info_monthly_edict_terracap()
df_imoveis_edital = pd.DataFrame(imoveis_edital)
list_urls = df_imoveis_edital['url_details'].tolist()
check_df_edital(edital)

df_imoveis_edital = pd.read_csv('edital_{}'.format(edital))
all_listings = pd.read_csv('listings_terracap_{}'.format(edital))
all_listings = all_listings.drop_duplicates(subset='url')
mask = df_imoveis_edital[~df_imoveis_edital["url_details"].isin(all_listings["url"])]
list_urls = mask['url_details'].tolist()


for link in list_urls:
    imovel = get_details_terracap(url=link)
    imovel = pd.DataFrame(imovel)
    all_listings = pd.read_csv('listings_terracap_{}'.format(edital))
    all_listings = pd.concat([all_listings, imovel])
    all_listings.to_csv('listings_terracap_{}'.format(edital), index=False)
    list_urls.remove(link)
    print(len(list_urls))

all_listings.drop_duplicates(subset=['url'], inplace=True)

df = pd.read_csv('terracap_atualizado_2.csv')
all_listings = pd.read_csv('listings_terracap_{}'.format(edital))
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
all_listings.to_csv('terracap_atualizado_{}.csv'.format(edital))

