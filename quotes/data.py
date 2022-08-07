from bs4 import BeautifulSoup
import requests
from .models import Quote
from companies.models import Company


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

        # Adequação do `value` para caso especial ("-")
        value = 0 if value == "-" else float(value)

        # Obtenção da empresa
        try:
            company = Company.objects.get(code=code)

        except Company.DoesNotExist:
            company = Company(
                name=name,
                code=code
            )
            company.save()

        quote = Quote(
            parent_company=company,
            value=value
        )

        quote.save()

        company.last_quote = value
        company.save()

        ids.append(quote.id)

    return ids
