from scrapy.selector import Selector
import time
import undetected_chromedriver as uc
import re
import pandas as pd

# Defining possible bidding dates
bidding_all = []
listings = pd.read_csv('terracap_todos_licitacao.csv')
num_imovel_list = listings['url_details'].tolist()
def remove(num_imovel_list):
    all_listings = pd.read_csv('listing_terracap_detail.csv')
    list_of_all_listings = all_listings['url'].tolist()
    for i in list_of_all_listings:
        try:
            num_imovel_list.remove(i)
        except:
            pass
remove(num_imovel_list)


def get_details_terracap(url):
    link_terracap = url
    print(link_terracap)
    temp = []
    # FIRST PAGE
    options = uc.ChromeOptions()
#    options.add_argument("--no-sandbox")
#    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    driver = uc.Chrome(options=options)
#        driver = Chrome()
    driver.get(link_terracap)
    time.sleep(2)
    html = driver.page_source
    response_obj = Selector(text=html)
    item = response_obj.xpath('//div[contains(@class, "form-body")]')
    items = item.xpath('.//div[contains(@class, "form-control")]/text()').getall()
    try:
        edital = items[0]
    except:
        edital = None
    try:
        n_imovel_no_edital = int(items[1])
    except:
        n_imovel_no_edital = None
    try:
        valor_face = items[2]
        valor_face = valor_face.replace("R$", "")
        valor_face = int(valor_face.split(',')[0].replace(".", ""))
    except:
        valor_face = None
    try:
        valor_caucao = items[3]
        valor_caucao = valor_caucao.replace("R$", "")
        valor_caucao = int(valor_caucao.split(',')[0].replace(".", ""))
    except:
        valor_caucao = None

    try:
        cond_pgto = items[4]
    except:
        cond_pgto = None

    try:
        _next = driver.find_element('xpath', "//a[contains(@class, 'fa fa-info')]")
        _next.click()
        time.sleep(2)
    except:
        print("--## FIM DA CAPTURA ##--")
    # Lista de atributos
    driver.switch_to.window(driver.window_handles[1])
    html = driver.page_source
    response = Selector(text=html)

    # Destinação de Uso do Lote:
    destinacao = response.xpath('//textarea[contains(@class, "form-control")]/text()').extract()[0]

    list_att = response.xpath('//div[contains(@class, "form-control")]/text()').extract()
    # Número de Identificação do Imóvel:
    id_terracap = list_att[0]

    # Endereço:
    end = list_att[1]

    # TESTES DE COERENCIA
    lista_teste_situacao = ["FIRME", "REGULAR", "IRREGULAR", "ISOLADO", "MEIO DA QUADRA", "ESQUINA"]
    lista_teste_tipo_solo = ["REGULAR", "IRREGULAR", "ISOLADO", "MEIO DA QUADRA", "ESQUINA"]
    lista_teste_forma = ["ISOLADO", "MEIO DA QUADRA", "ESQUINA"]

    # Número do Item:
    classificacao = list_att[2]
    if classificacao == 'PLANO':
        classificacao = str(10)
        relevo = list_att[2]
    else:
        relevo = list_att[3]

    if any(char.isdigit() for char in relevo) and any(char.isdigit() for char in classificacao):
        classificacao = None
        relevo = None
        area = list_att[2]
        area = area.split(".")[0]
        area_const_basica = list_att[3]
        area_const_basica = area_const_basica.split(".")[0]
        area_const_max = list_att[4]
        area_const_max = area_const_max.split(".")[0]
        try:
            situacao = list_att[5]
            if any(situacao == i for i in lista_teste_situacao):
                situacao = None
                tipo_de_solo = list_att[5]
                if any(tipo_de_solo == i for i in
                 lista_teste_tipo_solo):
                    tipo_de_solo = None
                    forma =  list_att[5]
                    if any(forma == i for i in lista_teste_forma):
                        forma = None
                        posicao = list_att[5]
                    else:
                        try:
                            posicao = list_att[6]
                        except:
                            posicao = None
                else:
                    try:
                        forma = list_att[6]
                        if any(forma == i for i in lista_teste_forma):
                            forma = None
                            posicao = list_att[6]
                        else:
                            try:
                                posicao = list_att[7]
                            except:
                                posicao = None
                    except:
                        forma = None
                        posicao = None
            else:
                try:
                    tipo_de_solo = list_att[6]
                    if any(tipo_de_solo == i for i in lista_teste_tipo_solo):
                        tipo_de_solo = None
                        forma =  list_att[6]
                        if any(forma == i for i in lista_teste_forma):
                            forma = None
                            posicao = list_att[6]
                        else:
                            try:
                                posicao = list_att[7]
                            except:
                                posicao = None
                    else:
                        try:
                            forma = list_att[7]
                            if any(forma == i for i in lista_teste_forma):
                                forma = None
                                posicao = list_att[7]
                            else:
                                try:
                                    posicao = list_att[8]
                                except:
                                    posicao = None
                        except:
                            forma = None
                            posicao = None
                except:
                    tipo_de_solo = None
                    forma = None
                    posicao = None
        except:
            situacao = None
            tipo_de_solo = None
            forma = None
            posicao = None

    elif any(char.isdigit() for char in relevo) or any(char.isdigit() for char in classificacao):
        if any(char.isdigit() for char in classificacao):
            classificacao = None
        else:
            classificacao = list_att[2]

        if any(char.isdigit() for char in relevo):
            relevo = None
        else:
            relevo = list_att[2]

        area = list_att[3]
        area = area.split(".")[0]
        area_const_basica = list_att[4]
        area_const_basica = area_const_basica.split(".")[0]
        area_const_max = list_att[5]
        area_const_max = area_const_max.split(".")[0]

        try:
            situacao = list_att[6]
            if any(situacao == i for i in lista_teste_situacao):
                situacao = None
                tipo_de_solo = list_att[6]
                if any(tipo_de_solo == i for i in lista_teste_tipo_solo):
                    tipo_de_solo = None
                    forma =  list_att[6]
                    if any(forma == i for i in lista_teste_forma):
                        forma = None
                        posicao = list_att[6]
                    else:
                        try:
                            posicao = list_att[7]
                        except:
                            posicao = None
                else:
                    try:
                        forma = list_att[7]
                        if any(forma == i for i in lista_teste_forma):
                            forma = None
                            posicao = list_att[7]
                        else:
                            try:
                                posicao = list_att[8]
                            except:
                                posicao = None
                    except:
                        forma = None
                        posicao = None
            else:
                try:
                    tipo_de_solo = list_att[7]
                    if any(tipo_de_solo == i for i in lista_teste_tipo_solo):
                        tipo_de_solo = None
                        forma =  list_att[7]
                        if any(forma == i for i in lista_teste_forma):
                            forma = None
                            posicao = list_att[7]
                        else:
                            try:
                                posicao = list_att[8]
                            except:
                                posicao = None
                    else:
                        try:
                            forma = list_att[8]
                            if any(forma == i for i in lista_teste_forma):
                                forma = None
                                posicao = list_att[8]
                            else:
                                try:
                                    posicao = list_att[9]
                                except:
                                    posicao = None
                        except:
                            forma = None
                            posicao = None
                except:
                    tipo_de_solo = None
                    forma = None
                    posicao = None
        except:
            situacao = None
            tipo_de_solo = None
            forma = None
            posicao = None

    else:
        area = list_att[4]
        area = area.split(".")[0]
        area_const_basica = list_att[5]
        area_const_basica = area_const_basica.split(".")[0]
        area_const_max = list_att[6]
        area_const_max = area_const_max.split(".")[0]

        try:
            situacao = list_att[7]
            if any(situacao == i for i in lista_teste_situacao):
                situacao = None
                tipo_de_solo = list_att[7]
                if any(tipo_de_solo == i for i in lista_teste_tipo_solo):
                    tipo_de_solo = None
                    forma =  list_att[7]
                    if any(forma == i for i in lista_teste_forma):
                        forma = None
                        posicao = list_att[7]
                    else:
                        try:
                            posicao = list_att[8]
                        except:
                            posicao = None
                else:
                    try:
                        forma = list_att[8]
                        if any(forma == i for i in lista_teste_forma):
                            forma = None
                            posicao = list_att[8]
                        else:
                            try:
                                posicao = list_att[9]
                            except:
                                posicao = None
                    except:
                        forma = None
                        posicao = None
            else:
                try:
                    tipo_de_solo = list_att[8]
                    if any(tipo_de_solo == i for i in lista_teste_tipo_solo):
                        tipo_de_solo = None
                        forma =  list_att[8]
                        if any(forma == i for i in lista_teste_forma):
                            forma = None
                            posicao = list_att[8]
                        else:
                            try:
                                posicao = list_att[9]
                            except:
                                posicao = None
                    else:
                        try:
                            forma = list_att[9]
                            if any(forma == i for i in lista_teste_forma):
                                forma = None
                                posicao = list_att[9]
                            else:
                                try:
                                    posicao = list_att[10]
                                except:
                                    posicao = None
                        except:
                            forma = None
                            posicao = None
                except:
                    tipo_de_solo = None
                    forma = None
                    posicao = None
        except:
            situacao = None
            tipo_de_solo = None
            forma = None
            posicao = None

    # Dimensões do Lote
    dimensions = response.xpath('//div[contains(@class, "description")]/text()').extract()

