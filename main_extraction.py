from functions import get_edital, get_basic_info_monthly_edict_terracap, get_details_terracap, check_df_edital, \
    sold_properties
from Transform.transform import add_missing_columns, revert_geometries
import pandas as pd

edital = input('Entre o número do Edital: ')
tipo = input('Atual (a) ou Passado (p) : ')

if tipo == 'a':
    year = 2023

    imoveis_edital = get_basic_info_monthly_edict_terracap(edital=edital, year=year)
    imoveis_edital = pd.DataFrame(imoveis_edital)

    check_df_edital(edital, year)

    all_listings = pd.read_csv('Data/Raw/listings_terracap_{}_{}'.format(edital, year))
    all_listings = all_listings.drop_duplicates(subset='url')
    mask = imoveis_edital[~imoveis_edital["url_details"].isin(all_listings["url"])]
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

    imoveis_edital = imoveis_edital[['url_details', 'coord_name', 'coords']]
    imoveis_edital.rename(columns={'url_details': 'url'}, inplace=True)

    merged_df = pd.merge(all_listings, imoveis_edital, on='url')
    merged_df.to_csv('Data/Raw/merged_listings_terracap_{}_{}'.format(edital, year), index=False)

    df_listings = pd.read_csv('Data/Raw/merged_listings_terracap_{}_{}'.format(edital, year))
    df_all_listings = pd.read_csv('Data/Ready/all_listings_updated_{}_{}'.format(int(edital) - 1, year))

#    df_listings.drop(columns=['Valor de Face'], inplace=True)
    # .drop(columns=['Unnamed: 0', 'edital_y', 'Unnamed: 0.3', 'Unnamed: 0.1', 'Unnamed: 0.2'], inplace=True)

    df_all_listings = df_all_listings.rename(
        columns={'edital_x': 'Edital', 'valor_caucao_x': 'Valor Caução', 'cond_pgto': 'Condição de Pagamento',
                 })

    df_listings.rename(
        columns={'edital': 'Edital', 'n_imovel_no_edital': 'Nº do Imóvel no Edital', 'destinacao': 'Destinação',
                 'end': 'Endereço', 'area': 'Área', 'area_const_basica': 'Área Construção Básica',
                 'area_const_max': 'Área Construção Máxima', 'url': 'url_details', 'valor_face': 'Valor de Face',
                 'cond_pgto': 'Condição de Pagamento', 'valor_caucao': 'Valor Caução',
                 'coords': 'geometry'}, inplace=True)

    temp = revert_geometries(df=df_listings)
    df_listings['geometry'] = pd.Series(temp)
    df_listings = add_missing_columns(df_all_listings, df_listings)
    df_all_listings = pd.concat([df_listings, df_all_listings])

    df_all_listings.reset_index(drop=True, inplace=True)

    df_actual_listings = df_all_listings[df_all_listings['Edital'] == '{}/{}'.format(edital, str(year))]
    df_past_listings = df_all_listings[~(df_all_listings['Edital'] == '{}/{}'.format(edital, str(year)))]

    # find first element of df_actual_listings in the rows of df_all_listings edital column
    for terracap_code in df_actual_listings['id_terracap']:

        if len(df_past_listings[df_past_listings['id_terracap'] == terracap_code]) >= 1:
            df_temp = df_past_listings[df_past_listings['id_terracap'] == terracap_code]

            for i in range(len(df_temp)):
                print(len(df_temp))
                # localize the row of df_all_listings that has the same id_terracap as terracap code
                index_present_edital = df_all_listings[df_all_listings['id_terracap'] == terracap_code].index[0]
                index_old_edital = df_all_listings[df_all_listings['id_terracap'] == terracap_code].index[i+1]

                if df_all_listings['outros_editais_1'].iloc[index_present_edital] == None:
                    df_all_listings['outros_editais_1'].iloc[index_present_edital] = df_all_listings['Edital'].iloc[index_old_edital]

                elif df_all_listings['outros_editais_2'].iloc[index_present_edital] == None:
                    df_all_listings['outros_editais_2'].iloc[index_present_edital] = df_all_listings['Edital'].iloc[index_old_edital]

                elif df_all_listings['outros_editais_3'].iloc[index_present_edital] == None:
                    df_all_listings['outros_editais_3'].iloc[index_present_edital] = df_all_listings['Edital'].iloc[index_old_edital]

                elif df_all_listings['outros_editais_4'].iloc[index_present_edital] == None:
                    df_all_listings['outros_editais_4'].iloc[index_present_edital] = df_all_listings['Edital'].iloc[index_old_edital]

                elif df_all_listings['outros_editais_5'].iloc[index_present_edital] == None:
                    df_all_listings['outros_editais_5'].iloc[index_present_edital] = df_all_listings['Edital'].iloc[index_old_edital]

                elif df_all_listings['outros_editais_6'].iloc[index_present_edital] == None:
                    df_all_listings['outros_editais_6'].iloc[index_present_edital] = df_all_listings['Edital'].iloc[index_old_edital]

                elif df_all_listings['outros_editais_7'].iloc[index_present_edital] == None:
                    df_all_listings['outros_editais_7'].iloc[index_present_edital] = df_all_listings['Edital'].iloc[index_old_edital]

                elif df_all_listings['outros_editais_8'].iloc[index_present_edital] == None:
                    df_all_listings['outros_editais_8'].iloc[index_present_edital] = df_all_listings['Edital'].iloc[index_old_edital]

                elif df_all_listings['outros_editais_9'].iloc[index_present_edital] == None:
                    df_all_listings['outros_editais_9'].iloc[index_present_edital] = df_all_listings['Edital'].iloc[index_old_edital]

                else:
                    print('abrir novo campo para {}'.format(terracap_code))

        else:
            pass

    df_all_listings.to_csv('Data/Ready/all_listings_updated_actual_{}_{}'.format(edital, year), index=False)

elif tipo == 'p':
    imoveis_edital = get_basic_info_monthly_edict_terracap(edital=edital, year=2023)

else:
    print('Tipo inválido')
