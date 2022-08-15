from bs4 import BeautifulSoup
import requests
from .models import Quote
from companies.models import Company
from monitoring.comparator import compare


def get_data():
    url = "https://valorinveste.globo.com/cotacoes/"

    html_response = requests.get(url=url)

    soup = BeautifulSoup(html_response.text, 'html.parser')

    rows = soup.table.tbody("tr")

    ids = []
    current_quotes = []

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
                code=code,

                # Se a empresa não existe, o valor mínimo e máximo são os atuais
                min_quote=value,
                max_quote=value
            )
            company.save()

        quote = Quote(
            parent_company=company,
            value=value
        )

        quote.save()

        company.last_quote = value

        if quote.value < company.min_quote:
            company.min_quote = quote.value

        elif quote.value > company.max_quote:
            company.max_quote = quote.value

        company.save()

        current_quotes.append(quote)
        ids.append(quote.id)

    compare(current_quotes)
    return ids