# Frente
    try:
        frente = dimensions[0]
        frente = frente.split(",")[0]
        frente = re.sub("[^0-9]", "", frente)
        if len(frente) >= 4:
            frente = None
        else:
            frente = int(frente)
    except:
        frente = None

        # Fundo
    try:
        fundo = dimensions[1]
        fundo = fundo.split(",")[0]
        fundo = re.sub("[^0-9]", "", fundo)
        if len(fundo) >= 4:
            fundo = None
        else:
            fundo = int(fundo)
    except:
        fundo = None

    # Lado Direito
    try:
        lado_direito = dimensions[2]
        lado_direito = lado_direito.split(",")[0]
        lado_direito = re.sub("[^0-9]", "", lado_direito)
        if len(lado_direito) >= 4:
            lado_direito = None
        else:
            lado_direito = int(lado_direito)
    except:
        lado_direito = None

    # Lado Esquerdo
    try:
        lado_esquerdo = dimensions[3]
        lado_esquerdo = lado_esquerdo.split(",")[0]
        lado_esquerdo = re.sub("[^0-9]", "", lado_esquerdo)
        if len(lado_esquerdo) >= 4:
            lado_esquerdo = None
        else:
            lado_esquerdo = int(lado_esquerdo)
    except:
        lado_esquerdo = None

    temp.append({
        'edital': edital,
        'n_imovel_no_edital': n_imovel_no_edital,
        'destinacao': destinacao,
        'area': area,
        'area_const_basica': area_const_basica,
        'area_const_max': area_const_max,
        'valor_face': valor_face,
        'valor_caucao': valor_caucao,
        'cond_pgto': cond_pgto,
        'id_terracap': id_terracap,
        'end': end,
        'classficacao': classificacao,
        'relevo': relevo,
        'situacao': situacao,
        'tipo_de_solo': tipo_de_solo,
        'forma': forma,
        'posicao': posicao,
        'frente': frente,
        'fundo': fundo,
        'lado_direito': lado_direito,
        'lado_esquerdo': lado_esquerdo,
        'url': url
    })
    driver.quit()
    return temp

