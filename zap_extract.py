# pip install zenrows
from zenrows import ZenRowsClient
from lxml import html

client = ZenRowsClient("273d07168188caf021d46c84f1764213cb932f9f")
url = "https://www.zapimoveis.com.br/imovel/venda-cobertura-3-quartos-petropolis-porto-alegre-rs-327m2-id-2655122330/"

response = client.get(url)
# Parse the HTML string
tree = html.fromstring(response.text)

tree

# Define an XPath expression to select elements
xpath_expression = "//p"

# Use XPath to find elements matching the expression
elements = tree.xpath(xpath_expression)

# Loop through the selected elements and print their text content
for element in elements:
    print(element.text)





