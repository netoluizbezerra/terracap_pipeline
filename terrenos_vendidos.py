from scrapy.selector import Selector
import undetected_chromedriver as uc
from datetime import datetime
import re
import time
from selenium.webdriver import Chrome
#biddings = list(range(18))
biddings = [1, 2, 3]
years = [2023]
# Defining possible bidding dates
bidding_all = []
_date = datetime.today().strftime('%Y-%m-%d')

for year in years:
    for bidding in biddings:
        link_terracap = 'https://comprasonline.terracap.df.gov.br/bidding/external/index?utf8=%E2%9C%93&edict_year={}&edict_number={}&number_item=&commit=Consultar'.format(year, (bidding+1))
        print(link_terracap)
        time.sleep(20)
        temp = []
        # FIRST PAGE
        # options = uc.ChromeOptions()
        # options.headless = True
        # options.add_argument('--headless')
        driver = uc.Chrome()
        driver.get(link_terracap)
        html = driver.page_source
        response_obj = Selector(text=html)
        item = response_obj.xpath('//div[contains(@class, "card")]')

        if len(item) >= 1:
            print('Edital {} do ano de {}'.format(bidding, year))
            for i in range(len(item)):
                link = item[i]
                titulo = link.xpath('.//div[contains(@class, "header")]/text()').get()
                features = link.xpath('.//div[contains(@class, "description")]/text()').getall()
                features.append(titulo)
                t = 0
                for feat in features:
                    input_string = feat.split("\n")[1]
                    output_string = []
                    for index in range(len(input_string)):

                        if input_string[index] != ' ':
                            if space_flag == True:
                                if (input_string[index] == '.'
                                        or input_string[index] == '?'
                                        or input_string[index] == ','):
                                    pass
                                else:
                                    output_string.append(' ')
                                space_flag = False
                            output_string.append(input_string[index])
                        elif input_string[index - 1] != ' ':
                            space_flag = True
                    features[t] = output_string
                    t+=1
                    print(''.join(output_string))
                try:
                    endereco = ''.join(features[0]).split(': ')[1]
                except:
                    endereco = None

                try:
                    licitante = ''.join(features[1])
                    licitante = re.sub("[^0-9]", "", licitante)
                except:
                    licitante = None

                try:
                    valor = ''.join(features[2])
                    valor = valor.split(': ')[1].replace("R$", "")
                    valor = int(valor.split(',')[0].replace(".", ""))
                except:
                    valor = None

                try:
                    condicao = ''.join(features[3]).split(': ')[1]
                except:
                    condicao = None

                try:
                    meses = ''.join(features[4])
                    meses = int(re.sub("[^0-9]", "", meses))
                except:
                    meses = None

                try:
                    entrada = ''.join(features[5])
                    entrada = float(re.sub("[^0-9]", "", entrada))/100
                except:
                    entrada = None

                try:
                    edital = ''.join(features[6]).split(': ')[1]
                except:
                    edital = None
                try:
                    button = link.xpath('.//div[contains(@class, "button")]/text()').getall()[1]
                    button = int(re.sub("[^0-9]", "", button))
                except:
                    button = 'Desclassificado'

                'button'

                temp.append({
                    'edital': edital,
                    'colocacao': button,
                    'endereco': endereco,
                    'licitante': licitante,
                    'condicao': condicao,
                    'meses': meses,
                    'entrada': entrada,
                    'valor': valor,
                })
        else:
            print('Edital não disponível')

        temp = temp[1:len(temp)]
        bidding_all.extend(temp)
        driver.close()

import pandas as pd
df = pd.DataFrame(bidding_all)
df.edital.unique()

df.to_csv('terrenos_vendidos_terracap_2023_new.csv', index=False)
terrenos_vendidos = pd.read_csv('terrenos_vendidos_terracap_2023_new.csv')


terrenos_vendidos = pd.read_csv('terrenos_vendidos_terracap.csv')
terrenos_vendidos_2 = pd.read_csv('terrenos_vendidos_terracap_2021_2022.csv')
terrenos_vendidos_3 = df.copy()
terrenos_vendidos = pd.concat([terrenos_vendidos, terrenos_vendidos_2, terrenos_vendidos_3])

terrenos_vendidos['endereco_comp'] = terrenos_vendidos['endereco'].str.replace(" ", "")
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




lista_def.to_csv('imoveis_cleaned_def_3')

end = 'ST HAB. J. BOTANICO AVENIDA DAS PAINEIRAS QD-05 CONJ E LT 14'.replace(" ", '')
a = lista_def[lista_def['end_comp'] == end]
a.Bairro
