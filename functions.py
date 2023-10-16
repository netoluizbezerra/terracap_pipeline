from scrapy.selector import Selector
from typing import List, Dict
import undetected_chromedriver as uc
import re
import time as time
import pandas as pd
import ast
import os
import patch


def get_edital():
    from path_maker import path

    """
    Scrapes the Edital number from a webpage.

    Returns:
        A string representing the Edital number, or None if no Edital number was found.
    """
    # Define the URL to scrape
    path = str(path)
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', patch.webdriver_executable()))
    link = 'https://comprasonline.terracap.df.gov.br/'
    # Set up the options for the Chrome driver
    options = uc.ChromeOptions()
    options.add_argument("--headless=new")  # Run Chrome in headless mode
    # Start the Chrome driver in a context manager to ensure proper cleanup
    with uc.Chrome(options=options, driver_executable_path=webdriver_path) as driver:
        # Load the URL in the driver and get the page source
        driver.get(link)
        html = driver.page_source
    # Parse the HTML source using Scrapy's Selector
    response_obj = Selector(text=html)
    # Find the element containing the Edital number
    item = response_obj.xpath('//h1[contains(@id, "edital-title")]')
    # Get a list of all the text elements inside <strong> tags
    edital_list = item.xpath('.//strong/text()').getall()
    # Check if the list is not empty
    if edital_list:
        # Extract the Edital number from the first element in the list
        edital = edital_list[0].strip().partition(": ")[2]
        return edital
    else:
        # Return None if no Edital number was found
        return None


def get_basic_info_monthly_edict_terracap(edital, year) -> List[Dict]:
    from path_maker import path
    """
    Scrape information about real estate properties from the website
    https://comprasonline.terracap.df.gov.br/.

    Returns:
        A list of dictionaries with the scraped information.
    """
    # Set up web driver and go to the website
    link = 'https://comprasonline.terracap.df.gov.br/?edict_number={}&edict_year={}&page={}&item=&ra=&destination=&min=&max=&area_min=&area_max='.format(edital, year, 1)
    path = str(path)
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', patch.webdriver_executable()))
    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    driver = uc.Chrome(options=options, driver_executable_path=webdriver_path)
    driver.get(link)
    time.sleep(2)
    temp = []
    html = driver.page_source
    response_obj = Selector(text=html)
    # Get the number of pages to iterate over
    try:
        n_pages = response_obj.xpath('//font[contains(@id, "titulo-paginacao")]/text()').getall()[0]
        n_pages = int(n_pages.split('de')[1].split('\n')[0])
        for j in range(n_pages):
            num_page = 2+j
            html = driver.page_source
            response_obj = Selector(text=html)
            items = response_obj.xpath('//div[contains(@class, "card mb-3 sombreado")]')

            # Iterate over each page and scrape the data
            for i in range(len(items)):
                listing = items[i]
                titulo = listing.xpath('.//h3[contains(@class, "card-title")]/text()').get()
                edital = titulo.split('Edital : ')[1].split('\n')[0]
                item_do_edital = titulo.split('Item : ')[1].split("xa")[0]
                all_url_details = listing.xpath('//div[contains(@class, "btn-group-vertical")]//a[contains(@class, "btn btn-default")]//@href').getall()
                url_details = [url for url in all_url_details if 'external/show' in url][i]
                url_details = 'https://comprasonline.terracap.df.gov.br{}'.format(url_details)

                _all = listing.xpath('.//p[contains(@class, "card-text")]/text()').getall()
                endereco = _all[0].split(': ')[1]
                bairro = _all[1].split(': ')[1]
                n_imoveis = int(_all[2].split(': ')[1])
                try:
                    area = int(_all[3].split(': ')[1].replace("m²", ""))
                except:
                    area = _all[3].split(': ')[1].replace("m²", "")
                    area = int(area.split('.')[0])

                valor_compra_temp = _all[4].split(': ')[1].replace("R$", "")
                valor_compra = int(valor_compra_temp.split(',')[0].replace(".", ""))
                valor_caucao_temp = _all[4].split(': ')[1].replace("R$", "")
                valor_caucao = int(valor_caucao_temp.split(',')[0].replace(".", ""))
                uso = listing.xpath('.//small[contains(@class, "text-muted")]/text()').getall()[0]
                coord_name = listing.xpath('.//input[contains(@type, "hidden")]/@name').getall()[0]
                coords = listing.xpath('.//input[contains(@type, "hidden")]/@value').getall()[0]

                temp.append({
                            'titulo': titulo,
                            'edital': edital,
                            'item': item_do_edital,
                            'url_details': url_details,
                            'endereco': endereco,
                            'bairro': bairro,
                            'n_imoveis': n_imoveis,
                            'area': area,
                            'valor_compra': valor_compra,
                            'valor_caucao': valor_caucao,
                            'uso': uso,
                            'coord_name': coord_name,
                            'coords': coords
                            })

            try:
                print('TENTAR PÁGINA {} de {}'.format(j+2, num_page))
                _next = driver.find_element('xpath',
                    '//a[contains(text(),{})]'.format(num_page)
                )
                _next.click()
                time.sleep(3)
            except:
                print("--## FIM DA CAPTURA ##--")
    except:
        print('Page out of range')
    driver.quit()
    return temp


