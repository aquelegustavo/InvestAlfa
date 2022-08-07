import requests
from bs4 import BeautifulSoup

url = "https://valorinveste.globo.com/cotacoes/"

html_response = requests.get(url=url)

soup = BeautifulSoup(html_response.text, 'html.parser')

rows = soup.table.tbody("tr")

for row in rows:

    name = row("td")[0].text.strip()
    code = row("td")[1].text.strip()
    value = (row("td")[2]
             .text
             .strip()
             .replace(',', '.'))

    print(
        f"""
        name={name},
        code={code},
        value={value}
        """)
