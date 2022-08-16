"""
Comparador de valores min e max relativos a cada túnel

"""
from datetime import datetime
from django.forms.models import model_to_dict
from ..companies.models import Company
from ..monitoring.sender import send_email
from ..users.models import CustomUser
from .models import Monitoring


def compare(quotes):
    """
    Comparar e alterar valores

    Função responsável por comparar relativo ao min e max de cada túnel e atualizar os valores salvos no banco de dados. 

    Caso as cotações atuais sejam maiores ou menores que a faixa de preço do tunel, esta função chama a função responsável por notificar o usuário

    Arguments:
        quotes: (list) Lista contendo as últimas cotações obtidas

    """

    #quotes = model_to_dict(quotes)
    monitoring = Monitoring.objects.all()

    for moni in monitoring:
        quote = list(
            filter(lambda q: q.parent_company == moni.company, quotes))[0]
        print(quote)

        company = Company.objects.get(code=moni.company.code)

        notification_user(moni)

        if quote.value < company.min_quote:
            # Cotação menor
            company.min_quote = quote.value
            company.save()
            notification_user(moni)

        elif quote.value > company.max_quote:
            # Cotação maior
            company.max_quote = quote.value
            company.save()
            notification_user(moni)


def notification_user(moni):
    """
    Desencadear notificação de usuário

    Para garantir o cumprimento da frequência de monitoramento, a função verifica se a nova notificação está suficientemente espaçada (valor da frequência em milisegundos) da última notificação. 

    Caso as determinações da frequências estejam ok, a função responsável por enviar o email é chamada.

    """

    last_notification = datetime(moni.last_notification)
    delta = datetime.now() - last_notification

    if delta >= (moni.frequency * 60 * 1000):
        send_email(moni.user.uid, moni.id)
