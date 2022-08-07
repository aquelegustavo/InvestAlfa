from bs4 import BeautifulSoup
import requests
from .models import Quote


def data():
    url = "https://valorinveste.globo.com/cotacoes/"

    html_response = requests.get(url=url)

    soup = BeautifulSoup(html_response.text, 'html.parser')

    rows = soup.table.tbody("tr")

    ids = []

    for row in rows:

        name = row("td")[0].text.strip()
        code = row("td")[1].text.strip()
        value = (row("td")[2]
                 .text
                 .strip()
                 .replace(',', '.'))

        value = 0 if value == "-" else float(value)

        quote = Quote(
            name=name,
            code=code,
            value=value
        )

        quote.save()

        ids.append(quote.id)

    return ids