def get_details_terracap(url):
    from path_maker import path
    path = str(path)
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', patch.webdriver_executable()))
    link_terracap = url
    print(link_terracap)
    temp = []
    # FIRST PAGE
    options = uc.ChromeOptions()
#    options.add_argument("--no-sandbox")
#    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    driver = uc.Chrome(options=options, driver_executable_path=webdriver_path)
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


def check_df_edital(edital, year):
    try:
        all_listings = pd.read_csv('Data/Raw/listings_terracap_{}_{}'.format(edital, year))
        print('Dataframe Already Created')
    except:
        df_new = pd.DataFrame(
            columns=['edital', 'n_imovel_no_edital', 'destinacao', 'area', 'area_const_basica', 'area_const_max',
                     'valor_face', 'valor_caucao', 'cond_pgto', 'id_terracap', 'end', 'classficacao', 'relevo',
                     'situacao', 'tipo_de_solo', 'forma', 'posicao', 'frente', 'fundo', 'lado_direito', 'lado_esquerdo',
                     'url'])
        df_new.to_csv('Data/Raw/listings_terracap_{}_{}'.format(edital, year), index=False)
        print('Dataframe has been Created')


def get_unique_elements(list1, list2):
    unique_list1 = []
    unique_list2 = []

    for element in list1:
        if element not in list2:
            unique_list1.append(element)

    for element in list2:
        if element not in list1:
            unique_list2.append(element)

    return unique_list1, unique_list2


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


def sold_properties(year, bidding):
    from path_maker import path
    path = str(path)
    webdriver_path = os.path.normpath(os.path.join(os.getcwd(), 'webdriver', patch.webdriver_executable()))
    link_terracap = 'https://comprasonline.terracap.df.gov.br/bidding/external/index?utf8=%E2%9C%93&edict_year={}&edict_number={}&number_item=&commit=Consultar'.format(year, (bidding))
    print(link_terracap)
    driver = uc.Chrome(driver_executable_path=webdriver_path)
    driver.get(link_terracap)
    html = driver.page_source
    response_obj = Selector(text=html)
    items = response_obj.xpath('//div[contains(@class, "card")]')
    items = items[1:]
    temp = []
    if len(items) >= 1:
        print('Edital {} do ano de {}'.format(bidding, year))
        for item in items:
            titulo = item.xpath('.//div[contains(@class, "header")]/text()').get()
            features = item.xpath('.//div[@class="content"]/div/text()').getall()

            #features.append(titulo)
            output_features = []
            for feature in features:
                input_string = feature.split("\n")[1]
                input_string = input_string.lstrip()
                print(input_string)
                output_features.append(input_string)

            endereco = None
            licitante = None
            valor = None
            condicao = None
            meses = None
            entrada = None
            edital = None
            button = 'Desclassificado'

            if len(output_features) > 0:
                try:
                    endereco = output_features[1].split(': ')[1]
                except:
                    pass

                try:
                    licitante = re.sub("[^0-9]", "", output_features[2])
                except:
                    pass

                try:
                    valor = output_features[3].split(': ')[1].replace("R$", "")
                    valor = int(valor.split(',')[0].replace(".", ""))
                except:
                    pass

                try:
                    condicao = output_features[4].split(': ')[1]
                except:
                    pass

                try:
                    meses = int(re.sub("[^0-9]", "", output_features[5]))
                except:
                    pass

                try:
                    entrada = float(re.sub("[^0-9]", "", output_features[6])) / 100
                except:
                    pass

                try:
                    edital = output_features[0].split(': ')[1]
                except:
                    pass

                try:
                    button_text = item.xpath('.//div[contains(@class, "button")]/text()').getall()[1]
                    button = int(re.sub("[^0-9]", "", button_text))
                except:
                    pass

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
    driver.quit()
    return pd.DataFrame(temp)