df = pd.read_csv('/home/luizneto/PycharmProjects/terracapScraper/info_basica_terracap_2023')
url = df['url_details'][0]

try:
    num_imovel_list.remove('https://comprasonline.terracap.df.gov.br/item/external/show?edict_number=7&edict_year=2022&item=24')
    num_imovel_list.remove('https://comprasonline.terracap.df.gov.br/item/external/show?edict_number=6&edict_year=2020&item=2')
except:
    pass

listings = listings[(listings.url_details != 'https://comprasonline.terracap.df.gov.br/item/external/show?edict_number=6&edict_year=2020&item=2')
                      & (listings.url_details != 'https://comprasonline.terracap.df.gov.br/item/external/show?edict_number=7&edict_year=2022&item=24')]


all_listings.rename(columns={'url': 'url_details'}, inplace=True)
merged_df = pd.merge(all_listings, listings, on='url_details')
df_new = merged_df.drop_duplicates(subset=['coords', 'edital_y'])
#df_new.to_csv('todos_limpos.csv', index=False)

df_duplicated = df_new[df_new.duplicated(subset='id_terracap')]
df_new['outros_editais_9'] = None
df_new_unique = df_new.drop_duplicates(subset='id_terracap')
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
a = df_new_unique[df_new_unique['id_terracap'] == '807187-0']
b = df_new[df_new['id_terracap'] == '807187-0']


df_new_unique.to_csv('df_terracap_df_1.csv', index=0)

num_imovel_list = df['url_details'].tolist()

all_listings['url']





for link in num_imovel_list:
    imovel = get_details_terracap(url=link)
    imovel = pd.DataFrame(imovel)
    all_listings = pd.read_csv('listings_terracap_2023')
    all_listings = pd.concat([all_listings, imovel])
    all_listings.to_csv('listings_terracap_2023', index=False)
    num_imovel_list.remove(link)
    print(len(num_imovel_list))

all_listings = all_listings.drop_duplicates(subset='url')
mask = df[~df["url_details"].isin(all_listings["url"])]
num_imovel_list = mask['url_details'].tolist()



















