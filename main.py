from scrapy.selector import Selector
import time
import json as json
import undetected_chromedriver as uc
from datetime import datetime
import pandas as pd
from selenium import webdriver

a = pd.read_csv('terracap_todos_licitacao.csv')



year = 2023
page = 1
number = 2

def get_basic_info_monthly_edict_terracap(number, year, page):
    _date = datetime.today().strftime('%Y-%m-%d')
    link = 'https://comprasonline.terracap.df.gov.br/?edict_number={}&edict_year={}&page={}&item=&ra=&destination=&min=&max=&area_min=&area_max='.format(number, year, page)
    print('Scraping {} out of {}'.format(number, 18))
    options = uc.ChromeOptions()
    #options.headless = True
#    options.add_argument('--headless=new')
    driver = uc.Chrome(options=options)
    driver.get(link)
    time.sleep(5)
    temp = []
    go = True
    html = driver.page_source
    response_obj = Selector(text=html)
    #Número de Páginas
    try:
        n_pages = response_obj.xpath('//font[contains(@id, "titulo-paginacao")]/text()').getall()[0]
        n_pages = int(n_pages.split('de')[1].split('\n')[0])
        for j in range(n_pages):
            num_page = 2+j
            #GETING everything
            html = driver.page_source
            response_obj = Selector(text=html)
            itens = response_obj.xpath('//div[contains(@class, "card mb-3 sombreado")]')
            for i in range(len(itens)):
                listing = itens[i]
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
                time.sleep(5)
            except:
                print("--## FIM DA CAPTURA ##--")
    except:
        print('Page out of range')
    driver.quit()
    return temp

year = 2023
page = 1
year_terracap = []
for number in range(2, 5):
     temp = get_basic_info_monthly_edict_terracap(number, year, page)
     print(temp)
     year_terracap += temp


df_terracap = pd.DataFrame(year_terracap)
df_terracap.to_csv('info_basica_terracap_2023')


